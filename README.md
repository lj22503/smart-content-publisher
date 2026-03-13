# 智能内容分发助手 v3.0 MVP

🚀 一站式内容创作与分发工具，支持智能改写（去AI化）和多平台自动分发。

## ✨ 功能特性

- 🤖 **智能改写引擎**: 去除AI腔调，转换为自然口语化表达
- 📱 **多平台分发**: 支持微信公众号、飞书、小红书
- 🎨 **现代化UI**: Streamlit暗黑主题界面，三栏布局
- 🔄 **平台适配**: 根据各平台特性自动调整内容风格
- 🔒 **本地运行**: 所有密钥仅保存在本地，安全可靠

## 📸 界面预览

```
┌─────────────────────────────────────────────────────────────┐
│  [Sidebar]  │              [Main Content Area]               │
│             │                                                │
│  🚀 Logo    │  ┌──────────┬──────────┬──────────┐           │
│  平台配置    │  │  源内容   │  小红书   │  公众号   │           │
│  - 微信     │  │          │  预览     │  预览     │           │
│  - 飞书     │  │          │          │          │           │
│  - 小红书   │  │  输入区   │  改写后   │  改写后   │           │
│             │  │          │  内容     │  内容     │           │
│             │  └──────────┴──────────┴──────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 快速开始

### 方式一：直接运行（推荐开发）

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/smart-content-publisher.git
cd smart-content-publisher/v3_mvp

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. 安装依赖
pip install -r requirements.txt
playwright install chromium

# 4. 启动应用
streamlit run main.py
# 或使用启动脚本
启动.bat
```

### 方式二：打包为可执行文件（推荐用户使用）

```bash
# 安装打包依赖
pip install pyinstaller

# 打包为目录版（推荐，启动更快）
python build_exe.py --mode onedir

# 或打包为单文件
python build_exe.py --mode onefile

# 可执行文件将生成在 dist/ 目录下
```

## 📱 平台配置说明

### 微信公众号

1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 开发 → 基本配置 → 获取AppID和AppSecret
3. 添加IP白名单（你的服务器IP或本地IP）
4. 在应用侧边栏填入AppID和AppSecret

### 飞书

1. 登录 [飞书开放平台](https://open.feishu.cn)
2. 创建企业自建应用
3. 获取App ID和App Secret
4. 申请权限：云文档、文档编辑
5. 在应用侧边栏填入AppID和AppSecret

### 小红书

1. 安装Chrome浏览器
2. 启动Chrome调试模式：
   ```bash
   # Windows
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222

   # Mac
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   ```
3. 在Chrome中登录小红书网页版
4. 点击应用中的"测试浏览器连接"按钮

⚠️ **注意**: 小红书使用浏览器自动化，存在封号风险，建议使用小号测试

## 🛠️ 技术栈

- **Python 3.8+**
- **Streamlit**: Web界面框架
- **Playwright**: 浏览器自动化
- **Requests**: HTTP请求

## 📁 项目结构

```
v3_mvp/
├── main.py                 # 应用入口
├── requirements.txt        # 依赖列表
├── test_integration.py     # 联调测试脚本
├── build_exe.py           # 打包脚本
├── 启动.bat               # Windows启动脚本
├── docs/
│   └── ui_design_spec.md   # UI设计规范
├── ui/
│   └── app.py             # Streamlit主界面
├── platforms/
│   ├── wechat.py          # 微信公众号API
│   ├── feishu.py          # 飞书API
│   └── xiaohongshu.py     # 小红书Playwright
└── rewriter/
    └── ai_humanizer.py    # 去AI化改写引擎
```

## 🧪 运行测试

```bash
python test_integration.py
```

测试结果：
- ✅ 基础改写功能
- ✅ 小红书风格改写
- ✅ 公众号风格改写
- ✅ 微信HTML转换
- ✅ 飞书Blocks转换
- ✅ 小红书内容适配

## 🔄 GitHub推送指南

如果你还没有推送到GitHub，请按以下步骤操作：

### 1. 在GitHub上创建新仓库

访问 https://github.com/new 创建新仓库，名称建议：`smart-content-publisher`

### 2. 推送代码到GitHub

```bash
# 添加远程仓库（替换为你的GitHub用户名）
git remote add origin https://github.com/yourusername/smart-content-publisher.git

# 推送代码
git branch -M main
git push -u origin main
```

### 3. 设置GitHub Actions（可选）

本仓库已配置GitHub Actions工作流，推送后会自动构建可执行文件：

- 每次推送或PR时自动构建
- 创建Release时自动上传构建产物

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📝 更新日志

### v3.0 (2026-03-13)
- ✅ 初始版本发布
- ✅ 智能改写引擎
- ✅ 微信公众号API接入
- ✅ 飞书API接入
- ✅ 小红书Playwright自动化
- ✅ 现代化Web界面

---

**Made with ❤️ by Claude Code Assistant**
