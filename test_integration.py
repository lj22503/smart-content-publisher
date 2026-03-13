"""
智能内容分发助手 - 联调测试脚本
测试内容改写引擎和平台适配功能
"""

import sys
import asyncio
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from rewriter.ai_humanizer import humanize_text, PlatformRewriter


class IntegrationTester:
    """集成测试器"""

    def __init__(self):
        self.test_results = []

    def log(self, message: str, status: str = "info"):
        """记录测试结果"""
        icon = {"info": "[i]", "success": "[OK]", "error": "[ERR]", "warning": "[WARN]"}.get(status, "[i]")
        print(f"{icon} {message}")
        self.test_results.append({"message": message, "status": status})

    def test_humanizer_basic(self):
        """测试基础改写功能"""
        print("\n" + "=" * 50)
        print("测试1: 基础改写功能")
        print("=" * 50)

        test_text = """
首先，我们需要理解这个问题的重要性。其次，通过系统性的分析，
可以发现关键因素。综上所述，解决方案是可行的。
这是一个非常有意义的研究方向，值得深入探讨。
"""

        try:
            result = humanize_text(test_text, platform="general")
            self.log("改写引擎运行正常", "success")

            # 检查AI词汇是否被替换
            ai_words = ["首先", "其次", "综上所述"]
            found_ai = [w for w in ai_words if w in result]

            if found_ai:
                self.log(f"警告: 仍保留AI词汇: {found_ai}", "warning")
            else:
                self.log("AI词汇替换成功", "success")

            print("\n改写结果预览:")
            print("-" * 40)
            print(result[:200] + "...")
            return True

        except Exception as e:
            self.log(f"改写失败: {e}", "error")
            return False

    def test_xiaohongshu_rewrite(self):
        """测试小红书改写"""
        print("\n" + "=" * 50)
        print("测试2: 小红书风格改写")
        print("=" * 50)

        test_content = """
# 基金投资入门指南

投资基金是理财的重要方式。首先，要了解基金的基本类型。
其次，需要评估自己的风险承受能力。最后，选择合适的基金产品。

这是一个值得关注的投资方向。
"""

        try:
            rewriter = PlatformRewriter()
            result = rewriter.rewrite_for_xiaohongshu(test_content)

            self.log("小红书改写成功", "success")

            # 检查特征
            has_emoji = any(ord(c) > 0x1F300 for c in result)
            has_line_breaks = result.count('\n') >= 3

            if has_emoji:
                self.log("[+] 包含emoji", "success")
            else:
                self.log("[!] 未检测到emoji", "warning")

            if has_line_breaks:
                self.log("[+] 段落已分段", "success")

            print("\n小红书版本预览:")
            print("-" * 40)
            # 过滤掉emoji以兼容Windows控制台
            preview = result[:300].encode('ascii', 'ignore').decode('ascii')
            print(preview + "...")
            return True

        except Exception as e:
            self.log(f"小红书改写失败: {e}", "error")
            return False

    def test_wechat_rewrite(self):
        """测试公众号改写"""
        print("\n" + "=" * 50)
        print("测试3: 公众号风格改写")
        print("=" * 50)

        test_content = """
# 基金投资策略分析

首先，市场分析显示当前是投资良机。其次，分散投资可以降低风险。
综上所述，建议采用定投策略。
"""

        try:
            rewriter = PlatformRewriter()
            result = rewriter.rewrite_for_wechat(test_content)

            self.log("公众号改写成功", "success")

            # 检查是否有导语和结语
            has_opening = any(phrase in result for phrase in ["最近", "今天", "先说结论"])
            has_ending = any(phrase in result for phrase in ["以上就是", "希望对你", "有问题可以"])

            if has_opening:
                self.log("[+] 包含导语", "success")
            if has_ending:
                self.log("[+] 包含结语", "success")

            print("\n公众号版本预览:")
            print("-" * 40)
            print(result[:300] + "...")
            return True

        except Exception as e:
            self.log(f"公众号改写失败: {e}", "error")
            return False

    def test_wechat_html_conversion(self):
        """测试微信HTML转换"""
        print("\n" + "=" * 50)
        print("测试4: 微信HTML转换")
        print("=" * 50)

        try:
            from platforms.wechat import WeChatPublisher

            publisher = WeChatPublisher("test_appid", "test_secret")

            markdown = """
# 测试标题

这是正文内容，**加粗文字**和普通文字。

## 小标题

- 列表项1
- 列表项2

这是*斜体*文字。
"""

            html = publisher.html_to_wechat(markdown)

            self.log("HTML转换成功", "success")

            # 检查HTML标签
            if "<h1" in html and "<strong>" in html and "<li>" in html:
                self.log("[+] HTML标签正确", "success")
            else:
                self.log("[!] HTML标签可能不完整", "warning")

            print("\nHTML输出预览:")
            print("-" * 40)
            print(html[:300])
            return True

        except Exception as e:
            self.log(f"HTML转换失败: {e}", "error")
            return False

    def test_feishu_blocks(self):
        """测试飞书Blocks转换"""
        print("\n" + "=" * 50)
        print("测试5: 飞书Blocks转换")
        print("=" * 50)

        try:
            from platforms.feishu import FeishuPublisher

            publisher = FeishuPublisher("test_appid", "test_secret")

            markdown = """
# 标题1

## 标题2

正文段落

- 列表项
"""

            blocks = publisher.markdown_to_feishu_blocks(markdown)

            self.log(f"Blocks转换成功，生成 {len(blocks)} 个block", "success")

            # 检查block类型
            block_types = [b.get('block_type') for b in blocks]
            if 1 in block_types:  # heading1
                self.log("[+] 包含标题1", "success")
            if 2 in block_types:  # heading2
                self.log("[+] 包含标题2", "success")
            if 4 in block_types:  # paragraph
                self.log("[+] 包含段落", "success")

            print("\nBlocks输出预览:")
            print("-" * 40)
            import json
            print(json.dumps(blocks[:2], indent=2, ensure_ascii=False))
            return True

        except Exception as e:
            self.log(f"Blocks转换失败: {e}", "error")
            return False

    def test_xiaohongshu_adapter(self):
        """测试小红书内容适配"""
        print("\n" + "=" * 50)
        print("测试6: 小红书内容适配")
        print("=" * 50)

        try:
            from platforms.xiaohongshu import XiaohongshuPublisher

            publisher = XiaohongshuPublisher()

            content = """
# 投资心得

这是一段关于基金投资的经验分享。
**重点内容**需要强调。

- 要点1
- 要点2
"""

            adapted = publisher.adapt_for_xiaohongshu(content)

            self.log("内容适配成功", "success")

            # 检查适配效果
            has_emojis = any(c in adapted for c in ['💡', '✨', '📌', '💭', '🔥'])

            if has_emojis:
                self.log("[+] 已添加emoji前缀", "success")

            print("\n适配后内容预览:")
            print("-" * 40)
            # 过滤掉emoji以兼容Windows控制台
            preview = adapted[:300].encode('ascii', 'ignore').decode('ascii')
            print(preview)
            return True

        except Exception as e:
            self.log(f"内容适配失败: {e}", "error")
            return False

    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "=" * 50)
        print("智能内容分发助手 - 联调测试")
        print("=" * 50)

        tests = [
            ("基础改写", self.test_humanizer_basic),
            ("小红书改写", self.test_xiaohongshu_rewrite),
            ("公众号改写", self.test_wechat_rewrite),
            ("微信HTML", self.test_wechat_html_conversion),
            ("飞书Blocks", self.test_feishu_blocks),
            ("小红书适配", self.test_xiaohongshu_adapter),
        ]

        passed = 0
        failed = 0

        for name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.log(f"测试异常: {e}", "error")
                failed += 1

        # 测试报告
        print("\n" + "=" * 50)
        print("测试报告")
        print("=" * 50)
        print(f"总计: {len(tests)} 项")
        print(f"通过: {passed} 项 [OK]")
        print(f"失败: {failed} 项 [FAIL]")

        if failed == 0:
            print("\n[PASS] 所有测试通过！系统运行正常。")
        else:
            print(f"\n[WARNING] 有 {failed} 项测试失败，请检查相关模块。")

        return failed == 0


def main():
    tester = IntegrationTester()
    success = tester.run_all_tests()

    # 返回退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
