"""
Day 4 Demo — 模块、文件读写、JSON、异常捕获
读取标签 JSON 文件并处理缺失字段和格式错误
"""
import json
from pathlib import Path


# ========== 1. 文件读写基础 ==========
print("=" * 40)
print("1. 文件读写")
print("=" * 40)

# 写文件
output_file = Path(__file__).parent / "demo_output.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("Day 4 学习笔记\n")
    f.write("文件读写很简单！\n")

# 读文件
with open(output_file, "r", encoding="utf-8") as f:
    content = f.read()
    print(f"写入并读取成功：{content.strip()}")
print()

# ========== 2. JSON 基础操作 ==========
print("=" * 40)
print("2. JSON 基础操作")
print("=" * 40)

# Python dict → JSON 字符串
label = {"name": "vip_user", "display_name": "VIP用户", "type": "behavior"}
json_str = json.dumps(label, ensure_ascii=False, indent=2)
print(f"dict → JSON 字符串:\n{json_str}")

# JSON 字符串 → Python dict
parsed = json.loads(json_str)
print(f"JSON 字符串 → dict: {parsed}")
print(f"标签名: {parsed['name']}")
print()

# ========== 3. 读取 JSON 文件 ==========
print("=" * 40)
print("3. 读取标签 JSON 文件")
print("=" * 40)


def load_labels(filepath: str) -> list:
    """读取并解析标签 JSON 文件"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            labels = json.load(f)
        print(f"成功加载 {len(labels)} 个标签")
        return labels
    except FileNotFoundError:
        print(f"错误：文件不存在 - {filepath}")
        return []
    except json.JSONDecodeError as e:
        print(f"错误：JSON 格式错误 - {e}")
        return []


def validate_label(label: dict) -> dict:
    """
    校验标签是否包含必需字段，缺失时提供默认值并打印警告。
    返回补全后的标签。
    """
    required_fields = {
        "name": "unknown",
        "display_name": "未命名",
        "type": "unclassified",
        "conditions": [],
    }

    for field, default in required_fields.items():
        if field not in label:
            print(f"  ⚠ 标签 '{label.get('name', '?')}' 缺少字段 '{field}'，使用默认值: {default}")
            label[field] = default

    return label


def print_labels(labels: list):
    """格式化打印所有标签"""
    print(f"\n共 {len(labels)} 个标签：")
    print("-" * 50)
    for i, label in enumerate(labels, 1):
        print(f"[{i}] {label['display_name']} ({label['name']})")
        print(f"    类型: {label['type']}")
        conditions = label.get("conditions", [])
        if conditions:
            for cond in conditions:
                print(f"    条件: {cond.get('field', '?')} {cond.get('op', '?')} {cond.get('value', '?')}")
        else:
            print(f"    条件: (无)")
        print()


# 加载标签
labels_file = Path(__file__).parent / "labels.json"
labels = load_labels(str(labels_file))

# 校验每个标签
print("\n校验标签字段：")
validated_labels = []
for label in labels:
    validated = validate_label(label)
    validated_labels.append(validated)

# 打印结果
print_labels(validated_labels)

# ========== 4. 异常捕获综合演示 ==========
print("=" * 40)
print("4. 异常捕获演示")
print("=" * 40)


def safe_read_json(filepath: str) -> dict | list | None:
    """安全读取 JSON 文件的通用函数"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  文件不存在: {filepath}")
    except json.JSONDecodeError as e:
        print(f"  JSON 解析失败: {e}")
    except PermissionError:
        print(f"  无权限读取: {filepath}")
    except Exception as e:
        print(f"  未知错误: {type(e).__name__}: {e}")
    return None


# 测试各种情况
print("正常文件:")
result = safe_read_json(str(labels_file))
print(f"  加载成功，共 {len(result)} 条记录\n")

print("不存在的文件:")
result = safe_read_json("not_exist.json")
print(f"  返回: {result}\n")

print("写入并读取一个 JSON 文件:")
test_data = {"message": "Hello JSON", "numbers": [1, 2, 3]}
test_file = Path(__file__).parent / "test_output.json"
with open(test_file, "w", encoding="utf-8") as f:
    json.dump(test_data, f, ensure_ascii=False, indent=2)

result = safe_read_json(str(test_file))
print(f"  读取结果: {result}")
