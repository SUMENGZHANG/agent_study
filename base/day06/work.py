"""
作业 1：命令行圈人条件生成器（必做）

编写 audience_generator.py 命令行工具，支持以下参数：

参数：
- --min-age / --max-age：年龄范围（int）
- --gender：性别，可选 male / female，非必填
- --city：城市，字符串，可传多个（nargs="+"）
- --vip：是否 VIP，布尔开关
- --logic：条件间逻辑，AND（默认）/ OR
- -o / --output：输出文件路径，不指定则打印到终端

输出格式：标准 JSON，包含 request_id（用 uuid 生成）、conditions 列表和 logic。

示例调用：
    python audience_generator.py --min-age 18 --max-age 35 --city hangzhou shanghai --vip --logic AND
"""
# TODO: 实现 audience_generator.py
# 提示：参考 demo.py 的结构，自己从头写一遍
# 1. 定义 Condition 和 AudienceRequest dataclass
# 2. 实现 build_conditions(args) 函数
# 3. 实现 create_parser() 函数
# 4. 实现 main() 函数
# 5. 用 if __name__ == "__main__": 调用 main()




def build_conditions(args):


def main():



"""
作业 2：从 JSON 文件读取并合并条件（选做）

支持 --label-file 参数读取 Day 4 的 labels.json，
将文件中的标签条件与命令行参数合并输出。

提示：
1. parser.add_argument("--label-file", type=str, help="标签 JSON 文件路径")
2. 读取并解析 labels.json（复用 Day 4/5 的 parse_label 逻辑）
3. 将文件中的条件与命令行参数生成的条件合并
4. 注意 JSON key 映射：field → field_name, type → label_type
"""
# TODO: 在 audience_generator.py 中添加 --label-file 参数支持


"""
作业 3：思考题（选做）

不看代码，口述以下问题（10 分钟）：

1. if __name__ == "__main__": 的作用是什么？不加会怎样？
2. argparse 的 action="store_true" 和 type=bool 有什么区别？
3. Python 的 json.dumps() 和 Java 的 ObjectMapper 在使用上有什么不同？
"""
