"""
小红书发布器
使用Playwright浏览器自动化
"""

import asyncio
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Page, Browser


class XiaohongshuPublisher:
    """小红书发布器（基于Playwright）"""

    def __init__(self, debug_port: int = 9222):
        self.debug_port = debug_port
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def connect_to_browser(self) -> bool:
        """
        连接到已启动的Chrome浏览器（CDP模式）

        使用前需要先启动Chrome:
        chrome.exe --remote-debugging-port=9222
        """
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.connect_over_cdp(
                f"http://localhost:{self.debug_port}"
            )

            # 获取第一个context和page
            contexts = self.browser.contexts
            if contexts:
                self.context = contexts[0]
                pages = self.context.pages
                self.page = pages[0] if pages else await self.context.new_page()
            else:
                self.context = await self.browser.new_context()
                self.page = await self.context.new_page()

            return True
        except Exception as e:
            print(f"连接浏览器失败: {e}")
            return False

    async def check_login_status(self) -> bool:
        """检查是否已登录"""
        if not self.page:
            return False

        await self.page.goto("https://www.xiaohongshu.com")
        await asyncio.sleep(2)

        try:
            # 检查是否有登录按钮
            login_button = await self.page.query_selector('text=登录')
            if login_button:
                print("未检测到登录状态")
                return False

            # 检查是否有首页元素
            await self.page.wait_for_selector('text=首页', timeout=5000)
            print("已登录")
            return True
        except:
            return False

    async def create_draft(self, title: str, content: str,
                          image_paths: Optional[list] = None) -> Dict[str, Any]:
        """
        创建小红书草稿

        Args:
            title: 标题
            content: 正文内容
            image_paths: 图片路径列表（可选）
        """
        if not self.page:
            connected = await self.connect_to_browser()
            if not connected:
                return {"success": False, "error": "无法连接到浏览器"}

        # 检查登录状态
        logged_in = await self.check_login_status()
        if not logged_in:
            return {
                "success": False,
                "error": "未登录，请先手动登录小红书",
                "action": "请访问 https://www.xiaohongshu.com 并登录"
            }

        try:
            # 进入创作页面
            await self.page.goto('https://www.xiaohongshu.com/create', wait_until='networkidle')
            await self.page.wait_for_selector('div[contenteditable="true"]', timeout=15000)

            # 如果有图片，先上传
            if image_paths:
                file_input = await self.page.query_selector('input[type="file"]')
                if file_input:
                    await file_input.set_input_files(image_paths)
                    await asyncio.sleep(2)

            # 输入标题
            title_input = await self.page.query_selector('input[placeholder*="标题"]')
            if title_input:
                await title_input.fill(title)

            # 输入正文
            editor = await self.page.query_selector('div[contenteditable="true"]')
            if editor:
                await editor.click()
                await editor.fill(content)

            # 保存为草稿（不发布）
            # 注意：小红书的草稿按钮可能需要根据实际页面结构调整
            draft_button = await self.page.query_selector('button:has-text("存草稿")')
            if draft_button:
                await draft_button.click()
                await asyncio.sleep(2)

            return {
                "success": True,
                "msg": "草稿已保存",
                "platform": "xiaohongshu"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def close(self):
        """关闭连接"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()

    def adapt_for_xiaohongshu(self, content: str, max_length: int = 1000) -> str:
        """
        将内容适配为小红书格式

        - 精简到1000字以内
        - 添加emoji
        - 分段简短
        """
        import re

        # 移除Markdown标记
        text = re.sub(r'#+ ', '', content)
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'\*', '', text)

        # 精简长度
        if len(text) > max_length:
            text = text[:max_length - 3] + "..."

        # 添加emoji到段落开头
        emojis = ['💡', '✨', '📌', '💭', '🔥', '⭐', '📊', '💪']
        lines = text.split('\n')
        new_lines = []

        for i, line in enumerate(lines):
            if line.strip():
                emoji = emojis[i % len(emojis)]
                new_lines.append(f"{emoji} {line}")
            else:
                new_lines.append(line)

        return '\n\n'.join(new_lines)


if __name__ == "__main__":
    # 测试代码
    async def test():
        publisher = XiaohongshuPublisher()

        # 连接浏览器
        connected = await publisher.connect_to_browser()
        if connected:
            print("已连接到浏览器")

            # 创建草稿
            result = await publisher.create_draft(
                title="测试标题",
                content="这是测试内容"
            )
            print(result)
        else:
            print("连接失败，请确保Chrome已启动并开启调试端口")
            print("启动命令: chrome.exe --remote-debugging-port=9222")

        await publisher.close()

    asyncio.run(test())
