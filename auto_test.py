import time
from pywinauto import Application


# --------------------------------------------------
# 配置
# --------------------------------------------------
import configparser

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

APP_PATH = config["app"]["path"]
USERNAME = config["login"]["username"]
PASSWORD = config["login"]["password"]

LOOP_COUNT = int(config["test"]["loop_count"])


# --------------------------------------------------
# 启动应用
# --------------------------------------------------
print("Starting UroBiopsy...")
app = Application(backend="uia").start(APP_PATH)

time.sleep(5)


# --------------------------------------------------
# 登录界面
# --------------------------------------------------
print("Waiting for Login window...")

login_dlg = app.window(title_re=".*UroBiopsy.*Login.*")
login_dlg.wait("visible", timeout=30)

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


# --------------------------------------------------
# 等待主界面
# --------------------------------------------------
print("Waiting for Main UI...")

main_dlg = app.window(title_re=".*UroBiopsy.*")

init_btn = main_dlg.child_window(
    title="Initialize Robot",
    control_type="Button"
)

init_btn.wait("visible enabled", timeout=200)

print("Main UI ready")


# --------------------------------------------------
# 初始化 + Cancel 循环
# --------------------------------------------------
for i in range(1, LOOP_COUNT + 1):
    print(f"Initialization cycle {i}")

    init_btn = main_dlg.child_window(
        title="Initialize Robot",    
        control_type="Button"
    )

    yes_btn = main_dlg.child_window(
        title="Yes",                   
        control_type="Button"
    )

    cancel_btn = main_dlg.child_window(
        title="Cancel",                   
        control_type="Button"
    )

    # 第一次初始化
    init_btn.wait("enabled", timeout=200)
    init_btn.click_input()
    time.sleep(2)

    # 点击 Yes
    yes_btn.wait("enabled", timeout=200)
    yes_btn.click_input()
    time.sleep(5)

    # 点击 Cancel
    cancel_btn.wait("enabled", timeout=200)
    cancel_btn.click_input()
    time.sleep(2)

    # # 第二次初始化（完整执行）
    # init_btn.wait("enabled", timeout=30)
    # init_btn.click_input()

    # # 等待初始化完成
    # # 推荐方式：等待按钮重新可用
    # init_btn.wait("enabled", timeout=300)

    # time.sleep(1)


# --------------------------------------------------
# 退出应用
# --------------------------------------------------
print("Closing UroBiopsy...")
print("Closing via Alt+F4")

main_dlg.set_focus()
time.sleep(1)
main_dlg.type_keys("%{F4}")

# 确认退出
yes_btn = app.window(title_re=".*").child_window(
    title="Yes",
    control_type="Button"
)

yes_btn.wait("enabled", timeout=200)
yes_btn.click_input()


print("TEST COMPLETED SUCCESSFULLY")
