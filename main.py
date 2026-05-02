#!/usr/bin/env python3
"""AI Resume Generator — CLI 版本

用法:
  python main.py                       # 交互式输入
  python main.py "我是..."             # 直接传入文本
  python main.py --optimize "改进点"   # 在已有简历上优化
"""

import sys
import json
from pathlib import Path

from core.llm import parse_to_resume, optimize_resume
from core.generator import generate_html
from core.schema import Resume


SAVE_FILE = Path(__file__).parent / "output" / "resume.json"


def _save_resume(resume: Resume):
    SAVE_FILE.parent.mkdir(exist_ok=True)
    SAVE_FILE.write_text(
        resume.model_dump_json(indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"  已保存: {SAVE_FILE}")


def _load_resume() -> Resume | None:
    if SAVE_FILE.exists():
        return Resume.model_validate_json(SAVE_FILE.read_text(encoding="utf-8"))
    return None


def interactive_mode():
    print("=" * 50)
    print("AI 简历生成器")
    print("输入你的个人经历，用自然语言描述即可")
    print("输入空行结束，输入 q 退出")
    print("=" * 50)

    lines = []
    print("\n请描述你的经历（教育、项目、技能等）：")
    while True:
        line = input("> ")
        if line.strip() == "":
            break
        if line.strip().lower() == "q":
            return
        lines.append(line)

    if not lines:
        print("没有输入，退出。")
        return

    text = "\n".join(lines)
    print("\n正在生成简历...")
    resume = parse_to_resume(text)
    _save_resume(resume)

    path = generate_html(resume)
    print(f"  简历已生成: {path}")

    # 支持迭代优化
    while True:
        print("\n--- 可以继续优化 ---")
        print("输入优化要求（如「把项目经历写得更有技术含量」），留空退出：")
        opt = input("> ").strip()
        if not opt:
            break
        print("正在优化...")
        resume = optimize_resume(resume, opt)
        _save_resume(resume)
        path = generate_html(resume, filename="resume.html")
        print(f"  优化完成: {path}")

    print(f"\n最终简历: {path}")
    print("   打开 HTML 文件即可预览")


def main():
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if text:
        resume = parse_to_resume(text)
        _save_resume(resume)
        path = generate_html(resume)
        print(f"简历已生成: {path}")
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
