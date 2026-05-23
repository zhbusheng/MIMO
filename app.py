import anthropic
import os
import sys

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    print("错误：未设置 ANTHROPIC_API_KEY 环境变量")
    print("请先运行：set ANTHROPIC_API_KEY=sk-ant-你的key")
    sys.exit(1)

client = anthropic.Anthropic(api_key=api_key)

print("=== AI 智能周报生成器 ===\n")
print("请输入本周工作内容（每条一行，输入空行结束）：")

lines = []
while True:
    try:
        line = input()
    except (EOFError, KeyboardInterrupt):
        print("\n已取消")
        sys.exit(0)
    if line == "":
        break
    lines.append(f"- {line}")

if not lines:
    print("未输入任何内容，已退出")
    sys.exit(0)

work_content = "\n".join(lines)

print("\n正在生成周报...\n")
print("-" * 40)

try:
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""请根据以下工作要点，生成一份专业的中文工作周报。

工作要点：
{work_content}

要求：
1. 格式：本周工作总结 / 工作亮点 / 下周计划
2. 语言专业、简洁
3. 适当扩充细节，体现工作价值""",
            }
        ],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

except anthropic.AuthenticationError:
    print("\n错误：API Key 无效，请检查 ANTHROPIC_API_KEY 是否正确")
    sys.exit(1)
except anthropic.RateLimitError:
    print("\n错误：请求频率过高，请稍后再试")
    sys.exit(1)
except anthropic.APIConnectionError:
    print("\n错误：网络连接失败，请检查网络")
    sys.exit(1)
except anthropic.APIError as e:
    print(f"\n错误：API 调用失败 ({e})")
    sys.exit(1)

print("\n" + "-" * 40)
print("\n周报生成完成！")
