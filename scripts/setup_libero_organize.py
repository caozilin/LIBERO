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
    print("\n[Step 1/2] Generating BDDL files...")
    from generate_libero_organize_bddl import main as generate_bddl
    generate_bddl()

    # Step 2: Generate initial states
    print("\n[Step 2/2] Generating initial state files...")
    from generate_libero_organize_init_states import main as generate_init_states
    generate_init_states()

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
