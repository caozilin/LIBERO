"""
Setup script for libero_organize task suite.
Runs BDDL generation and initial state generation in sequence.
Usage: python scripts/setup_libero_organize.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    print("=" * 60)
    print("LIBERO_ORGANIZE Task Suite Setup")
    print("=" * 60)

    # Step 1: Generate BDDL files
    print("\n[Step 1/3] Generating BDDL files...")
    from generate_libero_organize_bddl import main as generate_bddl
    bddl_file_names, failures, tasks, output_folder = generate_bddl()

    # Step 2: Update libero_suite_task_map.py
    print("\n[Step 2/3] Updating libero_suite_task_map.py...")
    task_map_names = []
    for task in tasks:
        task_map_names.append(f"{task['scene_name'].upper()}_{task['language'].replace(' ', '_')}")

    map_filepath = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "libero", "libero", "benchmark", "libero_suite_task_map.py"
    )
    with open(map_filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    in_organize = False
    skip_lines = False
    for line in lines:
        if '"libero_organize": [' in line:
            new_lines.append(line)
            for name in task_map_names:
                new_lines.append(f'        "{name}",')
            in_organize = True
            skip_lines = True
        elif in_organize and '],' in line:
            new_lines.append(line)
            in_organize = False
            skip_lines = False
        elif not skip_lines:
            new_lines.append(line)

    with open(map_filepath, "w", encoding="utf-8") as f:
        f.write('\n'.join(new_lines))

    # Step 3: Generate initial states
    print("\n[Step 3/3] Generating initial state files...")
    from generate_libero_organize_init_states import main as generate_init_states
    generate_init_states()

    print(f"\n{'='*60}")
    print(f"Generated {len(bddl_file_names)} BDDL files:")
    for f in bddl_file_names:
        print(f"  - {os.path.basename(f)}")
    print(f"\nSuccessfully auto-updated libero_suite_task_map.py with {len(task_map_names)} tasks!")
    
    if failures:
        print(f"\nFailed to generate {len(failures)} tasks:")
        for scene, lang in failures:
            print(f"  - {scene}: {lang}")
    
    print(f"{'='*60}")
    print(f"Output folder: {output_folder}")

    print("\n" + "=" * 60)
    print("LIBERO_ORGANIZE setup complete!")
    print("=" * 60)
    print("\nTo use libero_organize in your code:")
    print("  from libero.libero import benchmark")
    print("  task_suite = benchmark.get_benchmark_dict()['libero_organize']()")
    print("\nTo run with OpenPI:")
    print("  python examples/libero/main.py --args.task-suite-name libero_organize")


if __name__ == "__main__":
    main()
