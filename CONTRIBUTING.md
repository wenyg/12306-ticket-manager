# 贡献指南

感谢您对12306车票信息管理系统的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 1. 报告问题

如果您发现了bug或有功能建议，请通过以下方式报告：

- 在GitHub上创建Issue
- 详细描述问题或建议
- 提供复现步骤（如果是bug）
- 附上相关的日志信息

### 2. 提交代码

#### 开发环境设置

1. Fork项目到您的GitHub账户
2. 克隆您的fork到本地：
   ```bash
   git clone https://github.com/wenyg/12306-ticket-manager.git
   cd 12306-ticket-manager
   ```

3. 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

4. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

5. 创建功能分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### 开发规范

- 遵循PEP 8代码风格
- 添加适当的注释和文档字符串
- 编写单元测试（如果适用）
- 确保代码通过所有测试

#### 提交代码

1. 添加您的更改：
   ```bash
   git add .
   ```

2. 提交更改：
   ```bash
   git commit -m "feat: 添加新功能描述"
   ```

3. 推送到您的fork：
   ```bash
   git push origin feature/your-feature-name
   ```

4. 创建Pull Request

### 3. 代码审查

- 所有代码更改都需要通过Pull Request
- 至少需要一名维护者审查并批准
- 确保所有CI检查通过

## 开发指南

### 项目结构

```
12306-ticket-manager/
├── ticket/              # 车票管理模块
│   ├── __init__.py
│   ├── models.py        # 数据库模型
│   └── ticket_parser.py # 车票信息解析
├── tools/               # 工具模块
│   └── mail.py         # 邮件处理
├── static/              # 静态文件
│   └── index.html      # Web界面
├── docs/                # 文档
├── examples/            # 示例
├── scripts/             # 脚本
├── main.py             # 主应用
├── config.py           # 配置文件
└── requirements.txt    # 依赖列表
```

### 代码风格

- 使用4个空格缩进
- 行长度不超过120字符
- 使用有意义的变量和函数名
- 添加类型注解（Python 3.7+）

### 测试

运行测试：
```bash
python -m pytest tests/
```

### 文档

- 更新README.md（如果需要）
- 更新API文档（如果修改了API）
- 添加代码注释

## 提交信息规范

使用[约定式提交](https://www.conventionalcommits.org/zh-hans/)格式：

- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

示例：
```
feat: 添加邮件通知功能
fix: 修复车票解析错误
docs: 更新API文档
```

## 行为准则

- 尊重所有贡献者
- 保持专业和友好的交流
- 欢迎新手贡献者
- 提供建设性的反馈

## 许可证

通过提交代码，您同意您的贡献将在MIT许可证下发布。

## 联系方式

如果您有任何问题，请通过以下方式联系：

- 创建GitHub Issue
- 发送邮件到项目维护者

感谢您的贡献！🎉 