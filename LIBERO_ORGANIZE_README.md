# LIBERO_ORGANIZE Task Suite

A custom task suite for the OpenPI project, built on top of LIBERO.

## Overview

LIBERO_ORGANIZE contains 5 tasks across 3 different scenes:

| Task ID | Scene | Description |
|---------|-------|-------------|
| 0 | OrgKitchenScene1 | Put the black bowl in the top drawer of the cabinet |
| 1 | OrgKitchenScene1 | Put the black bowl in the bottom drawer of the cabinet |
| 2 | OrgKitchenScene2 | Turn on the stove |
| 3 | OrgKitchenScene2 | Turn on the stove and put the moka pot on it |
| 4 | OrgLivingRoomScene1 | Put both the alphabet soup and the tomato sauce in the basket |

## Setup

Run the setup script to generate BDDL files and initial states:

```bash
cd third_party/libero
python scripts/setup_libero_organize.py
```

Or run steps individually:

```bash
# Step 1: Generate BDDL files
python scripts/generate_libero_organize_bddl.py

# Step 2: Generate initial states
python scripts/generate_libero_organize_init_states.py
```

## Usage

### Python API

```python
from libero.libero import benchmark, get_libero_path
from libero.libero.envs import OffScreenRenderEnv

# Get task suite
benchmark_dict = benchmark.get_benchmark_dict()
task_suite = benchmark_dict["libero_organize"]()

# Get task info
task = task_suite.get_task(0)
print(f"Task: {task.language}")

# Create environment
bddl_file = f"{get_libero_path('bddl_files')}/libero_organize/{task.bddl_file}"
env = OffScreenRenderEnv(bddl_file_name=bddl_file, camera_heights=128, camera_widths=128)
env.seed(0)
env.reset()

# Set initial state
init_states = task_suite.get_task_init_states(0)
env.set_init_state(init_states[0])

# Run episode
obs, reward, done, info = env.step(action)
```

### With OpenPI

```bash
# Terminal 1: Start policy server
python scripts/serve_policy.py --env LIBERO

# Terminal 2: Run evaluation
python examples/libero/main.py --args.task-suite-name libero_organize
```

## File Structure

```
third_party/libero/
├── libero/libero/
│   ├── benchmark/
│   │   ├── __init__.py          # Benchmark registration
│   │   ├── libero_suite_task_map.py  # Task name mapping
│   │   └── mu_creation.py       # Scene definitions
│   ├── bddl_files/
│   │   └── libero_organize/     # Generated BDDL files
│   └── init_files/
│       └── libero_organize/     # Generated initial states
└── scripts/
    ├── setup_libero_organize.py       # Full setup script
    ├── generate_libero_organize_bddl.py    # BDDL generation
    └── generate_libero_organize_init_states.py  # Initial state generation
```

## Adding New Tasks

1. **Define a new scene** in `libero/libero/benchmark/mu_creation.py`:

```python
@register_mu(scene_type="kitchen")
class OrgKitchenScene3(InitialSceneTemplates):
    def __init__(self):
        fixture_num_info = {...}
        object_num_info = {...}
        super().__init__(...)
    
    def define_regions(self):
        self.regions.update(...)
    
    @property
    def init_states(self):
        return [...]
```

2. **Register the task** in `scripts/generate_libero_organize_bddl.py`:

```python
register_task_info(
    language="your task description",
    scene_name="org_kitchen_scene3",
    objects_of_interest=["object_1", "object_2"],
    goal_states=[("On", "object_1", "target_region")],
)
```

3. **Add task name** to `libero/libero/benchmark/libero_suite_task_map.py`:

```python
"libero_organize": [
    ...,
    "ORG_KITCHEN_SCENE3_your_task_description",
],
```

4. **Regenerate files**:

```bash
python scripts/setup_libero_organize.py
```

## Available Objects

### Fixtures
- `kitchen_table`, `living_room_table`, `study_table`
- `white_cabinet`, `wooden_cabinet`
- `flat_stove`, `microwave`
- `wine_rack`, etc.

### Movable Objects
- `akita_black_bowl`, `white_bowl`, `plate`
- `alphabet_soup`, `tomato_sauce`, `cream_cheese`, `ketchup`, `butter`
- `moka_pot`, `frying_pan`
- `basket`, `wine_bottle`
- etc.

## Available Predicates

| Predicate | Usage |
|-----------|-------|
| `On` | Object on region |
| `In` | Object in region |
| `Open` | Region is open |
| `Close` | Region is closed |
| `TurnOn` | Device is on |
| `TurnOff` | Device is off |
