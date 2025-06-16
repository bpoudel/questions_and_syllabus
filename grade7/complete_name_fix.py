import re

def find_all_missing_names(file_path):
    """Find ALL patterns where Description appears without a preceding Name line."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all Description lines and check what comes before them
    lines = content.split('\n')
    
    missing_patterns = []
    
    for i, line in enumerate(lines):
        if line.strip() == 'Description:':
            # Check the previous non-empty line
            prev_line_idx = i - 1
            while prev_line_idx >= 0 and not lines[prev_line_idx].strip():
                prev_line_idx -= 1
            
            if prev_line_idx >= 0:
                prev_line = lines[prev_line_idx].strip()
                
                # If previous line is not a Name line, we need to add one
                if not prev_line.startswith('Name:'):
                    # The skill title should be in prev_line
                    skill_title = prev_line
                    missing_patterns.append((i, skill_title, prev_line_idx))
    
    print(f"Found {len(missing_patterns)} Description lines missing preceding Name lines")
    
    if missing_patterns:
        print("\nExamples of missing Name lines:")
        for i, (desc_line_idx, skill_title, title_line_idx) in enumerate(missing_patterns[:10]):
            print(f"  Line {desc_line_idx}: '{skill_title}' needs Name line")
        if len(missing_patterns) > 10:
            print(f"  ... and {len(missing_patterns) - 10} more")
    
    return missing_patterns

def add_all_missing_names(file_path):
    """Add Name lines for ALL missing cases while preserving spacing."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all cases where we need to add Name lines
    # Look for any line followed directly by Description: where the line is not "Name:"
    
    # Pattern 1: Numbered skills without Name
    pattern1 = r'(\n+)(\d+\. [^\n]+)\n(Description:)'
    
    # Pattern 2: Any non-Name line followed by Description
    pattern2 = r'(\n+)([^\n]+)\n(Description:)'
    
    # First pass: numbered skills
    def replacement1(match):
        whitespace = match.group(1)
        skill_title = match.group(2)
        description = match.group(3)
        skill_name = re.sub(r'^\d+\. ', '', skill_title)
        return f"{whitespace}{skill_title}\nName: {skill_name}\n{description}"
    
    updated_content = re.sub(pattern1, replacement1, content)
    
    # Second pass: any remaining non-Name lines before Description
    def replacement2(match):
        whitespace = match.group(1)
        potential_title = match.group(2).strip()
        description = match.group(3)
        
        # Skip if this is already a Name line
        if potential_title.startswith('Name:'):
            return match.group(0)  # Return unchanged
        
        # Skip if this looks like question count info or other metadata
        skip_patterns = [
            'total number of questions',
            'concept / introduction',
            'practice no of questions',
            'challenging number',
            'application/word problem',
            'common pitfall avoidance',
            'introduced definitions:',
            'difficulty:'
        ]
        
        if any(pattern in potential_title.lower() for pattern in skip_patterns):
            return match.group(0)  # Return unchanged
        
        # This looks like a skill title that needs a Name line
        return f"{whitespace}{potential_title}\nName: {potential_title}\n{description}"
    
    # Apply second pattern but be very careful
    final_content = re.sub(pattern2, replacement2, updated_content)
    
    # Count changes
    original_names = len(re.findall(r'^Name:', content, re.MULTILINE))
    final_names = len(re.findall(r'^Name:', final_content, re.MULTILINE))
    added_names = final_names - original_names
    
    print(f"Original Name lines: {original_names}")
    print(f"Final Name lines: {final_names}")
    print(f"Added {added_names} Name lines")
    
    # Verify we now have matching counts
    desc_count = len(re.findall(r'^Description:', final_content, re.MULTILINE))
    print(f"Description lines: {desc_count}")
    
    if final_names == desc_count:
        print("✅ Success! All Description lines now have matching Name lines")
    else:
        print(f"⚠️  Still missing {desc_count - final_names} Name lines")
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    return added_names

if __name__ == "__main__":
    print("Finding and fixing ALL missing Name lines in Syllabus.txt...")
    
    # First, analyze what's missing
    missing_patterns = find_all_missing_names('inputsource/Syllabus.txt')
    
    if missing_patterns:
        print(f"\nAdding {len(missing_patterns)} missing Name lines...")
        added = add_all_missing_names('inputsource/Syllabus.txt')
        print(f"\n🎉 Complete! Added {added} Name lines to Syllabus.txt")
    else:
        print("\n✅ All skills already have Name lines!") 