import time
import os
import sys
import traceback
from pywinauto import Application
import configparser


# --------------------------------------------------
# 读取配置
# --------------------------------------------------
config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

APP_PATH = config["app"]["path"]
USERNAME = config["login"]["username"]
PASSWORD = config["login"]["password"]

LOOP_COUNT = int(config["test"]["loop_count"])

AUTO_SHUTDOWN = config.getboolean("system", "auto_shutdown", fallback=False)
SHUTDOWN_DELAY = config.getint("system", "shutdown_delay", fallback=60)


# --------------------------------------------------
# 自动关机函数（统一出口）
# --------------------------------------------------
def shutdown_system():
    if AUTO_SHUTDOWN:
        print(f"[SYSTEM] Shutdown in {SHUTDOWN_DELAY} seconds...")
        os.system(f"shutdown /s /t {SHUTDOWN_DELAY}")


# --------------------------------------------------
# 主逻辑
# --------------------------------------------------
def main():
    print("Starting UroBiopsy...")

    app = Application(backend="uia").start(APP_PATH)
    time.sleep(5)

    # ---------------- 登录界面 ----------------
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

    # ---------------- 主界面 ----------------
    print("Waiting for Main UI...")

    main_dlg = app.window(title_re=".*UroBiopsy.*")

    init_btn = main_dlg.child_window(
        title="Initialize Robot",
        control_type="Button"
    )

    init_btn.wait("visible enabled", timeout=200)

    print("Main UI ready")

    # ---------------- 初始化循环 ----------------
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

        init_btn.wait("enabled", timeout=200)
        init_btn.click_input()
        time.sleep(2)

        yes_btn.wait("enabled", timeout=200)
        yes_btn.click_input()
        time.sleep(5)

        cancel_btn.wait("enabled", timeout=200)
        cancel_btn.click_input()
        time.sleep(2)

    # ---------------- 退出应用 ----------------
    print("Closing UroBiopsy...")
    main_dlg.set_focus()
    time.sleep(1)
    main_dlg.type_keys("%{F4}")

    yes_btn = app.window(title_re=".*").child_window(
        title="Yes",
        control_type="Button"
    )

    yes_btn.wait("enabled", timeout=200)
    yes_btn.click_input()

    print("TEST COMPLETED SUCCESSFULLY")


# --------------------------------------------------
# 程序入口 + 异常兜底
# --------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR OCCURRED")
        traceback.print_exc()
    finally:
        shutdown_system()
