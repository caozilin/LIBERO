#!/usr/bin/env python
"""
Universal setup script for Libero task suites.
Usage: python scripts/setup_suite.py [--config scripts/suite_config.json]
"""
import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
from libero.libero.utils.task_generation_utils import (
    register_task_info,
    generate_bddl_from_task_info,
)
from libero.libero import get_libero_path
from libero.libero.envs import OffScreenRenderEnv

from libero.libero.benchmark import mu_creation


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_bddl_files(config, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    for task in config["tasks"]:
        goal_states = [tuple(g) for g in task["goal_states"]]
        register_task_info(
            language=task["language"],
            scene_name=task["scene_name"],
            objects_of_interest=task["objects_of_interest"],
            goal_states=goal_states,
        )
    
    bddl_file_names, failures = generate_bddl_from_task_info(folder=output_folder)
    return bddl_file_names, failures


def generate_init_states(config, output_folder, num_init_states=10, resolution=128):
    os.makedirs(output_folder, exist_ok=True)
    
    suite_name = config["suite_name"]
    tasks = config["tasks"]
    
    for task in tasks:
        task_name = f"{task['scene_name'].upper()}_{task['language'].replace(' ', '_')}"
        bddl_file = os.path.join(
            get_libero_path("bddl_files"),
            suite_name,
            f"{task_name}.bddl",
        )
        
        if not os.path.exists(bddl_file):
            print(f"  [WARNING] BDDL file not found: {bddl_file}")
            continue
        
        try:
            env = OffScreenRenderEnv(
                bddl_file_name=bddl_file,
                camera_heights=resolution,
                camera_widths=resolution,
            )
            env.seed(0)
            
            init_states = []
            for i in range(num_init_states):
                env.reset()
                state = env.get_sim_state()
                init_states.append(state)
            
            init_states_file = f"{task_name}.pruned_init"
            save_path = os.path.join(output_folder, init_states_file)
            torch.save(init_states, save_path)
            print(f"  [OK] Saved {num_init_states} initial states: {init_states_file}")
            
            env.close()
        except Exception as e:
            print(f"  [ERROR] Failed for task '{task_name}': {e}")


def main():
    default_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "suite_config.json")
    parser = argparse.ArgumentParser(description="Setup Libero task suite from JSON config")
    parser.add_argument("--config", type=str, default=default_config, help="Path to JSON config file")
    parser.add_argument("--skip-init-states", action="store_true", help="Skip initial state generation")
    args = parser.parse_args()
    
    config_path = args.config
    config = load_config(config_path)
    
    suite_name = config["suite_name"]
    
    print(f"Setting up task suite: {suite_name}")
    
    bddl_output_folder = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "libero", "libero", "bddl_files", suite_name
    )
    
    init_states_output_folder = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "libero", "libero", "init_files", suite_name
    )
    
    print(f"[Step 1/2] Generating BDDL files...")
    bddl_file_names, failures = generate_bddl_files(config, bddl_output_folder)
    
    for f in bddl_file_names:
        print(f"  [OK] {os.path.basename(f)}")
    
    if failures:
        for scene, lang in failures:
            print(f"  [ERROR] {scene}: {lang}")
    
    if not args.skip_init_states:
        print(f"[Step 2/2] Generating initial state files...")
        generate_init_states(config, init_states_output_folder)
    else:
        print(f"[Step 2/2] Skipping initial state generation")
    
    print(f"Done: {suite_name}")


if __name__ == "__main__":
    main()
