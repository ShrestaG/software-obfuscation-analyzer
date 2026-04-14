import time
import pandas as pd
import os

def obfuscate_code(code):
    return "# obfuscated\n" + code

def process_files(folder):
    results = []

    if not os.path.exists(folder):
        print("❌ 'files' folder not found!")
        return results

    for filename in os.listdir(folder):
        print("Processing:", filename)  # debug

        if filename.endswith(".py"):
            path = os.path.join(folder, filename)

            with open(path, "r") as f:
                code = f.read()

            start = time.time()

            time.sleep(len(code) * 0.0001)

            try:
                new_code = obfuscate_code(code)
                exec(new_code)
                status = "Success"
            except Exception as e:
                print("Error in", filename, ":", e)
                status = "Failed"

            end = time.time()

            results.append({
                "File": filename,
                "Status": status,
                "Time": round(end - start, 4),
                "File Size": len(code)
            })

    return results

if __name__ == "__main__":
    data = process_files("files")

    if not data:
        print("❌ No data processed!")
    else:
        df = pd.DataFrame(data)

        os.makedirs("data", exist_ok=True)
        df.to_csv("data/data.csv", index=False)

        print("✅ CSV created at data/data.csv")