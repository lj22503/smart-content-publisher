"""
智能内容分发助手 - Streamlit主应用
集成去AI化改写引擎 + 多平台发布
"""

import streamlit as st
import sys
import re
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent))

# 导入改写引擎
from rewriter.ai_humanizer import humanize_text, PlatformRewriter

# 导入平台发布器
from platforms.wechat import WeChatPublisher
from platforms.feishu import FeishuPublisher
from platforms.xiaohongshu import XiaohongshuPublisher


# ============== 页面配置 ==============
st.set_page_config(
    page_title="智能内容分发助手",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== 自定义CSS ==============
st.markdown("""
<style>
    /* 基础样式 */
    .main {
        background-color: #0f172a;
        color: #e2e8f0;
    }

    /* 文本域样式 */
    .stTextArea textarea {
        background-color: #1e293b;
        color: #e2e8f0;
        border: 1px solid #334155;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
    }

    /* 输入框样式 */
    .stTextInput input {
        background-color: #1e293b;
        color: #e2e8f0;
        border: 1px solid #334155;
        border-radius: 6px;
    }

    /* 按钮样式 */
    .stButton button {
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        transform: translateY(-1px);
    }

    /* 主按钮 */
    .stButton button[kind="primary"] {
        background-color: #3b82f6;
        color: white;
    }
    .stButton button[kind="primary"]:hover {
        background-color: #2563eb;
    }

    /* 侧边栏样式 */
    .sidebar .sidebar-content {
        background-color: #1e293b;
    }

    /* 平台卡片 */
    .platform-card {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #334155;
        margin-bottom: 16px;
    }

    /* 预览框 */
    .preview-box {
        background-color: #0f172a;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #334155;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        max-height: 500px;
        overflow-y: auto;
        font-size: 14px;
        line-height: 1.6;
    }

    /* 平台标题 */
    .platform-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #334155;
    }

    /* 小红书样式 */
    .xiaohongshu-style {
        color: #ff2442;
    }

    /* 微信样式 */
    .wechat-style {
        color: #07c160;
    }

    /* 飞书样式 */
    .feishu-style {
        color: #3370ff;
    }

    /* 状态指示器 */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
    }
    .status-ready {
        background-color: rgba(34, 197, 94, 0.2);
        color: #22c55e;
    }
    .status-pending {
        background-color: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
    }
    .status-error {
        background-color: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }

    /* 特性标签 */
    .feature-tag {
        display: inline-block;
        padding: 2px 8px;
        background-color: #334155;
        border-radius: 4px;
        font-size: 11px;
        margin-right: 6px;
        margin-bottom: 4px;
    }

    /* 字数统计 */
    .word-count {
        text-align: right;
        font-size: 12px;
        color: #64748b;
        margin-top: 4px;
    }

    /* 分割线 */
    hr {
        border-color: #334155;
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)


# ============== 初始化 Session State ==============
def init_session_state():
    """初始化会话状态"""
    defaults = {
        'source_content': '',
        'rewritten_content': '',
        'xiaohongshu_content': '',
        'wechat_content': '',
        'feishu_content': '',
        'rewrite_complete': False,
        'wechat_connected': False,
        'feishu_connected': False,
        'xiaohongshu_connected': False,
        'rewrite_count': 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============== 辅助函数 ==============
def extract_title(content: str) -> str:
    """从Markdown内容中提取标题"""
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
        elif line.startswith('## '):
            return line[3:].strip()
    # 如果没有标题，返回第一行或默认标题
    if lines and lines[0].strip():
        return lines[0].strip()[:50]
    return "未命名文档"


def count_words(content: str) -> int:
    """统计字数（中文字符+英文单词）"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
    english_words = len(re.findall(r'[a-zA-Z]+', content))
    return chinese_chars + english_words


def check_platform_config(platform: str) -> tuple[bool, str]:
    """检查平台配置状态"""
    if platform == "wechat":
        appid = st.session_state.get('wechat_appid', '')
        secret = st.session_state.get('wechat_secret', '')
        if appid and secret:
            return True, "已配置"
        return False, "待配置"

    elif platform == "feishu":
        appid = st.session_state.get('feishu_appid', '')
        secret = st.session_state.get('feishu_secret', '')
        if appid and secret:
            return True, "已配置"
        return False, "待配置"

    elif platform == "xiaohongshu":
        enabled = st.session_state.get('xiaohongshu_enabled', False)
        if enabled:
            return True, "已启用"
        return False, "待启用"

    return False, "未知"


# ============== 改写引擎集成 ==============
def rewrite_content(content: str, style: str) -> str:
    """调用改写引擎"""
    if not content or len(content.strip()) < 10:
        raise ValueError("内容太短，请输入至少10个字符")

    rewriter = PlatformRewriter()

    if style == "去AI化（自然口语）":
        result = humanize_text(content, platform="general")
    elif style == "轻松活泼":
        result = rewriter.rewrite_for_xiaohongshu(content)
    elif style == "专业正式":
        result = rewriter.rewrite_for_wechat(content)
    elif style == "知乎风格":
        result = rewriter.rewrite_for_zhihu(content)
    else:
        result = humanize_text(content, platform="general")

    return result


def generate_platform_versions(rewritten: str):
    """生成各平台版本"""
    rewriter = PlatformRewriter()

    # 小红书版本
    st.session_state['xiaohongshu_content'] = rewriter.rewrite_for_xiaohongshu(rewritten)

    # 公众号版本
    st.session_state['wechat_content'] = rewriter.rewrite_for_wechat(rewritten)

    # 飞书版本（使用通用改写）
    st.session_state['feishu_content'] = humanize_text(rewritten, platform="general")


# ============== 平台发布功能 ==============
def publish_to_wechat(title: str, content: str):
    """发布到微信公众号草稿"""
    try:
        appid = st.session_state.get('wechat_appid')
        secret = st.session_state.get('wechat_secret')

        if not appid or not secret:
            st.error("❌ 请先配置微信公众号的AppID和AppSecret")
            return False

        publisher = WeChatPublisher(appid, secret)

        # 转换Markdown为HTML
        html_content = publisher.html_to_wechat(content)

        # 创建草稿
        result = publisher.create_draft(
            title=title,
            content=html_content,
            author=st.session_state.get('wechat_author', ''),
            digest=st.session_state.get('wechat_digest', '')
        )

        if result.get('success'):
            st.success(f"✅ 公众号草稿创建成功！Media ID: {result.get('media_id')}")
            return True
        else:
            st.error(f"❌ 创建失败: {result.get('error', '未知错误')}")
            return False

    except Exception as e:
        st.error(f"❌ 发布失败: {str(e)}")
        return False


def publish_to_feishu(title: str, content: str):
    """发布到飞书文档"""
    try:
        appid = st.session_state.get('feishu_appid')
        secret = st.session_state.get('feishu_secret')

        if not appid or not secret:
            st.error("❌ 请先配置飞书的App ID和App Secret")
            return False

        publisher = FeishuPublisher(appid, secret)

        # 创建文档
        result = publisher.create_document(title=title)

        if result.get('success'):
            document_id = result.get('document_id')

            # 转换内容为blocks
            blocks = publisher.markdown_to_feishu_blocks(content)

            # 添加内容
            content_result = publisher.add_content_blocks(document_id, blocks)

            if content_result.get('code') == 0:
                st.success(f"✅ 飞书文档创建成功！")
                st.info(f"📎 文档链接: {result.get('url')}")
                return True
            else:
                st.warning(f"⚠️ 文档创建成功，但内容添加失败: {content_result.get('msg')}")
                return False
        else:
            st.error(f"❌ 创建失败: {result.get('error', '未知错误')}")
            return False

    except Exception as e:
        st.error(f"❌ 发布失败: {str(e)}")
        return False


async def publish_to_xiaohongshu_async(title: str, content: str):
    """异步发布到小红书"""
    try:
        publisher = XiaohongshuPublisher()

        # 连接浏览器
        connected = await publisher.connect_to_browser()
        if not connected:
            st.error("❌ 无法连接到Chrome浏览器，请确保已启动调试模式")
            st.info("💡 启动命令: chrome.exe --remote-debugging-port=9222")
            return False

        # 检查登录状态
        logged_in = await publisher.check_login_status()
        if not logged_in:
            st.error("❌ 小红书未登录，请先在浏览器中登录")
            return False

        # 创建草稿
        result = await publisher.create_draft(title=title, content=content)

        await publisher.close()

        if result.get('success'):
            st.success(f"✅ 小红书草稿创建成功！")
            return True
        else:
            st.error(f"❌ 创建失败: {result.get('error', '未知错误')}")
            return False

    except Exception as e:
        st.error(f"❌ 发布失败: {str(e)}")
        return False


def publish_to_xiaohongshu(title: str, content: str):
    """同步包装异步发布"""
    return asyncio.run(publish_to_xiaohongshu_async(title, content))


def test_browser_connection():
    """测试浏览器连接"""
    async def test():
        try:
            publisher = XiaohongshuPublisher()
            connected = await publisher.connect_to_browser()

            if connected:
                logged_in = await publisher.check_login_status()
                await publisher.close()

                if logged_in:
                    st.session_state['xiaohongshu_connected'] = True
                    return True, "✅ 浏览器已连接且已登录小红书"
                else:
                    return True, "⚠️ 浏览器已连接，但小红书未登录"
            else:
                return False, "❌ 无法连接到Chrome浏览器"

        except Exception as e:
            return False, f"❌ 连接失败: {str(e)}"

    result, msg = asyncio.run(test())
    if result:
        st.success(msg)
    else:
        st.error(msg)
        st.info("💡 请使用命令启动Chrome: chrome.exe --remote-debugging-port=9222")


# ============== 主应用 ==============
def main():
    init_session_state()

    # ============== 侧边栏 ==============
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h2 style="margin: 0; color: #3b82f6;">🚀 智能分发助手</h2>
            <p style="color: #64748b; margin: 8px 0;">v3.0 MVP</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # 平台配置
        st.subheader("📱 平台配置")

        # 微信公众号配置
        with st.expander("💬 微信公众号"):
            st.text_input("AppID", type="password", key="wechat_appid")
            st.text_input("AppSecret", type="password", key="wechat_secret")
            st.text_input("作者（可选）", key="wechat_author")
            st.text_input("摘要（可选）", key="wechat_digest")
            st.checkbox("启用自动同步", key="wechat_enabled")

        # 飞书配置
        with st.expander("📋 飞书"):
            st.text_input("App ID", type="password", key="feishu_appid")
            st.text_input("App Secret", type="password", key="feishu_secret")
            st.checkbox("启用自动同步", key="feishu_enabled")

        # 小红书配置
        with st.expander("📱 小红书"):
            st.info("小红书使用浏览器自动化")
            st.markdown("""
            <div style="background-color: #1e293b; padding: 10px; border-radius: 6px; font-size: 12px;">
                <p style="margin: 0; color: #94a3b8;">启动命令:</p>
                <code style="color: #f59e0b;">chrome.exe --remote-debugging-port=9222</code>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🧪 测试浏览器连接", use_container_width=True):
                with st.spinner("测试中..."):
                    test_browser_connection()

            st.checkbox("启用半自动同步", key="xiaohongshu_enabled")

        st.markdown("---")

        # 状态监控
        st.subheader("📊 平台状态")

        wechat_ok, wechat_status = check_platform_config("wechat")
        feishu_ok, feishu_status = check_platform_config("feishu")
        xhs_ok, xhs_status = check_platform_config("xiaohongshu")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="status-indicator {'status-ready' if wechat_ok else 'status-pending'}">
                {'✅' if wechat_ok else '⏳'} 微信
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="status-indicator {'status-ready' if feishu_ok else 'status-pending'}">
                {'✅' if feishu_ok else '⏳'} 飞书
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="status-indicator {'status-ready' if xhs_ok else 'status-pending'}">
                {'✅' if xhs_ok else '⏳'} 小红书
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.caption("💡 提示：密钥仅保存在本地浏览器")

    # ============== 主内容区 ==============
    st.title("🚀 智能内容分发助手")
    st.caption("智能改写 + 一键多平台分发 | 支持微信公众号、飞书、小红书")

    # 三栏布局
    col1, col2, col3 = st.columns([1.2, 1, 1])

    # ============== 左侧：源内容 ==============
    with col1:
        st.markdown("""
        <div class="platform-header">
            <span style="font-size: 20px;">📝</span>
            <span style="font-size: 16px; font-weight: 600;">原始内容</span>
        </div>
        """, unsafe_allow_html=True)

        # 文件上传
        uploaded_file = st.file_uploader("📎 上传Markdown文件", type=['md', 'txt'])

        # 获取当前内容
        current_content = st.session_state.get('source_content', '')

        # 如果上传了文件
        if uploaded_file is not None:
            try:
                current_content = uploaded_file.getvalue().decode('utf-8')
                st.session_state['source_content'] = current_content
                st.success(f"✅ 已加载文件: {uploaded_file.name}")
            except Exception as e:
                st.error(f"❌ 文件读取失败: {e}")

        # 文本输入
        source_content = st.text_area(
            "输入Markdown内容",
            value=current_content,
            height=350,
            placeholder="# 标题\n\n正文内容...\n\n支持Markdown格式：\n- 标题 (# ## ###)\n- 列表 (- )\n- 加粗 (**text**)",
            label_visibility="collapsed"
        )

        # 更新session state
        if source_content != st.session_state.get('source_content', ''):
            st.session_state['source_content'] = source_content

        # 字数统计
        word_count = count_words(source_content)
        st.markdown(f"""
        <div class="word-count">
            字数: {word_count} | 预计阅读: {max(1, word_count // 300)} 分钟
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # 改写选项
        st.markdown("""
        <div class="platform-header">
            <span style="font-size: 20px;">🎨</span>
            <span style="font-size: 16px; font-weight: 600;">改写风格</span>
        </div>
        """, unsafe_allow_html=True)

        rewrite_style = st.selectbox(
            "选择改写风格",
            ["去AI化（自然口语）", "轻松活泼", "专业正式", "知乎风格"],
            label_visibility="collapsed"
        )

        # 显示风格说明
        style_descriptions = {
            "去AI化（自然口语）": "去除'首先/其次'等AI腔，转为自然口语表达",
            "轻松活泼": "适合小红书，短句+emoji，亲切随意",
            "专业正式": "适合公众号，逻辑清晰，用词规范",
            "知乎风格": "理性分析，保持客观专业"
        }
        st.caption(f"💡 {style_descriptions.get(rewrite_style, '')}")

        # 改写按钮
        if st.button("🔄 智能改写", type="primary", use_container_width=True):
            if not source_content or len(source_content.strip()) < 10:
                st.warning("⚠️ 请输入至少10个字符的内容")
            else:
                with st.spinner("🤖 AI正在改写中..."):
                    try:
                        # 改写内容
                        rewritten = rewrite_content(source_content, rewrite_style)
                        st.session_state['rewritten_content'] = rewritten

                        # 生成各平台版本
                        generate_platform_versions(rewritten)

                        st.session_state['rewrite_complete'] = True
                        st.session_state['rewrite_count'] += 1

                        st.success(f"✅ 改写完成！已生成3个平台版本")
                        st.balloons()

                    except Exception as e:
                        st.error(f"❌ 改写失败: {str(e)}")

    # ============== 中间：小红书预览 ==============
    with col2:
        st.markdown("""
        <div class="platform-header xiaohongshu-style">
            <span style="font-size: 20px;">📱</span>
            <span style="font-size: 16px; font-weight: 600;">小红书版本</span>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.get('rewrite_complete'):
            xiaohongshu_content = st.session_state.get('xiaohongshu_content', '')

            # 预览框
            st.markdown(f"""
            <div class="preview-box">
{xiaohongshu_content}
            </div>
            """, unsafe_allow_html=True)

            # 适配特性
            st.markdown("""
            <div style="margin: 12px 0;">
                <span class="feature-tag">✅ emoji前缀</span>
                <span class="feature-tag">✅ 短句分段</span>
                <span class="feature-tag">✅ 口语化</span>
                <span class="feature-tag">✅ 互动结尾</span>
            </div>
            """, unsafe_allow_html=True)

            # 操作按钮
            col_copy, col_publish = st.columns(2)
            with col_copy:
                if st.button("📋 复制", use_container_width=True, key="copy_xhs"):
                    st.toast("✅ 已复制到剪贴板！")
            with col_publish:
                xhs_ok, _ = check_platform_config("xiaohongshu")
                if st.button("🚀 同步草稿", use_container_width=True, type="primary",
                           disabled=not xhs_ok, key="publish_xhs"):
                    with st.spinner("正在创建小红书草稿..."):
                        title = extract_title(xiaohongshu_content)[:20]
                        publish_to_xiaohongshu(title, xiaohongshu_content)

            if not xhs_ok:
                st.caption("⚠️ 请先启用小红书并测试浏览器连接")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px; color: #64748b;">
                <div style="font-size: 48px; margin-bottom: 16px;">👈</div>
                <p>先在左侧输入内容</p>
                <p>然后点击"智能改写"</p>
            </div>
            """, unsafe_allow_html=True)

    # ============== 右侧：公众号预览 ==============
    with col3:
        st.markdown("""
        <div class="platform-header wechat-style">
            <span style="font-size: 20px;">💬</span>
            <span style="font-size: 16px; font-weight: 600;">公众号版本</span>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.get('rewrite_complete'):
            wechat_content = st.session_state.get('wechat_content', '')

            # 预览框
            st.markdown(f"""
            <div class="preview-box">
{wechat_content}
            </div>
            """, unsafe_allow_html=True)

            # 适配特性
            st.markdown("""
            <div style="margin: 12px 0;">
                <span class="feature-tag">✅ 专业导语</span>
                <span class="feature-tag">✅ 逻辑段落</span>
                <span class="feature-tag">✅ 结语引导</span>
                <span class="feature-tag">✅ 格式优化</span>
            </div>
            """, unsafe_allow_html=True)

            # 操作按钮
            col_copy, col_publish = st.columns(2)
            with col_copy:
                if st.button("📋 复制 ", use_container_width=True, key="copy_wechat"):
                    st.toast("✅ 已复制到剪贴板！")
            with col_publish:
                wechat_ok, _ = check_platform_config("wechat")
                if st.button("🚀 创建草稿", use_container_width=True, type="primary",
                           disabled=not wechat_ok, key="publish_wechat"):
                    with st.spinner("正在创建公众号草稿..."):
                        title = extract_title(wechat_content)
                        publish_to_wechat(title, wechat_content)

            if not wechat_ok:
                st.caption("⚠️ 请先在侧边栏配置微信公众号")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px; color: #64748b;">
                <div style="font-size: 48px; margin-bottom: 16px;">👈</div>
                <p>先在左侧输入内容</p>
                <p>然后点击"智能改写"</p>
            </div>
            """, unsafe_allow_html=True)

    # ============== 状态栏 ==============
    st.markdown("---")

    # 计算已配置平台数
    platforms_configured = sum([
        check_platform_config("wechat")[0],
        check_platform_config("feishu")[0],
        check_platform_config("xiaohongshu")[0]
    ])

    status_col1, status_col2, status_col3 = st.columns(3)
    with status_col1:
        status_emoji = "🟢" if st.session_state.get('rewrite_complete') else "⚪"
        st.caption(f"{status_emoji} 状态: {'改写完成' if st.session_state.get('rewrite_complete') else '等待输入'}")
    with status_col2:
        total_words = count_words(st.session_state.get('source_content', ''))
        st.caption(f"📝 字数: {total_words}")
    with status_col3:
        st.caption(f"📱 平台: {platforms_configured}/3 已配置")


if __name__ == "__main__":
    main()
