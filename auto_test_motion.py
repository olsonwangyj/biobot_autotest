import time
import os
import configparser
from pywinauto import Application, mouse


# ==================================================
# 工具：点击 popup 坐标中心
# ==================================================
def click_rect_center(rect):
    x = (rect["l"] + rect["r"]) // 2
    y = (rect["t"] + rect["b"]) // 2
    mouse.click(button="left", coords=(x, y))


# ==================================================
# 配置
# ==================================================
config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

APP_PATH = config["app"]["path"]
USERNAME = config["login"]["username"]
PASSWORD = config["login"]["password"]
INIT_COUNT = int(config["test"]["init_count"])

AUTO_SHUTDOWN = config["system"].getboolean("auto_shutdown")
SHUTDOWN_DELAY = int(config["system"]["shutdown_delay_seconds"])


# ==================================================
# popup 坐标（Inspect 得到）
# ==================================================
MENU_LEVEL_1_RECT = {"l": 83, "t": 793, "r": 243, "b": 833}
MENU_LEVEL_2_RECT = {"l": 243, "t": 750, "r": 403, "b": 790}
MENU_EXIT_RECT   = {"l": 83, "t": 993, "r": 243, "b": 1033}


# ==================================================
# 启动
# ==================================================
print("Starting UroBiopsy...")
app = Application(backend="uia").start(APP_PATH)
time.sleep(5)


# ==================================================
# 登录
# ==================================================
print("Waiting for Login window...")
login_dlg = app.window(title_re=".*UroBiopsy.*Login.*")
login_dlg.wait("visible", timeout=60)

login_dlg.child_window(
    auto_id="UserLoginDialog.frame.EditUsername",
    control_type="Edit"
).set_text(USERNAME)

login_dlg.child_window(
    auto_id="UserLoginDialog.frame.EditPassword",
    control_type="Edit"
).set_text(PASSWORD)

login_dlg.child_window(
    auto_id="UserLoginDialog.frame_2.buttonLogin",
    control_type="Button"
).click_input()

print("Login clicked")


# ==================================================
# 主界面
# ==================================================
print("Waiting for Main UI...")
main_dlg = app.window(title_re=".*UroBiopsy.*")
main_dlg.wait("visible", timeout=120)
print("Main UI ready")


# ==================================================
# System → Robot Initialization
# ==================================================
print("Clicking System button...")
main_dlg.child_window(title="System", control_type="Button").click_input()
time.sleep(0.8)

print("Clicking first popup menu...")
click_rect_center(MENU_LEVEL_1_RECT)
time.sleep(0.8)

print("Clicking third item in second popup...")
click_rect_center(MENU_LEVEL_2_RECT)
time.sleep(1)


# ==================================================
# Robot Initialization UI
# ==================================================
print("Waiting for Robot Initialization UI...")

loop_spin = main_dlg.child_window(
    auto_id="BaseMainWindow.mainWidget.rightFrame.actionStackedWidget."
            "emcLayout.emcInitGroupBoxRobot.emcLoopSpinBoxRobot",
    control_type="Spinner"
)

loop_spin.wait("visible enabled", timeout=120)
print("Robot Initialization UI ready")


# ==================================================
# 输入 loop count
# ==================================================
print(f"Setting loop count to {INIT_COUNT}...")

loop_spin.click_input()
time.sleep(0.2)
loop_spin.type_keys("^a{BACKSPACE}")
loop_spin.type_keys(str(INIT_COUNT))

time.sleep(0.5)
print("Loop count set")


# ==================================================
# Start
# ==================================================
start_btn = main_dlg.child_window(
    auto_id="BaseMainWindow.mainWidget.rightFrame.actionStackedWidget."
            "emcLayout.emcInitGroupBoxRobot.emcStartInitRobot",
    control_type="Button"
)

start_btn.wait("enabled", timeout=30)
start_btn.click_input()
print("Start clicked")


# ==================================================
# Start 后确认 Yes
# ==================================================
try:
    yes_btn = app.window(title_re=".*").child_window(
        title="Yes",
        control_type="Button"
    )
    yes_btn.wait("enabled", timeout=15)
    yes_btn.click_input()
    print("Start confirmation Yes clicked")
except Exception:
    print("No confirmation dialog after Start")


# ==================================================
# 等待初始化完成（不用 sleep）
# ==================================================
print("Waiting for initialization to finish...")
back_btn = main_dlg.child_window(title="Back", control_type="Button")

MAX_TIMEOUT = INIT_COUNT * 180
back_btn.wait("enabled", timeout=MAX_TIMEOUT)
print("Initialization finished")


# ==================================================
# Back
# ==================================================
back_btn.click_input()
time.sleep(2)


# ==================================================
# 退出程序（System → Exit）
# ==================================================
print("Exiting via System → Exit...")

main_dlg.child_window(title="System", control_type="Button").click_input()
time.sleep(0.8)

click_rect_center(MENU_EXIT_RECT)
time.sleep(1)

# Exit 确认
try:
    exit_yes = app.window(title_re=".*").child_window(
        title="Yes",
        control_type="Button"
    )
    exit_yes.wait("enabled", timeout=15)
    exit_yes.click_input()
    print("Exit confirmed")
except Exception:
    print("No exit confirmation dialog")


# ==================================================
# 自动关机
# ==================================================
if AUTO_SHUTDOWN:
    print(f"System will shutdown in {SHUTDOWN_DELAY} seconds...")
    time.sleep(SHUTDOWN_DELAY)
    os.system("shutdown /s /t 0")

print("TEST COMPLETED SUCCESSFULLY")
