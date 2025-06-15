import json
import re
import os

#################################### GIves output of relevant example quesionts

def remove_placeholder_tags(text):
   
    return re.sub(r"\[\[☃.*?\]\]", "", text).strip()

def get_khan_academy_filepath(exercise_title):
    folder = './cleanedquestions'
    exercise_to_filemap_json = "./khanacademyquestionmap.json"
    
    if not os.path.exists(exercise_to_filemap_json):
        print(f"Error: Khan Academy mapping file not found at {exercise_to_filemap_json}")
        return None

    with open(exercise_to_filemap_json, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            if item['title'] == exercise_title:
                return os.path.join(folder, item['file_name'])
    return None

def get_engageny_filepath(grade, module, lesson):
    engageny_folder = './grade8lessonsmd'
    
    if not os.path.exists(engageny_folder):
        print(f"Error: EngageNY markdown lessons folder not found at {engageny_folder}")
        return None

    grade_str = f"g{grade}"
    module_str = f"m{module}"
    lesson_str = f"lesson-{lesson}"

    filename_pattern = rf"math-{grade_str}-{module_str}-topic-[a-z]-{lesson_str}-student\.md"
    
    for filename in os.listdir(engageny_folder):
        if re.match(filename_pattern, filename, re.IGNORECASE):
            return os.path.join(engageny_folder, filename)
    return None

def format_khan_academy_question(q):
    lines = []
    lines.append(f"---\n")
    lines.append(f"#### **Problem Type:** {q['problemType']}")
    lines.append(f"**Question:**\n{q['question']}\n")
    lines.append(f"**Has Image:** {'✅ Yes' if q['hasImage'] else '❌ No'}")

    if q.get("imageAlts"):
        lines.append("**Image Description(s):**")
        for alt in q["imageAlts"]:
            lines.append(f"- {alt}")

    if q["options"]:
        lines.append("\n**Options:**")
        for opt in q["options"]:
            content = opt.get("content", "")
            correct = " ✅" if opt.get("correct", False) else ""
            lines.append(f"- {content}{correct}")

    if q["hints"]:
        lines.append("\n**Hints:**")
        for i, hint in enumerate(q["hints"], 1):
            lines.append(f"{i}. {hint['content']}")
            if 'alt' in hint:
                lines.append(f"   - _Image description_: {hint['alt']}")

    return "\n".join(lines)

def format_engageny_lesson_content(title, content):
    lines = []
    lines.append("---\n")
    lines.append(f"### EngageNY Lesson: {title}\n")
    lines.append(content)
    return "\n".join(lines)

# --- Main Processing ---
############################
################################

json_file_path = './unified_skills.json' # Make sure this path is correct

if not os.path.exists(json_file_path):
    print(f"Error: Lesson data JSON file not found at {json_file_path}. Please ensure it exists.")
    exit()


################################################
################################################
#All skills are processed in a loop
with open(json_file_path, 'r', encoding='utf-8') as f:
    lessons_data = json.load(f)
    
    lessons_data = lessons_data[ :1]
    

for lesson in lessons_data:
    print(f"--- Lesson ID: {lesson['id']} ---")
    print(f"--- Lesson Description: {lesson['skill_name']} ---")
    print(f"{lesson['description']}\n")

    print("### Basic Question Examples: (Ignore if Khan Academy or EngageNY questions are available)")
    for q in lesson['basic_questions_example']:
        print(f"- {q}")

    print("\n---")
    print(f"Difficulty: {lesson['difficulty']} (Rating: {lesson['difficulty_rating']})")
    print(f"Common Pitfalls: {lesson['common_pitfalls']}")

    print("\n### Number of Questions:")
    for key, value in lesson["number_of_questions"].items():
        print(f"{key}: {value}")
    
    print("\n---")
    # Retrieve Khan Academy questions
    khan_academy_topic = lesson.get('khan_academy_topic')
    for khan_academy_topic in lesson.get('sources', {}).get('Khan Academy', []):
        khan_academy_file_path = get_khan_academy_filepath(khan_academy_topic)

        if khan_academy_file_path:
            print(f"\n## Khan Academy Relevant Questions: {khan_academy_topic}")
            try:
                with open(khan_academy_file_path, "r", encoding="utf8") as json_file:
                    data = json.load(json_file)
                    structured_questions = []

                    for item in data.get("items", []):
                        try:
                            ai = item["data"]["assessmentItem"]["item"]
                            question_data = ai["itemData"]["question"]
                            hints_data = ai["itemData"]["hints"]
                            problem_type = ai.get("problemType", "Unknown")

                            question_content = remove_placeholder_tags(question_data["content"])
                            question_images = question_data.get("images", [])
                            question_image_alts = [img.get("alt", "").strip() for img in question_images if "alt" in img]
                            question_has_images = bool(question_images)

                            hints = []
                            hint_has_images = False
                            for hint in hints_data:
                                cleaned_hint = {
                                    "content": remove_placeholder_tags(hint["content"])
                                }
                                if hint.get("images"):
                                    hint_has_images = True
                                    if hint["images"]:
                                        alt = hint["images"][0].get("alt", "").strip()
                                        if alt:
                                            cleaned_hint["alt"] = alt
                                hints.append(cleaned_hint)

                            has_image = question_has_images or hint_has_images

                            structured_questions.append({
                                "problemType": problem_type,
                                "question": question_content,
                                "hasImage": has_image,
                                "options": question_data.get("options", []),
                                "hints": hints,
                                "imageAlts": question_image_alts
                            })

                        except Exception as e:
                            print(f"Error processing a Khan Academy item: {e}")
                            continue

                    for q in structured_questions[:5]:
                        print(format_khan_academy_question(q))
            except FileNotFoundError:
                print(f"Khan Academy questions file not found at: {khan_academy_file_path}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON from Khan Academy file: {khan_academy_file_path}. Check file format.")
            except Exception as e:
                print(f"An unexpected error occurred while reading Khan Academy file: {e}")
        else:
            print(f"\nNo Khan Academy questions file path found for: {khan_academy_topic}")
     

    # Retrieve EngageNY lesson content based on sources
    engageny_sources = lesson.get('sources', {}).get('EngageNY', [])
    if engageny_sources:
        print("\n## EngageNY Relevant Lesson Content:")
        for source_topic in engageny_sources:
            # Extract grade from common_core_id
            engageny_grade = None
            if lesson.get('common_core_id') and lesson['common_core_id'][0].isdigit():
                engageny_grade = int(lesson['common_core_id'][0])
            
            module_match = re.search(r'Module (\d+)', source_topic, re.IGNORECASE)
            lesson_match = re.search(r'Lesson (\d+)', source_topic, re.IGNORECASE)

            if engageny_grade is not None and module_match and lesson_match:
                engageny_module = int(module_match.group(1))
                engageny_lesson = int(lesson_match.group(1))
                
                engageny_file_path = get_engageny_filepath(engageny_grade, engageny_module, engageny_lesson)

                if engageny_file_path:
                    try:
                        with open(engageny_file_path, 'r', encoding='utf-8') as md_file:
                            engageny_content = md_file.read()
                            print(format_engageny_lesson_content(source_topic, engageny_content))
                    except FileNotFoundError:
                        print(f"EngageNY file not found for '{source_topic}' at: {engageny_file_path}")
                    except Exception as e:
                        print(f"Error reading EngageNY file for '{source_topic}': {e}")
                else:
                    print(f"No EngageNY lesson file found for '{source_topic}' (Grade {engageny_grade}, Module {engageny_module}, Lesson {engageny_lesson})")
            else:
                print(f"Could not extract Grade, Module, and/or Lesson from EngageNY source topic: '{source_topic}'. Please ensure the source string contains 'Module X' and 'Lesson Y' and the common core ID has a leading digit for the grade.")
    else:
        print("\nNo EngageNY sources listed for this lesson.")

    # Add the relationship at the end
    print(f"\n--- Relationship: {lesson.get('relationship', 'N/A')} ---")
    print("\n" + "="*80 + "\n") # Separator for multiple lessons