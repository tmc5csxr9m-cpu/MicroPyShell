# MicroPyShell

[English](#english) | [中文](#chinese)

A minimal Python runtime for MicroPython devices with dual‑core processors, designed for extensibility and thread‑safe service management.

---

## English

### Overview

MicroPyShell is a lightweight runtime environment written in Python. It provides a basic command shell with argument parsing, a modular API (`api.py`), and a built‑in Service Manager for background tasks.

**Current features:**

- Basic shell (limited feature set – more commands will come as time permits)
- Service Manager that supports:
  - Auto‑start services (run once at boot)
  - Persistent services, which are always scheduled to run at a fixed interval (every *n* seconds)
- Thread‑safe API – a default instance is available as `api.system`

**Known limitations and realities:**

- The shell is minimal right now, purely because development time has been scarce. It will be extended gradually.
- Persistent services = timed services. There is no "always running without a timer" mode at the moment.
- Services are executed by iterating over a list; performance may degrade with many services.
- Code is currently **uncommented** and documentation is sparse – you will need to read the source. Proper docs will be added when time permits.

### Requirements

- A MicroPython device with a **dual‑core processor** (e.g. Raspberry Pi Pico, ESP32)
- Enough free storage for all `.py` files and the `sm.json` configuration

### Quick Start

1. Flash MicroPython onto your device.
2. Copy **all `.py` files** (including `main.py`) from this project to the board.
3. Create an `sm.json` file in the root directory. It uses **JSON Lines** format – exactly three lines, each a JSON object:
   - **Line 1**: Auto‑start services. Format: `{"service_name": "python_code"}`
   - **Line 2**: Persistent (timed) services. Format: `{"service_name": "python_code"}`
   - **Line 3**: Execution intervals for persistent services. Format: `{"service_name": n}` (run every `n` seconds)
4. Reset the device. The runtime will start automatically via `main.py`.

See the source for details – there is no separate documentation yet.

### Using the API

The core API is in `api.py`. After importing the module, you can use the pre‑instantiated object `api.system`. It is designed to be thread‑safe and can be called from the main thread or from `_thread` workers.

### Contributing

Contributions are very welcome – don’t worry if your code isn’t perfect. Areas where help is especially appreciated:

- More efficient service scheduling
- New shell commands
- Any comments or documentation that make the code easier to understand

---

## Chinese

### 概述

MicroPyShell 是一个轻量级的 Python 运行时环境，专为双核 MicroPython 设备设计。它提供一个基础命令行 Shell（支持参数解析）、模块化 API（`api.py`）以及内置的服务管理器。

**当前功能：**

- 基础 Shell（功能有限，后续会逐步添加更多命令）
- 服务管理器，支持：
  - 开机自启动服务（设备启动时运行一次）
  - 常驻服务，同时也是定时服务，每隔固定秒数运行一次
- 线程安全的 API，默认实例名为 `api.system`

**已知局限与实际情况：**

- Shell 目前比较简单，纯粹是因为开发时间有限，后续会逐步扩展。
- 常驻服务即定时服务，暂不支持无定时模式的常驻后台运行。
- 服务通过遍历列表执行，服务数量多时效率会降低。
- 代码**完全没有注释**，文档缺失 – 需要自行阅读源码。后续有时间会补充文档。

### 运行要求

- 具备**双核处理器**的 MicroPython 设备（如 Raspberry Pi Pico、ESP32）
- 足够的存储空间存放所有 `.py` 文件与 `sm.json` 配置文件

### 快速开始

1. 将 MicroPython 固件烧录到设备。
2. 将项目的**所有 `.py` 文件**（包括 `main.py`）复制到开发板。
3. 在根目录创建 `sm.json` 文件，采用 **JSON Lines** 格式，共三行，每行一个 JSON 对象：
   - **第一行**：开机自启动服务。格式：`{"服务名": "python 代码"}`
   - **第二行**：常驻（定时）服务。格式：`{"服务名": "python 代码"}`
   - **第三行**：常驻服务的执行间隔。格式：`{"服务名": n}` (n 为秒数，表示每 n 秒运行一次)
4. 重置设备，运行时会通过 `main.py` 自动启动。

配置细节请自行查阅源码 – 目前暂无独立文档。

### API 使用

核心 API 位于 `api.py` 中。导入模块后可直接使用预实例化的对象 `api.system`，它被设计为线程安全，可在主线程或 `_thread` 子线程中安全调用。

### 参与贡献

非常欢迎贡献，代码质量不必苛求。尤其期待以下方向的帮助：

- 更高效的服务调度机制
- 新的 Shell 命令
- 任何能让代码更容易理解的注释或文档
