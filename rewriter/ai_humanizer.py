"""
AI内容改写引擎 - 去AI化模块
将AI生成的内容转换为自然、口语化的人类风格
"""

import re
import random
from typing import Dict, List, Optional


class AIHumanizer:
    """
    AI内容人性化改写器

    核心功能：
    1. 去除AI腔调（"首先、其次、综上所述"等）
    2. 增加口语化表达
    3. 添加个人情感色彩
    4. 模拟真实写作风格
    """

    # AI高频词替换表
    AI_PATTERNS = {
        # 过渡词
        r'首先[，,]': ['先说', '第一点是', '开头要说的是'],
        r'其次[，,]': ['接着', '第二点', '然后'],
        r'再次[，,]': ['还有', '第三点', '接下来'],
        r'最后[，,]': ['最后说', '收尾', '总结一下'],
        r'综上所述': ['总的来说', '说句实在话', '说白了'],
        r'总而言之': ['总之', '一句话', '概括来说'],
        r'由此可见': ['看得出来', '这说明', '不难发现'],

        # 正式用语转口语
        r'非常[重要|关键]': ['特别重要', '很关键', '重中之重'],
        r'具有重要意义': ['很有意义', '挺重要的', '价值很大'],
        r'值得注意': ['要注意', '得留意', '别忽视'],
        r'不容忽视': ['不能忽视', '得重视', '很重要'],
        r'显而易见': ['很明显', '一眼就能看出来', '不用多说'],
        r'毫无疑问': ['毫无疑问', '不用怀疑', '肯定'],
        r'一定程度上': ['某种程度上', '多多少少', '有一定'],

        # 机械表达
        r'我们需要': ['咱们得', '要', '最好'],
        r'应该': ['应该', '得', '最好'],
        r'可以': ['可以', '能', '行'],
        r'通过.*?方式': ['通过', '用', '靠'],
    }

    # 口语化插入语
    FILLER_WORDS = [
        '其实', '说实话', '说真的', '讲真',
        '讲个道理', '不瞒你说', '说句心里话',
        '你可能不知道', '我发现', '我觉得',
        '相信大家', '别不信', '说实话',
    ]

    # 情感词增强
    EMOTION_WORDS = {
        '好': ['棒', '赞', '牛', '强', '厉害'],
        '重要': ['关键', '核心', '重中之重'],
        '困难': ['难搞', '棘手', '头疼'],
        '简单': ['容易', '轻松', '小菜一碟'],
        '有用': ['实用', '靠谱', '给力'],
    }

    # 句式模板
    SENTENCE_TEMPLATES = {
        'opening': [
            "最近一直在想{topic}这个问题",
            "关于{topic}，有些想法不吐不快",
            "今天想和大家聊聊{topic}",
            "说个{topic}的事儿",
        ],
        'transition': [
            "说到这儿，我突然想到",
            "有意思的是",
            "更让人意外的是",
            "不仅如此",
        ],
        'example': [
            "举个真实的例子",
            "我身边就有这么个事儿",
            "说个我经历过的",
            "拿实际案例来说",
        ],
        'conclusion': [
            "所以你看",
            "说白了",
            "总结一下",
            "最后的建议是",
        ],
    }

    def __init__(self, style: str = "natural"):
        """
        初始化改写器

        Args:
            style: 改写风格
                - natural: 自然口语化
                - casual: 轻松随意
                - professional: 专业但不生硬
        """
        self.style = style

    def humanize(self, text: str, platform: str = "general") -> str:
        """
        主改写方法

        Args:
            text: 原始AI生成文本
            platform: 目标平台 (xiaohongshu/wechat/general)

        Returns:
            改写后的人性化文本
        """
        result = text

        # 步骤1: 去除AI标记词
        result = self._remove_ai_patterns(result)

        # 步骤2: 增加口语化表达
        result = self._add_colloquialisms(result)

        # 步骤3: 添加情感色彩
        result = self._add_emotion(result)

        # 步骤4: 长短句变化
        result = self._vary_sentence_length(result)

        # 步骤5: 平台适配
        if platform == "xiaohongshu":
            result = self._adapt_for_xiaohongshu(result)
        elif platform == "wechat":
            result = self._adapt_for_wechat(result)

        return result

    def _remove_ai_patterns(self, text: str) -> str:
        """去除AI典型表达模式"""
        result = text

        for pattern, replacements in self.AI_PATTERNS.items():
            def replace_func(match):
                return random.choice(replacements)

            result = re.sub(pattern, replace_func, result)

        return result

    def _add_colloquialisms(self, text: str) -> str:
        """添加口语化表达"""
        sentences = re.split(r'([。！？\n])', text)
        result = []

        for i, sent in enumerate(sentences):
            if sent in ['。', '！', '？', '\n']:
                result.append(sent)
                continue

            # 随机插入填充词
            if random.random() < 0.3 and len(sent) > 10:
                filler = random.choice(self.FILLER_WORDS)
                sent = f"{filler}，{sent}"

            result.append(sent)

        return ''.join(result)

    def _add_emotion(self, text: str) -> str:
        """添加情感词增强"""
        result = text

        for word, emotions in self.EMOTION_WORDS.items():
            if word in result and random.random() < 0.3:
                emotion = random.choice(emotions)
                # 随机替换或追加
                if random.random() < 0.5:
                    result = result.replace(word, emotion, 1)
                else:
                    result = result.replace(word, f"{word}（{emotion}）", 1)

        return result

    def _vary_sentence_length(self, text: str) -> str:
        """变化句式长度，避免整齐划一"""
        sentences = re.split(r'([。！？])', text)
        result = []

        for i in range(0, len(sentences)-1, 2):
            sent = sentences[i]
            punct = sentences[i+1] if i+1 < len(sentences) else '。'

            # 长句拆短
            if len(sent) > 50 and '，' in sent:
                parts = sent.split('，')
                if len(parts) >= 2:
                    # 随机断句
                    mid = len(parts) // 2
                    sent = '，'.join(parts[:mid]) + punct + '，'.join(parts[mid:])
                    punct = ''

            result.append(sent + punct)

        return ''.join(result)

    def _adapt_for_xiaohongshu(self, text: str) -> str:
        """适配小红书风格"""
        # 添加emoji
        text = self._add_emojis(text)

        # 短段落
        paragraphs = text.split('\n')
        short_paragraphs = []

        for p in paragraphs:
            if len(p) > 30:
                # 长句拆分
                sentences = re.split(r'([。！？])', p)
                current = ''
                for s in sentences:
                    if len(current) + len(s) < 25:
                        current += s
                    else:
                        if current:
                            short_paragraphs.append(current)
                        current = s
                if current:
                    short_paragraphs.append(current)
            else:
                short_paragraphs.append(p)

        return '\n\n'.join(short_paragraphs)

    def _adapt_for_wechat(self, text: str) -> str:
        """适配公众号风格"""
        # 保持段落结构，但增加过渡
        paragraphs = text.split('\n\n')
        result = []

        for i, p in enumerate(paragraphs):
            result.append(p)

            # 段落间添加过渡（不是每段都加）
            if i < len(paragraphs) - 1 and random.random() < 0.3:
                transition = random.choice([
                    "接着说", "再说", "另外",
                ])
                result.append(f"\n{transition}，")

        return '\n\n'.join(result)

    def _add_emojis(self, text: str) -> str:
        """智能添加emoji"""
        emoji_map = {
            '好': ['👍', '👏', '💪'],
            '重要': ['⚠️', '❗', '🔥'],
            '注意': ['👀', '⚠️', '❗'],
            '爱': ['❤️', '💖', '💕'],
            '钱': ['💰', '💵', '💸'],
            '时间': ['⏰', '📅', '🕐'],
            '成功': ['🎉', '✨', '🏆'],
            '失败': ['😅', '😓', '💔'],
        }

        result = text
        for word, emojis in emoji_map.items():
            if word in result and random.random() < 0.4:
                emoji = random.choice(emojis)
                # 在词后添加emoji
                result = result.replace(word, f"{word}{emoji}", 1)

        return result


