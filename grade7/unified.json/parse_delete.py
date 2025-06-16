import json
import sys
import argparse

total = set()

def extract_skill_info(file_path):
    """
    Reads a JSON file containing a list of skill objects and prints the 
    ID and skill name for each object.

    Args:
        file_path (str): The path to the JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("Error: JSON file should contain a list of skill objects.")
            return

        print(f"--- Extracting skills from {file_path} ---")
        for skill in data:
            # Check if the required keys exist in the dictionary
            if 'id' in skill and 'skill_name' in skill:
                skill_id = skill.get('id', 'N/A')
                skill_name = skill.get('skill_name', 'N/A')
                total.add(skill_id)
                print(f"ID: {skill_id}, Skill Name: {skill_name}")
            else:
                print(f"Warning: Skipping an item because it's missing 'id' or 'skill_name'. Item: {skill}")
        print(len(total))
        print("--- Extraction complete ---")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Set up argument parser to accept a filename from the command line

    # Call the function with the provided filename
    extract_skill_info("unified.json")

