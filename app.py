import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="Obfuscation Dashboard", layout="wide")

st.title("🚀 Software Obfuscation Analyzer")
st.markdown("### Compare performance before and after obfuscation")

# 🔹 simple obfuscation
def obfuscate_code(code):
    return "# obfuscated\n" + code

results = []

# 🔹 OPTION SELECTOR
option = st.radio(
    "Choose Input Method:",
    ["Use Existing Files (files folder)", "Upload Files"]
)

# 🔹 COMMON FUNCTION (core logic)
def process_code(name, code):
    # BEFORE
    start = time.time()
    try:
        exec(code)
        before_status = "Success"
    except:
        before_status = "Failed"
    end = time.time()

    before_time = end - start
    before_size = len(code)

    # AFTER
    new_code = obfuscate_code(code)

    start = time.time()
    try:
        exec(new_code)
        after_status = "Success"
    except:
        after_status = "Failed"
    end = time.time()

    after_time = end - start
    after_size = len(new_code)

    return {
        "File": name,
        "Before Time (sec)": round(before_time, 4),
        "After Time (sec)": round(after_time, 4),
        "Before Size (KB)": round(before_size / 1024, 2),
        "After Size (KB)": round(after_size / 1024, 2),
        "Before Status": before_status,
        "After Status": after_status
    }

# 🟢 OPTION 1: FILES FROM FOLDER
if option == "Use Existing Files (files folder)":
    folder = "files"

    if st.button("Run Analysis on Folder"):
        if not os.path.exists(folder):
            st.error("❌ 'files' folder not found!")
        else:
            for filename in os.listdir(folder):
                if filename.endswith(".py"):
                    path = os.path.join(folder, filename)
                    with open(path, "r") as f:
                        code = f.read()

                    results.append(process_code(filename, code))

# 🟣 OPTION 2: UPLOAD FILES
elif option == "Upload Files":
    uploaded_files = st.file_uploader(
        "Upload Python files",
        type=["py"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            code = file.read().decode("utf-8")
            results.append(process_code(file.name, code))

# 🔹 SHOW RESULTS
if results:
    df = pd.DataFrame(results)

    # 🔹 Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Files", len(df))
    col2.metric("Before Success", (df["Before Status"] == "Success").sum())
    col3.metric("After Success", (df["After Status"] == "Success").sum())

    st.divider()

    # 🔹 Table
    st.subheader("📄 File Data")
    st.dataframe(df, use_container_width=True)

    # 🔹 Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⏱️ Execution Time Comparison")
        st.bar_chart(df.set_index("File")[["Before Time (sec)", "After Time (sec)"]])

    with col2:
        st.subheader("📦 File Size Comparison")
        st.bar_chart(df.set_index("File")[["Before Size (KB)", "After Size (KB)"]])

    st.subheader("📈 Time Trend")
    st.line_chart(df["After Time (sec)"])

    # 🔹 Insights
    st.subheader("🧠 Insights")

    avg_time = df["After Time (sec)"].mean()
    st.write(f"Average Execution Time (After Obfuscation): {avg_time:.4f} sec")

    slowest = df.loc[df["After Time (sec)"].idxmax()]
    st.write(f"🐢 Slowest File: {slowest['File']}")

    fastest = df.loc[df["After Time (sec)"].idxmin()]
    st.write(f"⚡ Fastest File: {fastest['File']}")
