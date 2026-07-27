# smart-content-publisher — neat-freak 知识收尾报告

**收尾时间**：2026-07-25
**收闭路径**：轻量路径（Python + Streamlit + PyInstaller 桌面发布工具，已有 recent neat-freak 风格 commit `6d29f78` PyInstaller 配置修复，HEAD 干净）
**收尾者**：neat-freak（v3.0.0）

---

## 一、影响（用户视角）

- **🔴 2 个 .bak 备份文件仍 commit 进 git**：
  - `README.md.bak` (5.8KB)
  - `publish_to_github_fixed.py.bak` (8.3KB)
  → 同款 .md.bak / .py.bak 备份格式（与 idx 22 investment-buddy-pet 的 `SKILL.md.backup` 同款）。
  → 按 neat-freak §4 "备份副本"分类，列入**删除候选**。
- **🔴 第 8 处双 publish 脚本**：
  - `publish_to_github.py` (8.3KB)
  - `publish_to_github_fixed.py` (8.3KB) **同名不同后缀**（无 _fixed 后缀 vs 有 _fixed 后缀）
  → 双胞胎现象（**累计第 8 处**）。
  → 推测：`publish_to_github_fixed.py` 是 `publish_to_github.py` 的修复版——是否已替换 / 哪个是当前？
- **整体良好**：命名一致、6 个 Python 脚本 + 4 个子目录结构、Streamlit + PyInstaller 桌面应用、有 .bat 启动脚本（一键发布到 GitHub）、GitHub Actions。

## 二、现役事实矩阵

| 事实面 | 状态 | 证据 |
|--------|------|------|
| 代码 | `verified-current` | main.py (309B 入口) + build_exe.py (6.4KB PyInstaller 打包) + publish_to_github.py + publish_to_github_fixed.py（双份）+ test_integration.py (9.9KB) |
| 运行态 | `verified-current` | HEAD `6d29f78` PyInstaller 配置修复；最近 5 commit 全是 fix（GitHub Actions + PyInstaller + Node.js 24 兼容 + 编码问题） |
| 文档 | `verified-current` | README.md 6.4KB + 发布指南.md 7KB + docs/ui_design_spec.md |
| 规则 | `not-applicable` | 无 CLAUDE.md / AGENTS.md |
| 记忆 | `not-applicable` | 无 |
| 工作区 | `verified-current` | 新建 `.neat-freak/`；HEAD 干净 |

## 三、关键发现

### 3.1 🔴 2 个 .bak 备份文件（累计 .md.bak / .py.bak 第 2 处）

| 文件 | 尺寸 | 类型 |
|------|------|------|
| `README.md.bak` | 5.8KB | 文档备份 |
| `publish_to_github_fixed.py.bak` | 8.3KB | 代码备份 |

→ 同款 `.bak` 后缀格式（与 idx 22 investment-buddy-pet 的 `SKILL.md.backup` 类似）。
→ 推测：上次 README/脚本修复时手动备份，未删除。
→ 处置：
- 选项 A：删除 `.bak` 文件（恢复成上一版本/对照选择保留）
- 选项 B：保留作历史快照

### 3.2 🔴 第 8 处 publish 脚本双胞胎

| 文件 | 命名 |
|------|------|
| `publish_to_github.py` | 原版 |
| `publish_to_github_fixed.py` | "fixed" 后缀（推测修复版） |

→ 累计"配置/代码双胞胎"现象 8 处：idx 2/17/18/20/21/24/32/37。
→ 处置：
- 选项 A：删除 `publish_to_github.py`（保留 `_fixed` 版）
- 选项 B：删除 `publish_to_github_fixed.py`（保留原版）
- 选项 C：保留双份（接受维护成本）

### 3.3 完整 Python 项目结构

```
smart-content-publisher/
├── main.py                    # Streamlit UI 入口（309B）
├── build_exe.py              # PyInstaller 打包（6.4KB）
├── publish_to_github.py      # GitHub 发布（双胞胎）
├── publish_to_github_fixed.py # GitHub 发布 fixed 版
├── publish_to_github_fixed.py.bak  # 备份
├── test_integration.py       # 集成测试（9.9KB）
├── 一键发布到GitHub.bat        # Windows 一键发布
├── 启动.bat                   # Windows 启动
├── requirements.txt
├── README.md + README.md.bak
├── 发布指南.md
├── docs/ui_design_spec.md
├── fund_investment_course/   # 投教课程模块
├── platforms/                # 多平台发布适配
├── rewriter/                 # 内容改写模块
└── ui/                       # UI 组件
```

### 3.4 最近 5 commit 全是 fix

