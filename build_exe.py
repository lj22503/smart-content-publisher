"""
智能内容分发助手 - 打包脚本
使用PyInstaller打包为可执行文件
"""

import PyInstaller.__main__
import os
import sys
from pathlib import Path

def build_executable():
    """打包应用为可执行文件"""

    # 获取当前目录
    base_dir = Path(__file__).parent.absolute()

    # 主入口文件
    main_script = base_dir / "main.py"

    # 图标文件（如果有的话）
    # icon_file = base_dir / "assets" / "icon.ico"

    # PyInstaller参数
    args = [
        str(main_script),
        "--name=智能内容分发助手",
        "--onefile",  # 打包为单个文件
        "--windowed",  # 无控制台窗口
        "--clean",  # 清理临时文件
        "--noconfirm",  # 不确认覆盖

        # 隐藏导入
        "--hidden-import=streamlit",
        "--hidden-import=streamlit.runtime.scriptrunner.magic_funcs",
        "--hidden-import=rewriter.ai_humanizer",
        "--hidden-import=platforms.wechat",
        "--hidden-import=platforms.feishu",
        "--hidden-import=platforms.xiaohongshu",

        # 数据文件
        f"--add-data={base_dir}/ui{os.pathsep}ui",
        f"--add-data={base_dir}/platforms{os.pathsep}platforms",
        f"--add-data={base_dir}/rewriter{os.pathsep}rewriter",

        # 输出目录
        f"--distpath={base_dir}/dist",
        f"--workpath={base_dir}/build",
        f"--specpath={base_dir}",
    ]

    # 如果有图标则添加
    # if icon_file.exists():
    #     args.append(f"--icon={icon_file}")

    print("=" * 50)
    print("开始打包智能内容分发助手...")
    print("=" * 50)

    try:
        PyInstaller.__main__.run(args)
        print("\n" + "=" * 50)
        print("打包完成！")
        print(f"可执行文件位于: {base_dir}/dist/")
        print("=" * 50)
        return True
    except Exception as e:
        print(f"\n打包失败: {e}")
        return False


def build_directory_version():
    """打包为目录版本（启动更快，文件更小）"""

    base_dir = Path(__file__).parent.absolute()
    main_script = base_dir / "main.py"

    args = [
        str(main_script),
        "--name=智能内容分发助手",
        "--onedir",  # 打包为目录
        "--windowed",
        "--clean",
        "--noconfirm",

        "--hidden-import=streamlit",
        "--hidden-import=streamlit.runtime.scriptrunner.magic_funcs",
        "--hidden-import=rewriter.ai_humanizer",
        "--hidden-import=platforms.wechat",
        "--hidden-import=platforms.feishu",
        "--hidden-import=platforms.xiaohongshu",

        f"--add-data={base_dir}/ui{os.pathsep}ui",
        f"--add-data={base_dir}/platforms{os.pathsep}platforms",
        f"--add-data={base_dir}/rewriter{os.pathsep}rewriter",

        f"--distpath={base_dir}/dist",
        f"--workpath={base_dir}/build",
        f"--specpath={base_dir}",
    ]

    print("=" * 50)
    print("开始打包智能内容分发助手（目录版）...")
    print("=" * 50)

    try:
        PyInstaller.__main__.run(args)
        print("\n" + "=" * 50)
        print("打包完成！")
        print(f"可执行文件位于: {base_dir}/dist/智能内容分发助手/")
        print("=" * 50)
        return True
    except Exception as e:
        print(f"\n打包失败: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="打包智能内容分发助手")
    parser.add_argument(
        "--mode",
        choices=["onefile", "onedir"],
        default="onedir",
        help="打包模式: onefile(单文件) 或 onedir(目录版，推荐)"
    )

    args = parser.parse_args()

    if args.mode == "onefile":
        build_executable()
    else:
        build_directory_version()
