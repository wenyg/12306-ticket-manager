# 项目结构

```
12306-ticket-manager/
├── 📁 ticket/                    # 车票管理模块
│   ├── __init__.py              # 模块初始化文件
│   ├── models.py                # 数据库模型和操作
│   └── ticket_parser.py         # 车票信息解析器
├── 📁 tools/                     # 工具模块
│   └── mail.py                  # 邮件处理模块
├── 📁 static/                    # 静态文件
│   └── index.html               # Web界面
├── 📁 assert/                    # 项目截图
│   ├── image.png                # 主界面截图
│   ├── image1.png               # 车票详情截图
│   └── image2.png               # 统计信息截图
├── 📁 docs/                      # 文档
│   └── API.md                   # API文档
├── 📁 examples/                  # 示例
│   └── example_config.py        # 配置示例
├── 📁 scripts/                   # 脚本
│   ├── setup.py                 # 安装脚本
│   └── start.sh                 # 启动脚本
├── 📄 main.py                   # 主应用文件
├── 📄 config.py                 # 配置文件
├── 📄 requirements.txt          # 依赖列表
├── 📄 quick_start.py            # 快速启动脚本
├── 📄 README.md                 # 项目说明
├── 📄 LICENSE                   # 许可证
├── 📄 CHANGELOG.md              # 更新日志
├── 📄 CONTRIBUTING.md           # 贡献指南
├── 📄 PROJECT_STRUCTURE.md      # 项目结构说明
└── 📄 .gitignore                # Git忽略文件
```

## 文件说明

### 核心模块

- **`main.py`**: FastAPI主应用，提供Web服务和API接口
- **`config.py`**: 系统配置文件，包含邮箱、数据库、服务器等配置
- **`ticket/`**: 车票管理核心模块
  - `models.py`: 数据库模型，定义车票数据结构和数据库操作
  - `ticket_parser.py`: 车票信息解析器，解析邮件中的车票信息
- **`tools/mail.py`**: 邮件处理模块，负责从邮箱读取和处理邮件

### 静态文件

- **`static/index.html`**: 美观的Web界面，支持移动端访问

### 项目截图

- **`assert/`**: 项目界面截图文件夹
  - `image.png`: 主界面截图，展示系统整体布局
  - `image1.png`: 车票详情页面截图，展示车票信息详情
  - `image2.png`: 统计信息页面截图，展示数据统计功能

### 文档

- **`README.md`**: 项目介绍、安装和使用说明
- **`docs/API.md`**: 详细的API接口文档
- **`CHANGELOG.md`**: 版本更新日志
- **`CONTRIBUTING.md`**: 贡献指南
- **`PROJECT_STRUCTURE.md`**: 项目结构说明

### 脚本和工具

- **`quick_start.py`**: 一键快速启动脚本
- **`scripts/setup.py`**: 安装和初始化脚本
- **`scripts/start.sh`**: Shell启动脚本
- **`examples/example_config.py`**: 配置文件示例

### 配置文件

- **`requirements.txt`**: Python依赖包列表
- **`.gitignore`**: Git版本控制忽略文件
- **`LICENSE`**: MIT开源许可证

## 技术架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   邮箱服务器     │    │   邮件处理模块   │    │   数据解析模块   │
│  (IMAP/SMTP)    │───▶│   (tools/mail)  │───▶│ (ticket_parser) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web界面       │    │   FastAPI服务   │    │   SQLite数据库  │
│ (static/index)  │◀───│   (main.py)     │◀───│  (ticket/models)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 数据流

1. **邮件获取**: `tools/mail.py` 从邮箱服务器获取12306邮件
2. **信息解析**: `ticket/ticket_parser.py` 解析邮件中的车票信息
3. **数据存储**: `ticket/models.py` 将解析后的数据存储到SQLite数据库
4. **数据展示**: `main.py` 提供API接口，`static/index.html` 展示数据
5. **用户交互**: 用户通过Web界面查看和管理车票信息

## 扩展性

项目采用模块化设计，便于扩展：

- **新增邮箱支持**: 在`tools/mail.py`中添加新的邮箱服务商支持
- **新增数据源**: 可以添加其他数据源（如API、文件等）
- **新增展示方式**: 可以添加移动端APP、桌面应用等
- **新增功能**: 可以添加统计分析、通知提醒等功能 