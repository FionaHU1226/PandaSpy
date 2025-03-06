import pandas as pd

# **🟢 第一步：加载数据**
def validate_task_1_step1(user_code, df):
    try:
        local_vars = {}
        exec(user_code, {}, local_vars)

        if "df" not in local_vars:
            return False, "请确保变量名为 `df`！"

        user_df = local_vars["df"]
        if not isinstance(user_df, pd.DataFrame):
            return False, "`df` 不是 DataFrame，请检查 `pd.read_csv()` 语法！"

        return True, ""
    except Exception as e:
        return False, f"代码运行错误：{e}"

# **🟢 第二步：探索数据**
def validate_task_1_step2(user_code, df):
    try:
        local_vars = {"df": df}
        exec(user_code, {}, local_vars)

        return True, ""
    except Exception as e:
        return False, f"代码运行错误：{e}"

# **🟢 第三步：筛选大额交易**
def validate_task_1_step3(user_code, df):
    try:
        local_vars = {"df": df}
        exec(user_code, {}, local_vars)

        if "suspicious_transactions" not in local_vars:
            return False, "请确保变量名为 `suspicious_transactions`！"

        result_df = local_vars["suspicious_transactions"]
        expected_df = df[df["amount"] > 10000]

        if result_df.equals(expected_df):
            return True, result_df
        else:
            return False, "结果不正确，请检查筛选条件！"

    except Exception as e:
        return False, f"代码运行错误：{e}"

# **🟢 第四步：找出嫌疑账户**
def validate_task_1_step4(user_code, suspicious_transactions):
    try:
        # 将 suspicious_transactions 注入到执行环境中
        local_vars = {"suspicious_transactions": suspicious_transactions}
        exec(user_code, {}, local_vars)

        if "suspicious_accounts" not in local_vars:
            return False, "请确保变量名为 `suspicious_accounts`！"

        result_accounts = set(local_vars["suspicious_accounts"])
        expected_accounts = set(suspicious_transactions["sender"].unique())

        if result_accounts == expected_accounts:
            return True, local_vars["suspicious_accounts"]
        else:
            return False, "结果不正确，请检查 `unique()` 方法是否使用正确！"

    except Exception as e:
        return False, f"代码运行错误：{e}"

# **🟢 第五步：统计嫌疑账户交易金额**
def validate_task_1_step5(user_code, suspicious_transactions):
    try:
        local_vars = {"suspicious_transactions": suspicious_transactions}
        exec(user_code, {}, local_vars)

        if "suspicious_totals" not in local_vars:
            return False, "请确保变量名为 `suspicious_totals`！"

        result_totals = local_vars["suspicious_totals"]
        expected_totals = suspicious_transactions.groupby("sender")["amount"].sum()

        if isinstance(result_totals, pd.Series) and result_totals.equals(expected_totals):
            return True, result_totals
        else:
            return False, "结果不正确，请检查 groupby 和 sum() 是否正确使用！"
    except Exception as e:
        return False, f"代码运行错误：{e}"

# **🟢 第六步：确定罪犯账户**
def validate_task_1_step6(user_code, suspicious_totals):
    try:
        local_vars = {"suspicious_totals": suspicious_totals}
        exec(user_code, {}, local_vars)

        if "culprit" not in local_vars:
            return False, "请确保变量名为 `culprit`！"

        result_culprit = local_vars["culprit"]
        expected_culprit = suspicious_totals.idxmax()

        if result_culprit == expected_culprit:
            return True, result_culprit
        else:
            return False, "结果不正确，请检查 idxmax() 是否正确使用！"
    except Exception as e:
        return False, f"代码运行错误：{e}"
