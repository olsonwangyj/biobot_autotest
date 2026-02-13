# Auto Test Motion

用于自动化执行 UroBiopsy 的 Robot Initialization 测试流程（Windows UI 自动化）。

## 功能概览

脚本 `auto_test_motion.py` 会按顺序执行以下步骤：

1. 读取 `config.ini` 配置。
2. 启动目标程序（UroBiopsy）。
3. 在 Login 窗口输入账号密码并登录。
4. 进入主界面后点击 `System` 菜单，进入 `Robot Initialization`。
5. 设置循环次数（`init_count`）并点击 `Start`。
6. 自动处理 `Start` 后可能出现的 `Yes` 确认弹窗。
7. 等待初始化完成（通过 `Back` 按钮可用状态判断）。
8. 点击 `Back` 返回后，通过 `System -> Exit` 退出程序。
9. 可选：测试结束后自动关机。

## 运行环境

- Windows（脚本使用 `pywinauto` + UIA）
- Python 3.8+
- 目标软件可在本机正常启动并可见 UI

安装依赖：

```powershell
pip install pywinauto
```

## 配置文件

在项目根目录创建 `config.ini`，示例：

```ini
[app]
path = C:\Path\To\UroBiopsy.exe

[login]
username = your_username
password = your_password

[test]
init_count = 3

[system]
auto_shutdown = false
shutdown_delay_seconds = 30
```

字段说明：

- `app.path`：被测程序可执行文件路径。
- `login.username` / `login.password`：登录凭据。
- `test.init_count`：初始化循环次数。
- `system.auto_shutdown`：`true/false`，是否在测试后关机。
- `system.shutdown_delay_seconds`：关机前延时秒数。

## 使用方法

在项目根目录执行：

```powershell
python auto_test_motion.py
```

运行日志会在终端输出，例如：

- `Starting UroBiopsy...`
- `Login clicked`
- `Initialization finished`
- `TEST COMPLETED SUCCESSFULLY`

## 关键实现说明

- 通过 `pywinauto.Application(backend="uia")` 控制窗口与控件。
- 通过固定矩形坐标点击 popup 菜单（`MENU_LEVEL_1_RECT`、`MENU_LEVEL_2_RECT`、`MENU_EXIT_RECT`）。
- 以控件状态等待替代纯 `sleep`，例如等待 `Back` 按钮 `enabled` 判断初始化完成。
- `MAX_TIMEOUT = init_count * 180`，循环次数越大等待上限越长。

## 注意事项

- popup 菜单使用屏幕坐标点击，分辨率、缩放比例或 UI 布局变化会导致点击偏移。
- 建议测试时保持前台窗口稳定，避免人工干预鼠标键盘。
- 开启自动关机前请确认无其他未保存工作。
- 若控件的 `title/auto_id/control_type` 在新版本软件中变化，需要同步更新脚本定位逻辑。
