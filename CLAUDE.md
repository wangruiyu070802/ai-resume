# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

AI 简历生成器：用户用自然语言描述个人经历，DeepSeek LLM 解析成结构化 JSON（Pydantic 校验），再用 Jinja2 渲染成 HTML 简历。两个入口：CLI（`main.py`）和 Streamlit Web（`app.py`）。

## 运行命令

```bash
pip install -r requirements.txt          # 安装依赖

# 环境变量：复制 .env.example 为 .env，填入 DEEPSEEK_API_KEY
# DEEPSEEK_API_KEY=sk-...
# DEEPSEEK_BASE_URL=https://api.deepseek.com   # 可选，默认就是这个

python main.py                  # CLI：交互式输入
python main.py "我是..."        # CLI：直接传文本
streamlit run app.py            # Web 界面
```

注意：`main.py` 顶部 docstring 里的 `--optimize` 参数**并未实现**——`main()` 只是把 `sys.argv` 拼成文本，不解析 flag。别照着 docstring 假设它有这个开关。

## 架构与数据流

单向数据流：**自然语言文本 → LLM 解析 → `Resume`(Pydantic) → Jinja2 渲染 → HTML**

- `core/schema.py` — 唯一的数据契约。`Resume` 及子模型（`Experience`/`Education`/`Project`/`Skill`）的 Pydantic 定义。LLM 输出必须严格匹配这个结构，`model_validate_json` 对不上就抛异常。
- `core/prompts.py` — 两份提示词：`SYSTEM_PROMPT`（首次解析）和 `OPTIMIZE_PROMPT`（迭代优化），内嵌了 JSON 输出格式示例。
- `core/llm.py` — DeepSeek 调用封装。用 OpenAI SDK 指向 DeepSeek 的 base_url，模型固定 `deepseek-chat`，`response_format={"type": "json_object"}`。两个函数：`parse_to_resume()`、`optimize_resume()`。API key 读取优先级：`.env` 的 `DEEPSEEK_API_KEY` → Streamlit secrets。
- `core/generator.py` — 用 Jinja2 把 `Resume` 渲染成 `output/resume.html`。
- `templates/resume.html` — 简历 HTML 模板（纯静态 CSS，无 JS）。
- `main.py` — CLI 入口，交互式支持「生成后继续迭代优化」，中间态存 `output/resume.json`。
- `app.py` — Streamlit Web UI，三个 tab（生成/优化/预览），用 `session_state` 持有 `Resume` 和 HTML 路径。

## 关键约定

- 输出产物统一放 `output/`（已 gitignore）：CLI 存 `resume.json` + `resume.html`；Streamlit 存 HTML。
- 改简历结构要**同时改三处**：`core/schema.py` 的 Pydantic 模型 + `core/prompts.py` 里内嵌的 JSON 格式示例 + `templates/resume.html` 的渲染。漏一处，LLM 返回对不上 schema，或页面不显示。
- 没有测试、没有 lint 配置。改动后手动跑 `python main.py "..."` 验证一条链路即可。
- 需要 Python 3.10+（代码用了 `X | None` 类型标注语法）。
