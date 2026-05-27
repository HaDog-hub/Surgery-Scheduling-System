import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 中文顯示設定
matplotlib.rcParams['font.family'] = 'Microsoft JhengHei'
matplotlib.rcParams['axes.unicode_minus'] = False

# 載入排程參數
def load_exec_params(path="SERVER\\server\\SurgerySchedulerSA\\data\\in\\Arguments4Exec.csv"):
    encodings = ["utf-8-sig", "cp950", "big5", "utf-8"]
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc, header=None)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError("無法解碼 Arguments4Exec.csv")

    values = df.iloc[1::2, 0].astype(int).tolist()
    return {
        "start_time": values[0],
        "max_regular": values[1],
        "max_overtime": values[2],
        "cleaning_time": values[3],
    }

PARAMS = load_exec_params()

def load_schedule(path):
    with open(path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()

    if first_line.startswith("surgeryId"):
        df = pd.read_csv(path)
    else:
        df = pd.read_csv(path, header=None,
                         names=["surgeon", "roomId", "anesthesia", "duration", "roomRequirement", "order"])
        df["priority"] = 1
        df["specialty"] = "UNK"

    df["duration"] = pd.to_numeric(df["duration"], errors='coerce').fillna(0).astype(int)
    df["order"] = pd.to_numeric(df["order"], errors='coerce').fillna(0).astype(int)

    df["start"] = 0
    df["end"] = 0

    # 👉 根據 roomId + order 排序（會影響 start/end 的計算順序）
    df = df.sort_values(by=["roomId", "order"]).reset_index(drop=True)

    # 根據順序決定 start / end 時間
    for room in df['roomId'].dropna().unique():
        current_time = 0
        for idx in df[df['roomId'] == room].index:
            df.loc[idx, 'start'] = current_time
            df.loc[idx, 'end'] = current_time + df.loc[idx, 'duration']
            current_time = df.loc[idx, 'end'] + PARAMS["cleaning_time"]

    return df

def classify_by_end(end_time):
    base = PARAMS["start_time"]
    reg_limit = base + PARAMS["max_regular"]
    ot_limit = reg_limit + PARAMS["max_overtime"]
    if end_time <= reg_limit:
        return "regular"
    elif end_time <= ot_limit:
        return "overtime"
    else:
        return "overdue"

def classify_and_plot(ax, df, room_pos, offset, label_prefix, colors, cleaning_color):
    first_room = list(room_pos.keys())[0]
    for _, row in df.iterrows():
        if row["duration"] <= 0:
            continue

        y = room_pos[row["roomId"]] + offset
        start = row["start"] + PARAMS["start_time"]
        end = row["end"] + PARAMS["start_time"]
        color_key = classify_by_end(end)
        label = f"{label_prefix}：{color_key}" if row["roomId"] == first_room else ""
        ax.barh(y, end - start, left=start, color=colors[color_key], edgecolor="black", height=0.4, label=label)

        # 加入清消區塊
        clean_label = f"{label_prefix}：清消" if row["roomId"] == first_room else ""
        ax.barh(y, PARAMS["cleaning_time"], left=end, color=cleaning_color, edgecolor="black", height=0.4,
                label=clean_label)

def plot_gantt(df_old, df_new):
    fig, ax = plt.subplots(figsize=(14, 8))
    y_labels = sorted(set(df_old['roomId'].dropna()) | set(df_new['roomId'].dropna()))
    room_pos = {room: i for i, room in enumerate(y_labels)}

    classify_and_plot(ax, df_old, room_pos, 0, "原始排程", {
        "regular": "#6aa84f",   # 深綠
        "overtime": "#ffd966",  # 深黃
        "overdue": "#cc0000"    # 深紅
    }, cleaning_color="#3c78d8")  # 深藍

    classify_and_plot(ax, df_new, room_pos, 0.45, "模擬退火後", {
        "regular": "#93c47d",   # 淺綠
        "overtime": "#f6b26b",  # 淺黃
        "overdue": "#e06666"    # 淺紅
    }, cleaning_color="#9fc5e8")  # 淺藍

    ax.set_yticks([r + 0.2 for r in range(len(y_labels))])
    ax.set_yticklabels(y_labels)
    ax.set_xlabel("時間（分鐘，自午夜起）")
    ax.set_title("手術排程甘特圖（區分常規／加班／超時 + 清消）")
    ax.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    old_df = load_schedule("SERVER\\server\\SurgerySchedulerSA\\data\\in\\TimeTable.csv")
    new_df = load_schedule("SERVER\\server\\SurgerySchedulerSA\\data\\out\\newTimeTable.csv")
    plot_gantt(old_df, new_df)
