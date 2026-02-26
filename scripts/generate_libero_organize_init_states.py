"""
Generate initial state files for libero_organize task suite.
Usage: python scripts/generate_libero_organize_init_states.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
from libero.libero import benchmark, get_libero_path
from libero.libero.envs import OffScreenRenderEnv


def main():
    benchmark_dict = benchmark.get_benchmark_dict()
    task_suite = benchmark_dict["libero_organize"]()
    num_tasks = task_suite.n_tasks

    print(f"Generating initial states for {num_tasks} tasks in libero_organize suite")
    print("=" * 60)

    output_folder = os.path.join(get_libero_path("init_states"), "libero_organize")
    os.makedirs(output_folder, exist_ok=True)

    num_init_states = 10
    resolution = 128

    for task_id in range(num_tasks):
        task = task_suite.get_task(task_id)
        print(f"\nTask {task_id + 1}/{num_tasks}: {task.name}")
        print(f"  Language: {task.language}")

        bddl_file = os.path.join(
            get_libero_path("bddl_files"),
            task.problem_folder,
            task.bddl_file,
        )

        if not os.path.exists(bddl_file):
            print(f"  [WARNING] BDDL file not found: {bddl_file}")
            print(f"  Please run generate_libero_organize_bddl.py first!")
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

            save_path = os.path.join(output_folder, task.init_states_file)
            torch.save(init_states, save_path)
            print(f"  [OK] Saved {num_init_states} initial states to: {save_path}")

            env.close()

        except Exception as e:
            print(f"  [ERROR] Failed to generate initial states: {e}")
            continue

    print("\n" + "=" * 60)
    print("Initial state generation complete!")
    print(f"Output folder: {output_folder}")


if __name__ == "__main__":
    main()
