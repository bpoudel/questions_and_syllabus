import json

def update_skills_json(first_json_path, second_json_path, output_json_path):
    """
    Updates the first JSON file with information from the second JSON file,
    including the position of each skill within its sub-cluster.

    Args:
        first_json_path (str): The file path to the first JSON (list of skills).
        second_json_path (str): The file path to the second JSON (revised skill list by topics).
        output_json_path (str): The file path where the updated JSON will be saved.
    """
    try:
        # Load the first JSON file
        with open(first_json_path, 'r') as f:
            first_json_data = json.load(f)

        # Load the second JSON file
        with open(second_json_path, 'r') as f:
            second_json_data = json.load(f)

    except FileNotFoundError as e:
        print(f"Error: One of the JSON files was not found. Please check the paths. {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON. Please check file content. {e}")
        return

    # Create a dictionary for quick lookup from the second JSON
    # The key will be the skill_description for matching
    second_json_lookup = {}
    for unit in second_json_data:
        unit_order = unit.get('unit_order')
        unit_name = unit.get('unit_name')
        for cluster in unit.get('clusters', []):
            cluster_order_within_unit = cluster.get('cluster_order_within_unit')
            cluster_name = cluster.get('cluster_name')
            for sub_cluster in cluster.get('sub_clusters', []):
                sub_cluster_order_within_cluster = sub_cluster.get('sub_cluster_order_within_cluster')
                sub_cluster_name = sub_cluster.get('sub_cluster_name')
                
                # Enumerate skills to get their position within the sub_cluster
                for i, skill_in_subcluster in enumerate(sub_cluster.get('skills', [])):
                    skill_description = skill_in_subcluster.get('skill_description')
                    if skill_description:
                        second_json_lookup[skill_description] = {
                            'skill_id_new': skill_in_subcluster.get('skill_id'),
                            'standard_id': skill_in_subcluster.get('standard_id'),
                            'unit_order': unit_order,
                            'unit_name': unit_name,
                            'cluster_order_within_unit': cluster_order_within_unit,
                            'cluster_name': cluster_name,
                            'sub_cluster_order_within_cluster': sub_cluster_order_within_cluster,
                            'sub_cluster_name': sub_cluster_name,
                            'position_within_subcluster': i + 1 # 1-based index for progression
                        }

    # Update the first JSON data
    updated_skills_list = []
    for skill in first_json_data:
        skill_description = skill.get('skill_name')
        if skill_description and skill_description in second_json_lookup:
            matched_info = second_json_lookup[skill_description]

            # Update 'id' by combining standard_id and skill_id from the second JSON
            new_id = f"{matched_info.get('standard_id')}_{matched_info.get('skill_id_new')}"
            skill['id'] = new_id

            # Add/Update other fields from the second JSON
            skill['unit_order'] = matched_info.get('unit_order')
            skill['unit_name'] = matched_info.get('unit_name')
            skill['cluster_order_within_unit'] = matched_info.get('cluster_order_within_unit')
            skill['cluster_name'] = matched_info.get('cluster_name')
            skill['sub_cluster_order_within_cluster'] = matched_info.get('sub_cluster_order_within_cluster')
            skill['sub_cluster_name'] = matched_info.get('sub_cluster_name')
            skill['position_within_subcluster'] = matched_info.get('position_within_subcluster')
        updated_skills_list.append(skill)

    # Save the updated JSON to a new file
    with open(output_json_path, 'w') as f:
        json.dump(updated_skills_list, f, indent=4)

    print(f"Updated JSON saved to {output_json_path}")


# --- How to use the script ---
# Make sure your first JSON is named 'first_json.json'
# and your second JSON is named 'second_json.json'
# in the same directory as this script, or provide their full paths.
# The updated JSON will be saved as 'updated_first_json.json'.
update_skills_json('modified_first.json', 'files1.json', 'updated_first_json.json')