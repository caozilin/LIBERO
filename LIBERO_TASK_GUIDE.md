# Libero 任务修改指南

本文档说明如何在 Libero 中新建或修改任务套件。

---

## 快速开始

### 1. 编辑配置文件

编辑 `scripts/suite_config.json`：

```json
{
    "suite_name": "your_suite_name",
    "suite_description": "任务套件描述",
    "tasks": [
        {
            "language": "pick up the milk and put it in the basket",
            "scene_name": "test_scene1",
            "objects_of_interest": ["milk_1", "basket_1"],
            "goal_states": [["In", "milk_1", "basket_1_contain_region"]]
        }
    ]
}
```

### 2. 运行脚本

**注意**：需要先激活虚拟环境（在 openpi 的 example libero 目录中）：

```bash
cd /path/to/openpi/examples/libero
source .venv/bin/activate

cd /path/to/libero
python scripts/setup_suite.py
```

### 3. 手动修改 Python 文件

根据脚本输出，手动修改以下文件。

---

## 完整流程

### 步骤 1：定义场景（mu_creation.py）

**文件位置**：`libero/libero/benchmark/mu_creation.py`

```python
@register_mu(scene_type="your_scene_type")
class YourScene1(InitialSceneTemplates):
    def __init__(self):
        fixture_num_info = {
            "table": 1,  # 使用 "table"，会自动映射为 "main_table"
        }

        object_num_info = {
            "milk": 1,
            "basket": 1,
        }

        super().__init__(
            workspace_name="main_table",
            fixture_num_info=fixture_num_info,
            object_num_info=object_num_info,
        )

    def define_regions(self):
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, 0.25],
                region_name="basket_init_region",
                target_name=self.workspace_name,
                region_half_len=0.01,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, -0.10],
                region_name="milk_init_region",
                target_name=self.workspace_name,
                region_half_len=0.025,
            )
        )
        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(
            self.regions
        )

    @property
    def init_states(self):
        states = [
            ("On", "milk_1", "main_table_milk_init_region"),
            ("On", "basket_1", "main_table_basket_init_region"),
        ]
        return states
```

**注意事项**：
- `fixture_num_info` 中的 key 是 fixture **类型**（如 `"table"`），会通过 `object_naming_mapping` 映射为具体名称（`"table"` → `"main_table"`）
- `workspace_name` 是 workspace **名称**，用于选择 BDDL 生成器，必须是预定义值之一
- 两者需要对应：`fixture_num_info = {"table": 1}` + `workspace_name = "main_table"`
- `init_states` 中的区域名格式：`{workspace_name}_{region_name}`

---

### 步骤 2：注册 Benchmark（benchmark/__init__.py）

**文件位置**：`libero/libero/benchmark/__init__.py`

#### 2.1 添加到 `libero_suites` 列表

```python
libero_suites = [
    "your_suite_name",  # 添加到这里
    "libero_organize",
    ...
]
```

#### 2.2 添加 Benchmark 类

```python
@register_benchmark
class YOUR_SUITE_NAME(Benchmark):
    def __init__(self, task_order_index=0):
        super().__init__(task_order_index=task_order_index)
        self.name = "your_suite_name"
        self._make_benchmark()
```

---

### 步骤 3：添加任务映射（libero_suite_task_map.py）

**文件位置**：`libero/libero/benchmark/libero_suite_task_map.py`

```python
libero_task_map = {
    "your_suite_name": [
        "YOUR_SCENE1_pick_up_the_milk_and_put_it_in_the_basket",
    ],
    ...
}
```

**任务名格式**：`{SCENE_NAME}_{language_with_underscores}`

---

### 步骤 4：编辑配置并运行脚本

编辑 `scripts/suite_config.json`，然后运行：

```bash
python scripts/setup_suite.py
```

脚本会自动生成：
- BDDL 文件：`bddl_files/{suite_name}/`
- 初始状态文件：`init_files/{suite_name}/`

---

## 可用 workspace

| workspace_name | 说明 |
|----------------|------|
| `main_table` | 主桌面 |
| `kitchen_table` | 厨房桌面 |
| `living_room_table` | 客厅桌面 |
| `study_table` | 书房桌面 |
| `coffee_table` | 咖啡桌 |

---

## 可用物体

参见 `available_objects_list.txt`。

---

## 物体旋转设置

### 旋转属性说明

物体的初始旋转由物体类中的 `rotation` 和 `rotation_axis` 属性控制。

**文件位置**：
- `libero/libero/envs/objects/hope_objects.py` - HOPE 数据集物体（食品罐头等）
- `libero/libero/envs/objects/google_scanned_objects.py` - Google 扫描物体（碗、盘子等）

