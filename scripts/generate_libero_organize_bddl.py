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

    # Task 1: Open top drawer and put black bowl in it
    register_task_info(
        language="open the top drawer of the cabinet and put the black bowl in it",
        scene_name="org_kitchen_scene1",
        objects_of_interest=["akita_black_bowl_1", "white_cabinet_1"],
        goal_states=[
            ("Open", "white_cabinet_1_top_region"),
            ("In", "akita_black_bowl_1", "white_cabinet_1_top_region"),
        ],
    )

    # Task 2: Open bottom drawer and put black bowl in it
    register_task_info(
        language="open the bottom drawer of the cabinet and put the black bowl in it",
        scene_name="org_kitchen_scene1",
        objects_of_interest=["akita_black_bowl_1", "white_cabinet_1"],
        goal_states=[
            ("Open", "white_cabinet_1_bottom_region"),
            ("In", "akita_black_bowl_1", "white_cabinet_1_bottom_region"),
        ],
    )

    # Task 3: Turn on the stove
    register_task_info(
        language="turn on the stove",
        scene_name="org_kitchen_scene2",
        objects_of_interest=["flat_stove_1"],
        goal_states=[
            ("TurnOn", "flat_stove_1"),
        ],
    )

    # Task 4: Turn on stove and put moka pot on it
    register_task_info(
        language="turn on the stove and put the moka pot on it",
        scene_name="org_kitchen_scene2",
        objects_of_interest=["flat_stove_1", "moka_pot_1"],
        goal_states=[
            ("TurnOn", "flat_stove_1"),
            ("On", "moka_pot_1", "flat_stove_1_top_region"),
        ],
    )

    # Task 5: Put both alphabet soup and tomato sauce in basket
    register_task_info(
        language="put both the alphabet soup and the tomato sauce in the basket",
        scene_name="org_living_room_scene1",
        objects_of_interest=["alphabet_soup_1", "tomato_sauce_1", "basket_1"],
        goal_states=[
            ("In", "alphabet_soup_1", "basket_1_contain_region"),
            ("In", "tomato_sauce_1", "basket_1_contain_region"),
        ],
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


if __name__ == "__main__":
    main()
