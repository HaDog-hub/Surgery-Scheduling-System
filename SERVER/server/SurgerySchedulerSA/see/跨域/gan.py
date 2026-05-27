# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
# import pandas as pd
# from datetime import datetime, timedelta
# import matplotlib.dates as mdates
# import matplotlib.cm as cm
# import matplotlib.colors as mcolors

# # 中文字型設定
# plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta', 'Microsoft JhengHei', 'Arial Unicode MS']
# plt.rcParams['axes.unicode_minus'] = False

# # 任務資料
# tasks = [    
#     ("確認問題與臨床需求", "2024/08/22", "2024/09/08"),
#     ("蒐集資料與解決方式", "2024/09/09", "2024/09/28"),
#     ("問題塑模", "2024/09/28", "2024/11/05"),
#     ("搜集與整理演算法文獻", "2024/10/28", "2024/12/13"),
#     ("撰寫模擬退火程式", "2024/12/14", "2025/01/25"),
#     ("加入多種擾動與測試", "2025/01/26", "2025/02/20"),
#     ("加入自適應溫度控制", "2025/02/21", "2025/03/20"),
#     ("釐清系統功能需求", "2024/11/21", "2024/12/12"),
#     ("建立系統資料庫", "2024/12/13", "2025/01/18"),
#     ("設計前後端架構", "2025/01/19", "2025/02/04"),
#     ("建立前後端架構", "2025/02/01", "2025/03/14"),
#     ("後端功能實作與資料串接", "2025/03/15", "2025/06/14"),
#     ("前端排程頁面設計與實作", "2025/03/20", "2025/06/14"),
#     ("系統整合", "2025/05/30", "2025/06/14"),
#     ("功能測試與修正錯誤", "2025/06/15", "2025/07/29"),
#     ("撰寫文件", "2025/06/25", "2025/07/29"),
#     ("專案完成", "2025/07/29", "2025/07/29"),
# ]

# # 使用 tab10 色系（鮮明乾淨）
# tab10 = cm.get_cmap('tab10', len(tasks))
# colors = [tab10(i) for i in range(len(tasks))]

# # 建立 DataFrame 並加入顏色欄位
# df = pd.DataFrame(tasks, columns=["工作內容", "開始", "結束"])
# df["開始"] = pd.to_datetime(df["開始"])
# df["結束"] = pd.to_datetime(df["結束"])
# df["工作日數"] = (df["結束"] - df["開始"]).dt.days + 1
# df["顏色"] = colors

# # 繪圖
# fig, ax = plt.subplots(figsize=(20, 30))
# bars = []
# for i, row in df.iterrows():
#     bar = ax.barh(y=i, width=row["工作日數"], left=row["開始"], height=0.8,
#                   align='center', color=row["顏色"])
#     bars.append(bar)
#     ax.text(row["開始"] + timedelta(days=row["工作日數"] / 2),
#             i, f'{row["工作日數"]} 天',
#             va='center', ha='center', fontsize=18, color='black')

# # 設定 y 軸與文字顏色
# yticks = range(len(df))
# ax.set_yticks(yticks)
# ax.set_yticklabels(df["工作內容"], fontweight='bold', fontsize=28)
# for label, color in zip(ax.get_yticklabels(), df["顏色"]):
#     label.set_color(color)

# # 軸設定
# ax.set_xlabel("日期", fontsize=18)
# ax.set_title("SurgiFlow：智能手術排程管理系統 計劃管理甘特圖", fontsize=18)
# ax.tick_params(axis='x', labelsize=18)  # 放大 X 軸日期刻度字體
# ax.invert_yaxis()

# # 日期格式
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
# ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
# ax.tick_params(axis='x', labelsize=18)
# fig.autofmt_xdate()

# # 網格與排版
# ax.grid(True, axis='x', linestyle='--', alpha=0.5)
# # plt.tight_layout()
# plt.subplots_adjust(top=0.97, bottom=0.1, left=0.18, right=0.98)
# plt.show()
# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
# import pandas as pd
# from datetime import datetime, timedelta
# import matplotlib.dates as mdates
# # import matplotlib.cm as cm  # 已註解掉顏色套件
# # import matplotlib.colors as mcolors

# # 中文字型設定
# plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta', 'Microsoft JhengHei', 'Arial Unicode MS']
# plt.rcParams['axes.unicode_minus'] = False

# # 任務資料
# tasks = [    
#     ("確認問題與臨床需求", "2024/08/22", "2024/09/08"),
#     ("蒐集資料與解決方式", "2024/09/09", "2024/09/28"),
#     ("問題塑模", "2024/09/28", "2024/11/05"),
#     ("搜集與整理演算法文獻", "2024/10/28", "2024/12/13"),
#     ("撰寫模擬退火程式", "2024/12/14", "2025/01/25"),
#     ("加入多種擾動與測試", "2025/01/26", "2025/02/20"),
#     ("加入自適應溫度控制", "2025/02/21", "2025/03/20"),
#     ("釐清系統功能需求", "2024/11/21", "2024/12/12"),
#     ("建立系統資料庫", "2024/12/13", "2025/01/18"),
#     ("設計前後端架構", "2025/01/19", "2025/02/04"),
#     ("建立前後端架構", "2025/02/01", "2025/03/14"),
#     ("後端功能實作與資料串接", "2025/03/15", "2025/06/14"),
#     ("前端排程頁面設計與實作", "2025/03/20", "2025/06/14"),
#     ("系統整合", "2025/05/30", "2025/06/14"),
#     ("功能測試與修正錯誤", "2025/06/15", "2025/07/29"),
#     ("撰寫文件", "2025/06/25", "2025/07/29"),
#     ("專案完成", "2025/07/29", "2025/07/29"),
# ]

