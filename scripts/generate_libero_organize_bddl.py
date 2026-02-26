"""
Generate BDDL files for libero_organize task suite.
Usage: python scripts/generate_libero_organize_bddl.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libero.libero.utils.task_generation_utils import (
    register_task_info,
    generate_bddl_from_task_info,
)

# Import to register scene classes
from libero.libero.benchmark import mu_creation


def main():
    output_folder = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "libero", "libero", "bddl_files", "libero_organize"
    )
    os.makedirs(output_folder, exist_ok=True)

    # Load tasks from JSON config
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libero_organize_tasks.json")
    import json
    with open(config_path, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    for task in tasks:
        # Convert list of lists to list of tuples for goal_states
        goal_states = [tuple(g) for g in task["goal_states"]]
        register_task_info(
            language=task["language"],
            scene_name=task["scene_name"],
            objects_of_interest=task["objects_of_interest"],
            goal_states=goal_states,
        )

    bddl_file_names, failures = generate_bddl_from_task_info(folder=output_folder)

    print(f"\n{'='*60}")
    print(f"Generated {len(bddl_file_names)} BDDL files:")
    for f in bddl_file_names:
        print(f"  - {os.path.basename(f)}")
    
    if failures:
        print(f"\nFailed to generate {len(failures)} tasks:")
        for scene, lang in failures:
            print(f"  - {scene}: {lang}")
    
    print(f"{'='*60}")
    print(f"Output folder: {output_folder}")
    
    return bddl_file_names, failures, tasks, output_folder


if __name__ == "__main__":
    main()
