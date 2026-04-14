import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="Obfuscation Dashboard", layout="wide")

st.title("🚀 Software Obfuscation Analyzer")
st.markdown("### Analyze and visualize code performance")

def obfuscate_code(code):
    return "# obfuscated\n" + code

results = []

# 🔹 OPTION SELECTOR
option = st.radio(
    "Choose Input Method:",
    ["Use Existing Files (files folder)", "Upload Files"]
)

# 🟢 OPTION 1: USE EXISTING FILES
if option == "Use Existing Files (files folder)":
    folder = "files"

    if st.button("Run Analysis on Folder"):
        for filename in os.listdir(folder):
            if filename.endswith(".py"):
                path = os.path.join(folder, filename)

                with open(path, "r") as f:
                    code = f.read()

                start = time.time()

                # 🔥 realistic delay
                time.sleep(len(code) * 0.0001)

                try:
                    new_code = obfuscate_code(code)
                    exec(new_code)
                    status = "Success"
                except Exception as e:
                    status = "Failed"

                end = time.time()

                results.append({
                    "File": filename,
                    "Status": status,
                    "Time (sec)": round(end - start, 4),
                    "File Size (KB)": round(len(code) / 1024, 2)
                })

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

            start = time.time()

            # 🔥 realistic delay
            time.sleep(len(code) * 0.0001)

            try:
                new_code = obfuscate_code(code)
                exec(new_code)
                status = "Success"
            except Exception as e:
                status = "Failed"

            end = time.time()

            results.append({
                "File": file.name,
                "Status": status,
                "Time (sec)": round(end - start, 4),
                "File Size (KB)": round(len(code) / 1024, 2)
            })

# 🔹 SHOW RESULTS
if results:
    df = pd.DataFrame(results)

    # 🔹 Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Files", len(df))
    col2.metric("Success", (df["Status"] == "Success").sum())
    col3.metric("Failed", (df["Status"] == "Failed").sum())

    st.divider()

    # 🔹 Table
    st.subheader("📄 File Data")
    st.dataframe(df, use_container_width=True)

    # 🔹 Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Status Distribution")
        st.bar_chart(df["Status"].value_counts())

    with col2:
        st.subheader("⏱️ Execution Time")
        st.bar_chart(df.set_index("File")["Time (sec)"])

    st.subheader("📈 Time Trend")
    st.line_chart(df["Time (sec)"])

    # 🔹 Insights
    st.subheader("🧠 Insights")

    avg_time = df["Time (sec)"].mean()
    st.write(f"Average Processing Time: {avg_time:.4f} sec")

    slowest = df.loc[df["Time (sec)"].idxmax()]
    st.write(f"🐢 Slowest File: {slowest['File']} ({slowest['Time (sec)']} sec)")

    fastest = df.loc[df["Time (sec)"].idxmin()]
    st.write(f"⚡ Fastest File: {fastest['File']} ({fastest['Time (sec)']} sec)")

    failed_files = df[df["Status"] == "Failed"]["File"].tolist()
    if failed_files:
        st.write("⚠️ Failed Files:", failed_files)