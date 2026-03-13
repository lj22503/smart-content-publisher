# 智能内容分发助手 v3.0 MVP

## 快速开始

### 1. 安装依赖
```bash
cd v3_mvp
pip install -r requirements.txt
playwright install chromium
```

### 2. 启动应用
```bash
streamlit run main.py
```

### 3. 配置平台密钥
在侧边栏中配置各平台的AppID和AppSecret

## 平台配置说明

### 微信公众号
1. 登录 https://mp.weixin.qq.com
2. 开发 → 基本配置 → 获取AppID和AppSecret
3. 添加IP白名单

### 飞书
1. 登录 https://open.feishu.cn
2. 创建企业自建应用
3. 获取App ID和App Secret
4. 申请云文档权限

### 小红书
1. 启动Chrome调试模式：
   ```bash
   chrome.exe --remote-debugging-port=9222
   ```
2. 在Chrome中登录小红书
3. 工具会自动连接已登录的浏览器

## 注意事项
- 小红书使用浏览器自动化，存在封号风险，建议使用小号测试
- 知乎API暂未公开，此版本暂不支持
