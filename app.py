import streamlit as st
import importlib
from config import TASKS

# 选择任务
st.title("🕵️‍♂️ PandaSpy: 编程解谜游戏")
task_choice = st.selectbox("选择一个任务", list(TASKS.keys()))

# 加载任务模块
task_module = importlib.import_module(f"tasks.{TASKS[task_choice]}")
task_module.run_task()