### 旋转属性详解

```python
class SomeObject(HopeBaseObject):
    def __init__(self, name="some_object", obj_name="some_object"):
        super().__init__(name, obj_name)
        self.rotation = (np.pi / 2, np.pi / 2)  # 旋转角度范围 (min, max)
        self.rotation_axis = "z"                 # 旋转轴：'x', 'y', 'z' 或 None
```

#### 旋转轴说明

| rotation_axis | 说明 |
|---------------|------|
| `"x"` | 绕 X 轴旋转 |
| `"y"` | 绕 Y 轴旋转 |
| `"z"` | 绕 Z 轴旋转（最常用，水平旋转） |
| `None` | 多轴旋转，使用字典定义 |

#### 常见旋转配置

**1. 站立的罐头（默认）**
```python
self.rotation = (np.pi / 2, np.pi / 2)  # 固定角度
self.rotation_axis = "z"                 # 只绕 Z 轴旋转（水平方向随机）
```

**2. 躺着的物体（如 butter, chocolate_pudding）**
```python
self.rotation = (0.0, 0.0)  # 不旋转，保持水平
self.rotation_axis = "x"
```

**3. 多轴旋转（如 milk, ketchup）**
```python
self.rotation = {
    "x": (np.pi / 2, np.pi / 2),  # X 轴旋转 90 度（躺下）
    "z": (0.0, 2 * np.pi),         # Z 轴随机旋转
}
self.rotation_axis = None  # 使用字典时设为 None
```

### 创建自定义旋转物体

如果需要特定旋转的物体，可以创建新的物体类：

```python
@register_object
class LyingAlphabetSoup(HopeBaseObject):
    """躺着的字母汤罐头"""
    def __init__(self, name="lying_alphabet_soup", obj_name="alphabet_soup"):
        super().__init__(name, obj_name)
        self.rotation = {
            "x": (np.pi / 2, np.pi / 2),  # 绕 X 轴旋转 90 度（躺下）
            "z": (0.0, 2 * np.pi),         # Z 轴随机旋转
        }
        self.rotation_axis = None
```

**注意**：
- `obj_name` 指向实际的模型文件目录
- `name` 是场景中的物体名称
- 注册后可在 `object_num_info` 中使用 `"lying_alphabet_soup": 1`

### 在场景中使用自定义物体

```python
object_num_info = {
    "lying_alphabet_soup": 1,  # 使用躺着的罐头
    "basket": 1,
}
```

---

## 初始状态谓词

### 可用谓词

| 谓词 | 格式 | 说明 |
|------|------|------|
| `On` | `("On", "object", "region")` | 物体放置在区域上 |
| `In` | `("In", "object", "contain_region")` | 物体放入容器区域 |
| `Open` | `("Open", "articulated_object")` | 打开可关节物体（抽屉、微波炉等） |
| `Close` | `("Close", "articulated_object")` | 关闭可关节物体 |
| `Turnon` | `("Turnon", "stove")` | 打开炉灶 |
| `Turnoff` | `("Turnoff", "stove")` | 关闭炉灶 |

### 示例

```python
@property
def init_states(self):
    states = [
        ("On", "milk_1", "main_table_milk_init_region"),
        ("On", "basket_1", "main_table_basket_init_region"),
        ("Open", "microwave_1"),  # 微波炉初始打开
    ]
    return states
```

---

## 常见问题

### Q: BDDL 生成失败

检查：
1. `scene_name` 是否与 `mu_creation.py` 中的类名对应（小写下划线格式）
2. `objects_of_interest` 中的物体是否在场景中定义
3. `workspace_name` 是否正确

### Q: 初始状态生成失败

检查：
1. BDDL 文件是否正确生成
2. 场景中的物体和区域定义是否匹配

### Q: 任务数量不为 10

代码已自动处理，直接使用原始顺序。

---

## 文件结构

```
libero/
├── libero/
│   └── libero/
│       ├── benchmark/
│       │   ├── __init__.py              # Benchmark 注册
│       │   ├── libero_suite_task_map.py # 任务映射
│       │   └── mu_creation.py           # 场景定义
│       ├── bddl_files/
│       │   └── {suite_name}/            # BDDL 文件（自动生成）
│       └── init_files/
│           └── {suite_name}/            # 初始状态文件（自动生成）
├── scripts/
│   ├── suite_config.json                # 任务配置
│   └── setup_suite.py                   # 生成脚本
└── available_objects_list.txt           # 可用物体列表
```