class PlatformRewriter:
    """
    平台特定改写器
    针对不同平台的风格要求进行内容改写
    """

    def __init__(self):
        self.humanizer = AIHumanizer()

    def rewrite_for_xiaohongshu(self, text: str) -> str:
        """
        改写成小红书风格
        - 短句为主
        - emoji点缀
        - 口语化强
        - 互动性强
        """
        # 基础去AI化
        humanized = self.humanizer.humanize(text, platform="xiaohongshu")

        # 小红书特定处理
        lines = humanized.split('\n')
        result_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 每行添加emoji前缀（随机）
            if random.random() < 0.5 and not line[0] in '🔥💡✨👍❤️':
                emojis = ['💡', '✨', '📌', '💭', '🔥', '👀', '👇']
                line = f"{random.choice(emojis)} {line}"

            result_lines.append(line)

        # 添加互动结尾
        endings = [
            "\n\n👇 你觉得呢？评论区聊聊",
            "\n\n💬 有问必答，评论区见",
            "\n\n❤️ 有用的话点个赞吧",
            "\n\n📌 收藏起来慢慢看",
        ]
        result_lines.append(random.choice(endings))

        return '\n\n'.join(result_lines)

    def rewrite_for_wechat(self, text: str) -> str:
        """
        改写成公众号风格
        - 专业但有温度
        - 逻辑清晰
        - 有导语和结语
        """
        # 基础去AI化
        humanized = self.humanizer.humanize(text, platform="wechat")

        # 添加导语
        openings = [
            "最近一直在思考这个问题，今天和大家分享一些想法。",
            "关于这个话题，最近有很多读者在问，今天就系统地说说。",
            "先说结论，再展开讲。",
        ]

        # 添加结语
        endings = [
            "\n\n以上就是今天的分享，希望对你有帮助。",
            "\n\n如果觉得有用，欢迎转发给需要的朋友。",
            "\n\n有问题可以在评论区留言，我会尽力回复。",
        ]

        result = random.choice(openings) + "\n\n" + humanized + random.choice(endings)

        return result

    def rewrite_for_zhihu(self, text: str) -> str:
        """
        改写成知乎风格
        - 理性分析
        - 数据支撑
        - 逻辑严密
        """
        # 知乎相对保持原样，但去除AI腔
        humanized = self.humanizer.humanize(text, platform="general")

        # 添加来源说明
        if random.random() < 0.5:
            humanized += "\n\n（注：以上内容基于公开资料整理，仅供参考）"

        return humanized


# 便捷函数
def humanize_text(text: str, platform: str = "general") -> str:
    """
    快速改写函数

    Args:
        text: 原始文本
        platform: 目标平台 (xiaohongshu/wechat/zhihu/general)

    Returns:
        改写后的文本
    """
    rewriter = PlatformRewriter()

    if platform == "xiaohongshu":
        return rewriter.rewrite_for_xiaohongshu(text)
    elif platform == "wechat":
        return rewriter.rewrite_for_wechat(text)
    elif platform == "zhihu":
        return rewriter.rewrite_for_zhihu(text)
    else:
        return rewriter.humanizer.humanize(text)


if __name__ == "__main__":
    # 测试
    test_text = """
    首先，我们需要理解这个问题的重要性。其次，通过系统性的分析，
    可以发现关键因素。综上所述，解决方案是可行的。
    这是一个非常有意义的研究方向，值得深入探讨。
    """

    print("原始文本:")
    print(test_text)
    print("\n" + "="*50 + "\n")

    print("小红书风格:")
    print(humanize_text(test_text, "xiaohongshu"))
    print("\n" + "="*50 + "\n")

    print("公众号风格:")
    print(humanize_text(test_text, "wechat"))
