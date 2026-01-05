import time
import os
from pywinauto import Application, Desktop
from pywinauto.keyboard import send_keys


# --------------------------------------------------
# 配置
# --------------------------------------------------
WORD_PATH = r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
SAVE_DIR = r"D:\auto_test\WordDocs"
DOC_COUNT = 10

os.makedirs(SAVE_DIR, exist_ok=True)


# --------------------------------------------------
# 启动 Word
# --------------------------------------------------
print("Starting Microsoft Word...")
Application(backend="uia").start(WORD_PATH)

time.sleep(10)  # Word 启动 + Start Page 非常慢


# --------------------------------------------------
# 手动定位 Word 主窗口（关键点）
# --------------------------------------------------
print("Searching for visible Word window...")

word = None
for w in Desktop(backend="uia").windows():
    try:
        if "Word" in w.window_text() and w.is_visible():
            word = w
            break
    except Exception:
        pass

if word is None:
    raise RuntimeError("FAILED: Cannot find visible Word window")

word.set_focus()
print(f"Connected to Word window: {word.window_text()}")


# --------------------------------------------------
# 进入编辑模式（TAB + ENTER 实验法）
# --------------------------------------------------
print("Opening Blank document...")

send_keys("{ESC}")
time.sleep(0.5)
word.set_focus()
time.sleep(0.5)

# ⚠️ 这个 TAB 次数和 Office 版本有关
for _ in range(6):
    send_keys("{TAB}")
    time.sleep(0.3)

send_keys("{ENTER}")
time.sleep(4)


# --------------------------------------------------
# 主循环
# --------------------------------------------------
for i in range(1, DOC_COUNT + 1):
    print(f"Processing document {i}")

    send_keys("Hello{SPACE}Word", with_spaces=True)
    time.sleep(1)

    # Save As
    send_keys("{F12}")
    time.sleep(3)

    file_path = os.path.join(SAVE_DIR, f"doc{i}.docx")
    send_keys(file_path, with_spaces=True)
    time.sleep(0.5)
    send_keys("{ENTER}")
    time.sleep(3)

    # Close document
    send_keys("^w")
    time.sleep(2)

    # New document（此时在编辑模式，Ctrl+N 有效）
    send_keys("^n")
    time.sleep(3)


# --------------------------------------------------
# 退出 Word
# --------------------------------------------------
print("Closing Word...")
send_keys("%{F4}")

print("TEST FINISHED")
