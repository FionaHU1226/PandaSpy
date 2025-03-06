import streamlit as st
import pandas as pd
from streamlit_ace import st_ace  # 更好看的代码编辑器组件
import utils.validator as validator
import utils.data_loader as data_loader

def run_task():
    st.header("🔍 金融诈骗调查 - 任务 1")
    
    # 初始化部分 session_state 变量，确保后续步骤不会因未定义而报错
    if "suspicious_transactions" not in st.session_state:
        st.session_state.suspicious_transactions = None
    if "suspicious_totals" not in st.session_state:
        st.session_state.suspicious_totals = None

    st.markdown("""
    你是一名 PandaSpy 侦探，负责调查一起洗钱案。银行提供了一份交易记录，你的任务是：
    1️⃣ **加载数据**
    2️⃣ **探索数据**
    3️⃣ **筛选大额交易**
    4️⃣ **找出嫌疑账户**
    5️⃣ **统计嫌疑账户交易金额**
    6️⃣ **最终锁定罪犯**
    """)

    # 载入数据
    df = data_loader.load_transactions()

    ### 第一步：加载数据
    st.subheader("📌 第一步：加载数据")
    st.markdown("请使用 pandas 读取交易数据，并显示前 5 行。")
    with st.expander("💡 提示"):
        st.info("你可以使用 pd.read_csv('data/transactions.csv') 来加载数据。")

    if "step1_code" not in st.session_state:
        st.session_state.step1_code = (
            "import pandas as pd\n\n"
            "# 示例代码\n"
            "df = pd.read_csv('data/transactions.csv')\n"
            "df.head()"
        )
    user_code_1 = st_ace(value=st.session_state.step1_code, language='python', key="step1_code")
    
    if st.button("🚀 运行代码", key="step1_run"):
        result, message = validator.validate_task_1_step1(user_code_1, df)
        if result:
            st.success("✅ 正确！数据加载成功！")
            st.session_state.step1_completed = True
        else:
            st.error(f"❌ {message}")

    if st.session_state.get("step1_completed", False):
        st.dataframe(df.head())

    ### 第二步：探索数据
    if st.session_state.get("step1_completed", False):
        st.subheader("📌 第二步：探索数据")
        st.markdown("使用 .info() 和 .describe() 检查数据类型和统计信息。")
        with st.expander("💡 提示"):
            st.info("试试 df.info() 和 df.describe()。")
        
        if "step2_code" not in st.session_state:
            st.session_state.step2_code = "df.info()\ndf.describe()"
        user_code_2 = st_ace(value=st.session_state.step2_code, language='python', key="step2_code")
        
        if st.button("🚀 运行代码", key="step2_run"):
            result, message = validator.validate_task_1_step2(user_code_2, df)
            if result:
                st.success("✅ 正确！你已经了解数据结构！")
                st.session_state.step2_completed = True
            else:
                st.error(f"❌ {message}")

    if st.session_state.get("step2_completed", False):
        st.write("📊 **数据结构分析 (.info())**")
        # 注意：df.info() 输出信息只能用 text() 显示
        st.text(df.info())
        st.write("📊 **数据统计 (.describe())**")
        st.dataframe(df.describe())

    ### 第三步：筛选大额交易
    if st.session_state.get("step2_completed", False):
        st.subheader("📌 第三步：筛选大额交易")
        st.markdown("请找出 **金额大于 10000** 的交易，并存入 suspicious_transactions 变量。")
        with st.expander("💡 提示"):
            st.info("你可以使用 df[df['amount'] > 10000] 筛选大额交易。")
        
        if "step3_code" not in st.session_state:
            st.session_state.step3_code = (
                "suspicious_transactions = df[df['amount'] > 10000]\n"
                "suspicious_transactions"
            )
        user_code_3 = st_ace(value=st.session_state.step3_code, language='python', key="step3_code")
        
        if st.button("🚀 运行代码", key="step3_run"):
            result, message = validator.validate_task_1_step3(user_code_3, df)
            if result:
                st.success("✅ 你找到了大额交易！")
                st.session_state.suspicious_transactions = message
                st.session_state.step3_completed = True
            else:
                st.error(f"❌ {message}")

    if st.session_state.get("step3_completed", False):
        st.dataframe(st.session_state.suspicious_transactions)

    ### 第四步：找出嫌疑账户
    if st.session_state.get("step3_completed", False):
        st.subheader("📌 第四步：找出嫌疑账户")
        st.markdown("请找出涉及大额交易的账户（发送者）。")
        with st.expander("💡 提示"):
            st.info("试试 suspicious_transactions['sender'].unique()。")
        
        if "step4_code" not in st.session_state:
            st.session_state.step4_code = (
                "suspicious_accounts = suspicious_transactions['sender'].unique()\n"
                "suspicious_accounts"
            )
        user_code_4 = st_ace(value=st.session_state.step4_code, language='python', key="step4_code")
        
        if st.button("🚀 运行代码", key="step4_run"):
            if st.session_state.suspicious_transactions is not None:
                result, message = validator.validate_task_1_step4(user_code_4, st.session_state.suspicious_transactions)
                if result:
                    st.success("🏆 恭喜！你锁定了嫌疑账户！")
                    st.dataframe(message)
                    st.session_state.step4_completed = True
                else:
                    st.error(f"❌ {message}")
            else:
                st.error("⚠️ 你需要先完成第三步！")

    ### 第五步：统计嫌疑账户交易金额
    if st.session_state.get("step4_completed", False):
        st.subheader("📌 第五步：统计嫌疑账户交易金额")
        st.markdown("请计算每个嫌疑账户的交易总金额，以便进一步缩小范围。")
        with st.expander("💡 提示"):
            st.info("你可以使用 groupby 聚合，例如： suspicious_totals = suspicious_transactions.groupby('sender')['amount'].sum()")
        
        if "step5_code" not in st.session_state:
            st.session_state.step5_code = (
                "suspicious_totals = suspicious_transactions.groupby('sender')['amount'].sum()\n"
                "suspicious_totals"
            )
        user_code_5 = st_ace(value=st.session_state.step5_code, language='python', key="step5_code")
        
        if st.button("🚀 运行代码", key="step5_run"):
            result, message = validator.validate_task_1_step5(user_code_5, st.session_state.suspicious_transactions)
            if result:
                st.success("✅ 计算完成！")
                # 以表格方式展示每个账户的总金额
                st.dataframe(message.reset_index())
                st.session_state.suspicious_totals = message
                st.session_state.step5_completed = True
            else:
                st.error(f"❌ {message}")

    ### 第六步：确定罪犯账户
    if st.session_state.get("step5_completed", False):
        st.subheader("📌 第六步：确定罪犯账户")
        st.markdown("请找出交易总金额最高的账户作为最终嫌疑对象。")
        with st.expander("💡 提示"):
            st.info("你可以使用 suspicious_totals.idxmax() 来找出金额最高的账户。")
        
        if "step6_code" not in st.session_state:
            st.session_state.step6_code = (
                "culprit = suspicious_totals.idxmax()\n"
                "culprit"
            )
        user_code_6 = st_ace(value=st.session_state.step6_code, language='python', key="step6_code")
        
        if st.button("🚀 运行代码", key="step6_run"):
            if st.session_state.suspicious_totals is not None:
                result, message = validator.validate_task_1_step6(user_code_6, st.session_state.suspicious_totals)
                if result:
                    st.success("🏆 找到最终嫌疑账户！")
                    st.write("罪犯账户为：", message)
                    st.session_state.step6_completed = True
                else:
                    st.error(f"❌ {message}")
            else:
                st.error("⚠️ 请先完成第五步！")
