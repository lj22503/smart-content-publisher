# GitHub推送指南

## 快速推送命令

### 1. 在GitHub上创建新仓库

访问 https://github.com/new

- Repository name: `smart-content-publisher` (或你喜欢的名称)
- Description: `智能内容分发助手 - 支持微信公众号、飞书、小红书的自动内容分发工具`
- 选择 Public 或 Private
- 不要初始化 README (我们已经有了)
- 点击 **Create repository**

### 2. 推送本地代码到GitHub

复制以下命令并在项目目录(v3_mvp)中执行：

```bash
# 添加远程仓库（替换 yourusername 为你的GitHub用户名）
git remote add origin https://github.com/yourusername/smart-content-publisher.git

# 推送代码到main分支
git branch -M main
git push -u origin main
```

### 3. 验证推送

推送成功后，访问：
```
https://github.com/yourusername/smart-content-publisher
```

## 使用SSH方式推送（推荐）

如果你配置了SSH密钥，可以使用：

```bash
# 添加远程仓库（SSH方式）
git remote add origin git@github.com:yourusername/smart-content-publisher.git

# 推送代码
git branch -M main
git push -u origin main
```

## GitHub Actions 自动构建

推送代码后，GitHub Actions会自动运行：

1. 点击仓库的 **Actions** 标签
2. 查看 **Build Executable** 工作流
3. 等待构建完成（约5-10分钟）
4. 在 **Actions** → 最新运行 → **Artifacts** 中下载可执行文件

## 创建Release版本

如果你想发布正式版本：

```bash
# 创建标签
git tag -a v3.0.0 -m "Release version 3.0.0"

# 推送标签到GitHub
git push origin v3.0.0
```

推送标签后，GitHub Actions会自动创建Release并上传构建产物。

## 后续更新代码

```bash
# 查看修改
git status

# 添加修改的文件
git add .

# 提交修改
git commit -m "描述你的修改"

# 推送到GitHub
git push origin main
```

## 常见问题

### Q: 推送时提示 "fatal: Authentication failed"
A: 你需要配置GitHub凭证：
- 使用HTTPS：输入GitHub用户名和个人访问令牌(PAT)
- 使用SSH：确保SSH密钥已添加到GitHub账户

### Q: 如何生成GitHub个人访问令牌？
A: GitHub Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token

### Q: 推送时提示 "rejected: non-fast-forward"
A: 先执行 `git pull origin main` 拉取远程更新，解决冲突后再推送
