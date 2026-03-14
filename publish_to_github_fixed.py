#!/usr/bin/env python3
"""
智能内容分发助手 - GitHub自动发布脚本
"""

import os
import sys
import subprocess
import shlex
from pathlib import Path


def run_command(cmd: str, cwd: str = None) -> tuple[int, str, str]:
    """运行shell命令并返回结果"""
    try:
        process = subprocess.Popen(
            shlex.split(cmd) if sys.platform != "win32" else cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            text=True,
            shell=(sys.platform == "win32")
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout.strip(), stderr.strip()
    except Exception as e:
        return -1, "", str(e)


def check_git_installed() -> bool:
    """检查Git是否已安装"""
    code, stdout, stderr = run_command("git --version")
    if code == 0:
        print("[OK] Git已安装:", stdout)
        return True
    else:
        print("[ERR] Git未安装或不可用")
        print("请先安装Git: https://git-scm.com/downloads")
        return False


def check_git_config() -> bool:
    """检查Git配置"""
    print("\n[INFO] 检查Git配置...")

    # 检查用户名
    code, username, _ = run_command("git config user.name")
    if code != 0 or not username:
        print("[WARN]  Git用户名未配置")
        username = input("请输入Git用户名: ").strip()
        if username:
            run_command(f'git config user.name "{username}"')
        else:
            print("[ERR] 必须配置Git用户名")
            return False

    # 检查邮箱
    code, email, _ = run_command("git config user.email")
    if code != 0 or not email:
        print("[WARN]  Git邮箱未配置")
        email = input("请输入Git邮箱: ").strip()
        if email:
            run_command(f'git config user.email "{email}"')
        else:
            print("[ERR] 必须配置Git邮箱")
            return False

    print(f"[OK] Git配置完成: {username} <{email}>")
    return True


def get_github_username() -> str:
    """获取GitHub用户名"""
    print("\n[LINK] 配置GitHub仓库")
    print("=" * 50)

    username = input("请输入你的GitHub用户名: ").strip()
    if not username:
        print("[ERR] 必须提供GitHub用户名")
        sys.exit(1)

    # 验证用户名格式
    if " " in username or "/" in username:
        print("[ERR] GitHub用户名不能包含空格或斜杠")
        sys.exit(1)

    return username


def add_github_remote(username: str) -> bool:
    """添加GitHub远程仓库"""
    print("\n[UPLOAD] 添加远程仓库...")

    # 检查是否已存在远程仓库
    code, stdout, _ = run_command("git remote -v")
    if "origin" in stdout:
        print("[OK] 远程仓库已配置:")
        print(stdout)

        # 询问是否要更新
        response = input("是否要更新远程仓库URL? (y/N): ").strip().lower()
        if response != "y":
            return True

        # 移除现有远程仓库
        run_command("git remote remove origin")

    # 添加新的远程仓库
    repo_url = f"https://github.com/{username}/smart-content-publisher.git"
    print(f"[BOX] 仓库URL: {repo_url}")

    code, _, stderr = run_command(f'git remote add origin "{repo_url}"')
    if code != 0:
        print(f"[ERR] 添加远程仓库失败: {stderr}")
        return False

    print("[OK] 远程仓库添加成功")
    return True


def create_github_repo_instructions(username: str):
    """显示创建GitHub仓库的指引"""
    print("\n[NOTE] 创建GitHub仓库指引")
    print("=" * 50)
    print("请按以下步骤创建GitHub仓库:")
    print()
    print("1. 访问: https://github.com/new")
    print("2. 填写仓库信息:")
    print(f"   - Repository name: smart-content-publisher")
    print("   - Description: 智能内容分发助手 - 支持微信公众号、飞书、小红书的自动内容分发工具")
    print("   - 选择 Public (公开) 或 Private (私有)")
    print("   - 不要勾选 'Add a README file' (我们已经有了)")
    print("   - 点击 Create repository")
    print()
    print("3. 创建完成后，返回到此窗口按回车继续")
    input("按回车继续... ")


def push_to_github() -> bool:
    """推送代码到GitHub"""
    print("\n[ROCKET] 推送代码到GitHub...")

    # 切换到main分支
    code, _, stderr = run_command("git branch -M main")
    if code != 0:
        print(f"[ERR] 切换到main分支失败: {stderr}")
        return False

    # 推送代码
    print("[SYNC] 正在推送代码...")
    code, stdout, stderr = run_command("git push -u origin main")
    if code != 0:
        print(f"[ERR] 推送失败: {stderr}")

        # 如果是认证失败，给出建议
        if "Authentication failed" in stderr or "fatal: invalid credentials" in stderr:
            print("\n[KEY] 认证失败解决方案:")
            print("1. 确保GitHub仓库已创建")
            print("2. 如果使用双因素认证，需要使用个人访问令牌(PAT)")
            print("3. 生成PAT: GitHub Settings → Developer settings → Personal access tokens")
            print("4. 推送时使用PAT代替密码")
            print("\n或者，你可以手动执行:")
            print("  git push -u origin main")

        return False

    print("[OK] 代码推送成功！")
    print(stdout)
    return True


def create_release_tag() -> bool:
    """创建发布标签"""
    print("\n[TAG]  创建发布标签...")

    response = input("是否要创建v3.0.0发布标签? (y/N): ").strip().lower()
    if response != "y":
        print("跳过标签创建")
        return True

    # 创建标签
    code, _, stderr = run_command('git tag -a v3.0.0 -m "Release version 3.0.0 - Initial MVP"')
    if code != 0:
        print(f"[ERR] 创建标签失败: {stderr}")
        return False

    # 推送标签
    print("推送标签到GitHub...")
    code, stdout, stderr = run_command("git push origin v3.0.0")
    if code != 0:
        print(f"[ERR] 推送标签失败: {stderr}")
        return False

    print("[OK] 标签创建并推送成功！")
    print("GitHub Actions会自动构建可执行文件并创建Release")
    return True


def show_next_steps(username: str):
    """显示下一步指引"""
    print("\n[CELEBRATE] GitHub发布完成！")
    print("=" * 50)
    print("[OK] 代码已推送到GitHub")
    print(f"[FOLDER] 仓库地址: https://github.com/{username}/smart-content-publisher")
    print()
    print("[INFO] 下一步操作:")
    print("1. 访问你的GitHub仓库查看代码")
    print("2. 进入 Actions 标签查看自动构建状态")
    print("3. 构建完成后可以下载可执行文件")
    print("4. 如果需要创建Release，手动创建或推送标签")
    print()
    print("[TOOL] 使用方式:")
    print("  直接运行: streamlit run main.py")
    print("  打包使用: python build_exe.py --mode onedir")
    print()
    print("[PHONE] 如有问题，请查看 README.md 和 发布指南.md")


def main():
    """主函数"""
    print("=" * 60)
    print("智能内容分发助手 - GitHub自动发布工具")
    print("=" * 60)

    # 获取项目目录
    project_dir = Path(__file__).parent.absolute()
    print(f"[DIR] 项目目录: {project_dir}")

    # 检查Git
    if not check_git_installed():
        sys.exit(1)

    # 检查Git配置
    if not check_git_config():
        sys.exit(1)

    # 获取GitHub用户名
    username = get_github_username()

    # 显示创建仓库指引
    create_github_repo_instructions(username)

    # 添加远程仓库
    if not add_github_remote(username):
        sys.exit(1)

    # 推送代码
    if not push_to_github():
        sys.exit(1)

    # 创建发布标签
    create_release_tag()

    # 显示下一步指引
    show_next_steps(username)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[STOP]  用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERR] 发生错误: {e}")
        sys.exit(1)
