import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from .prompts import SYSTEM_PROMPT, OPTIMIZE_PROMPT
from .schema import Resume

load_dotenv()


def _get_api_key() -> str:
    key = os.getenv("DEEPSEEK_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        key = st.secrets.get("DEEPSEEK_API_KEY")
        if key:
            return key
    except ImportError:
        pass
    raise ValueError("DEEPSEEK_API_KEY not found. Set it in .env or Streamlit secrets.")


def _get_client() -> OpenAI:
    return OpenAI(
        api_key=_get_api_key(),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    )


def parse_to_resume(natural_input: str) -> Resume:
    """将自然语言描述解析为结构化简历数据"""
    client = _get_client()

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": natural_input},
        ],
        response_format={"type": "json_object"},
    )

    raw = resp.choices[0].message.content
    return Resume.model_validate_json(raw)


def optimize_resume(resume: Resume, request: str) -> Resume:
    """根据用户要求优化简历"""
    client = _get_client()

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"当前简历 JSON:\n{resume.model_dump_json(indent=2, ensure_ascii=False)}",
            },
            {
                "role": "user",
                "content": OPTIMIZE_PROMPT.format(request=request),
            },
        ],
        response_format={"type": "json_object"},
    )

    raw = resp.choices[0].message.content
    return Resume.model_validate_json(raw)
