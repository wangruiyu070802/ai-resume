#!/usr/bin/env python3
"""AI Resume Generator — Streamlit Web 界面"""

import streamlit as st
from core.llm import parse_to_resume, optimize_resume
from core.generator import generate_html

st.set_page_config(page_title="AI 简历生成器", layout="centered")
st.title("AI 简历生成器")
st.markdown("用自然语言描述你的经历，AI 自动生成结构化简历。")

# 初始化 session state
if "resume" not in st.session_state:
    st.session_state.resume = None
if "html_path" not in st.session_state:
    st.session_state.html_path = None

tab1, tab2, tab3 = st.tabs(["生成简历", "优化简历", "预览"])

with tab1:
    st.subheader("描述你的经历")
    st.markdown("可以写教育背景、项目经历、技能、实习经历等，用自然语言就行。")

    input_text = st.text_area(
        "例如：我叫张三，是 XX 大学计算机系大一学生。学过 C 语言，做过一个贪吃蛇项目...",
        height=200,
        placeholder="请用自然语言描述你的个人经历...",
    )

    if st.button("生成简历", type="primary"):
        if not input_text.strip():
            st.warning("请先输入你的经历。")
        else:
            with st.spinner("AI 正在分析并生成简历..."):
                resume = parse_to_resume(input_text)
                html_path = generate_html(resume)
                st.session_state.resume = resume
                st.session_state.html_path = html_path
            st.success("简历生成完成！")
            st.json(resume.model_dump())

with tab2:
    st.subheader("优化简历")
    if st.session_state.resume is None:
        st.info("请先在「生成简历」标签页生成一份简历。")
    else:
        opt_request = st.text_input("优化要求（如：把项目经历写得更具体、增加量化数据）")
        if st.button("应用优化", type="primary"):
            if not opt_request.strip():
                st.warning("请输入优化要求。")
            else:
                with st.spinner("正在优化..."):
                    resume = optimize_resume(st.session_state.resume, opt_request)
                    html_path = generate_html(resume)
                    st.session_state.resume = resume
                    st.session_state.html_path = html_path
                st.success("优化完成！")
                st.json(resume.model_dump())

with tab3:
    st.subheader("预览简历")
    if st.session_state.html_path is None:
        st.info("请先生成一份简历。")
    else:
        with open(st.session_state.html_path, encoding="utf-8") as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=800, scrolling=True)

        with open(st.session_state.html_path, "rb") as f:
            st.download_button(
                label="下载简历 (HTML)",
                data=f,
                file_name="我的简历.html",
                mime="text/html",
            )
