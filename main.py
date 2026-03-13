#!/usr/bin/env python3
"""
智能内容分发助手 v3.0 MVP
Streamlit版本 - 现代化Web界面
"""

import streamlit as st
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from ui.app import main

if __name__ == "__main__":
    main()