# # 建立 DataFrame
# df = pd.DataFrame(tasks, columns=["工作內容", "開始", "結束"])
# df["開始"] = pd.to_datetime(df["開始"])
# df["結束"] = pd.to_datetime(df["結束"])
# df["工作日數"] = (df["結束"] - df["開始"]).dt.days + 1
# # df["顏色"] = ['gray'] * len(df)  # 不使用顏色

# # 繪圖
# fig, ax = plt.subplots(figsize=(20, 35))
# bars = []
# for i, row in df.iterrows():
#     bar = ax.barh(y=i, width=row["工作日數"], left=row["開始"], height=0.8,
#                   align='center', color='white', edgecolor='black')  # 改為白底黑框
#     bars.append(bar)
#     ax.text(row["開始"] + timedelta(days=row["工作日數"] / 2),
#             i, f'{row["工作日數"]} 天',
#             va='center', ha='center', fontsize=25, color='black')

# # 設定 y 軸
# yticks = range(len(df))
# ax.set_yticks(yticks)
# ax.set_yticklabels(df["工作內容"], fontweight='bold', fontsize=32, color='black')

# # 軸設定
# ax.set_xlabel("日期", fontsize=32)
# ax.set_title("SurgiFlow：智能手術排程管理系統 計劃管理甘特圖", fontsize=32)
# ax.tick_params(axis='x', labelsize=32)
# ax.invert_yaxis()

# # 日期格式
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
# ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
# fig.autofmt_xdate()

# # 網格與排版
# ax.grid(True, axis='x', linestyle='--', alpha=0.5)
# plt.subplots_adjust(top=0.96, bottom=0.14, left=0.20, right=0.98)
# plt.show()
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# 載入中文字型與英文字型（Windows 路徑）
chinese_font = fm.FontProperties(fname="C:/Windows/Fonts/kaiu.ttf", weight='bold')  # 標楷體
english_font = fm.FontProperties(fname="C:/Windows/Fonts/times.ttf", weight='bold')  # Times New Roman

# 任務資料
tasks = [    
    ("確認問題與臨床需求", "2024/08/22", "2024/09/08"),
    ("蒐集資料與解決方式", "2024/09/09", "2024/09/28"),
    ("問題塑模", "2024/09/28", "2024/11/05"),
    ("搜集與整理演算法文獻", "2024/10/28", "2024/12/13"),
    ("撰寫模擬退火程式", "2024/12/14", "2025/01/25"),
    ("加入多種擾動與測試", "2025/01/26", "2025/02/20"),
    ("加入自適應溫度控制", "2025/02/21", "2025/03/20"),
    ("釐清系統功能需求", "2024/11/21", "2024/12/12"),
    ("建立系統資料庫", "2024/12/13", "2025/01/18"),
    ("設計前後端架構", "2025/01/19", "2025/02/04"),
    ("建立前後端架構", "2025/02/01", "2025/03/14"),
    ("後端功能實作與資料串接", "2025/03/15", "2025/06/14"),
    ("前端排程頁面設計與實作", "2025/03/20", "2025/06/14"),
    ("系統整合", "2025/05/30", "2025/06/14"),
    ("功能測試與修正錯誤", "2025/06/15", "2025/07/29"),
    ("撰寫文件", "2025/06/25", "2025/07/29"),
    ("專案完成", "2025/07/29", "2025/07/29"),
]

# 建立 DataFrame
df = pd.DataFrame(tasks, columns=["工作內容", "開始", "結束"])
df["開始"] = pd.to_datetime(df["開始"])
df["結束"] = pd.to_datetime(df["結束"])
df["工作日數"] = (df["結束"] - df["開始"]).dt.days + 1

# 繪圖
fig, ax = plt.subplots(figsize=(20, 35))
for i, row in df.iterrows():
    ax.barh(
        y=i,
        width=row["工作日數"],
        left=row["開始"],
        height=0.8,
        align='center',
        color='white',
        edgecolor='black'
    )
    # ax.text(
    #     row["開始"] + timedelta(days=row["工作日數"] / 2),
    #     i,
    #     f'{row["工作日數"]} 天',
    #     va='center',
    #     ha='center',
    #     fontsize=25,
    #     color='black',
    #     fontproperties=english_font  # 數字用 Times New Roman
    # )
    # 畫數字（Times New Roman）
    ax.text(
        row["開始"] + timedelta(days=row["工作日數"] / 2 - 0.5),
        i,
        f'{row["工作日數"]}',
        va='center',
        ha='right',
        fontsize=25,
        color='black',
        fontproperties=english_font
    )

    # 畫「天」（標楷體）
    ax.text(
        row["開始"] + timedelta(days=row["工作日數"] / 2 + 0.5),
        i,
        '天',
        va='center',
        ha='left',
        fontsize=25,
        color='black',
        fontproperties=chinese_font
    )


# 設定 Y 軸標籤（使用標楷體）
yticks = range(len(df))
ax.set_yticks(yticks)
ax.set_yticklabels(df["工作內容"], fontsize=28, fontproperties=chinese_font)

# X 軸與標題（日期 + 中文）
ax.set_xlabel("日期", fontsize=32, fontproperties=chinese_font)
ax.set_title("SurgiFlow：智能手術排程管理系統 計劃管理甘特圖", fontsize=32, fontproperties=chinese_font)
ax.invert_yaxis()

# X 軸時間刻度
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
for label in ax.get_xticklabels():
    label.set_fontproperties(english_font)
    label.set_fontsize(20)

# 網格與排版
ax.grid(True, axis='x', linestyle='--', alpha=0.5)
plt.subplots_adjust(top=0.96, bottom=0.065, left=0.18, right=0.98)
plt.show()