```
6d29f78 fix: improve PyInstaller configuration for Streamlit
e8de0e7 fix: improve PyInstaller configuration for Streamlit app
7640770 fix: update GitHub Actions to latest versions and fix Node.js 24 compatibility
09f12de fix: GitHub Actions build issues
222ba03 Update GitHub publish scripts and fix encoding issues
```

→ 关键决策 `222ba03` "Update GitHub publish scripts and fix encoding issues" —— 这可能解释了 `publish_to_github_fixed.py` 的诞生。
→ 关键决策 `7640770` "GitHub Actions to latest versions" —— GitHub Actions 自动构建。

### 3.5 项目定位

按 README.md + 文件名推测：
- **核心功能**：智能内容发布（智能改写 + 多平台发布）
- **目标用户**：内容创作者（含金融投教课程内容）
- **部署形态**：Streamlit + PyInstaller 打包桌面应用（不是 Web 服务）

### 3.6 双 .bat 启动脚本

| 文件 | 用途 |
|------|------|
| `一键发布到GitHub.bat` | Windows 一键发布到 GitHub（推测调用 publish_to_github_fixed.py） |
| `启动.bat` | Windows 启动 UI（推测调用 main.py） |

→ Windows 友好（与 idx 22 investment-buddy-pet 同款）。

### 3.7 4 个子目录

| 目录 | 用途（推测） |
|------|------------|
| `fund_investment_course/` | 投教课程内容 |
| `platforms/` | 多平台适配（小红书/公众号/知乎 等） |
| `rewriter/` | 内容改写引擎 |
| `ui/` | Streamlit UI 组件 |

→ 与 idx 19 finops-Toolkit 的 4 模块架构（Router/Orchestrator/DocGenerator/FeedbackLearner）形似但不同：
- smart-content-publisher：内容输入 → 改写 → 发布
- finops-Toolkit：Skill 输入 → 路由 → 输出

### 3.8 docs/ui_design_spec.md

| 属性 | 推测 |
|------|------|
| UI 设计规范文档 | Streamlit 界面布局 + 颜色 + 组件规范 |

### 3.9 命名一致 ✅

| 维度 | 名字 |
|------|------|
| 本地目录 | `smart-content-publisher` |
| GitHub remote | `lj22503/smart-content-publisher` |
| package.json name | （无 package.json，是 Python 项目） |

### 3.10 与 idx 27 investor-education-workflow 对照

| 维度 | smart-content-publisher（idx 37） | investor-education-workflow（idx 27） |
|------|----------------------------------|--------------------------------------|
| 形态 | Python + Streamlit + PyInstaller 桌面 | 纯 Markdown Skill 包 |
| 输出 | 多平台发布（公众号/小红书等） | 投教内容生成（5 大模块） |
| 自动化 | publish_to_github.py 自动发布 | 需手动调用 LLM |
| 5 大模块 | 无（推测 4 子目录） | 有（基本功/风险/行为/规划/陪伴） |

→ 两项目主题接近（都做投教/内容生产），但智能内容发布工具比纯 Skill 包"实操性"更强。

### 3.11 项目矩阵定位

| 关联 | 来源 |
|------|------|
| 与 finops-Toolkit 主题 | 内容生产（创作+合规+多渠道分发） |
| 与 betterlife 主题 | 财商教育（fund_investment_course/ 子目录） |
| 与 investor-education-workflow 主题 | 投教内容生成 |
| 与 contexts-manager 主题 | 改写引擎（rewriter/） |

→ smart-content-publisher 是**多个 Skill 项目的"执行终端"**。

## 四、改动 / 新建

| 文件 | 动作 | 原因 |
|------|------|------|
| `.neat-freak/reports/smart-content-publisher-2026-07-24.md` | 新建 | 本次 audit trail |

## 五、待你确认（未确认前不动作）

1. **🔴 .bak 文件删除**：README.md.bak + publish_to_github_fixed.py.bak
2. **🔴 publish 双胞胎处置**：选保留 publish_to_github.py 还是 publish_to_github_fixed.py
3. **GitHub Actions 配置**：与 publish 脚本关系确认（GitHub Actions 调用哪个脚本？）

## 六、遗留

- main.py 仅 309B 推测仅做入口转发
- publish_to_github.py + publish_to_github_fixed.py 内容差异未对比
- build_exe.py 6.4KB 实际 PyInstaller 配置未读
- 4 个子目录（fund_investment_course / platforms / rewriter / ui）实际内容未审
- 发布指南.md 7KB 全文未读

---

*收尾完成度：5 事实面已标注（记忆 not-applicable，规则 not-applicable 缺文件）。报告基于 commit `6d29f78`（HEAD，分支 main）。如需重新跑请清空 `.neat-freak/reports/` 后重跑。*