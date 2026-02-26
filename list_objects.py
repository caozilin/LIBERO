from libero.libero.envs.objects import OBJECTS_DICT

# 列出所有可用物品名
object_names = list(OBJECTS_DICT.keys())

# 输出到txt文件
with open('available_objects.txt', 'w') as f:
    for obj_name in object_names:
        f.write(f"{obj_name}\n")

print(f"已将 {len(object_names)} 个物品名称输出到 available_objects.txt")
print("前10个物品:", object_names[:10])