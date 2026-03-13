"""
微信公众号发布器
使用微信官方API创建草稿
"""

import requests
import json
from typing import Optional, Dict, Any


class WeChatPublisher:
    """微信公众号发布器"""

    API_BASE = "https://api.weixin.qq.com/cgi-bin"

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None

    def get_access_token(self) -> str:
        """获取access_token"""
        url = f"{self.API_BASE}/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "access_token" in data:
            self.access_token = data["access_token"]
            return self.access_token
        else:
            raise Exception(f"获取token失败: {data}")

    def create_draft(self, title: str, content: str, author: str = "",
                     digest: str = "", thumb_media_id: str = "") -> Dict[str, Any]:
        """
        创建草稿

        Args:
            title: 标题
            content: 正文内容（支持HTML）
            author: 作者
            digest: 摘要
            thumb_media_id: 封面图片media_id
        """
        if not self.access_token:
            self.get_access_token()

        url = f"{self.API_BASE}/draft/add"
        params = {"access_token": self.access_token}

        data = {
            "articles": [{
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "thumb_media_id": thumb_media_id,
                "show_cover_pic": 1,
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }]
        }

        response = requests.post(
            url,
            params=params,
            data=json.dumps(data, ensure_ascii=False).encode('utf-8')
        )

        result = response.json()

        if "media_id" in result:
            return {
                "success": True,
                "media_id": result["media_id"],
                "msg": "草稿创建成功"
            }
        else:
            return {
                "success": False,
                "error": result.get("errmsg", "未知错误"),
                "code": result.get("errcode", -1)
            }

    def upload_image(self, image_path: str) -> str:
        """
        上传图片获取media_id

        Args:
            image_path: 图片本地路径
        """
        if not self.access_token:
            self.get_access_token()

        url = f"{self.API_BASE}/media/upload"
        params = {
            "access_token": self.access_token,
            "type": "image"
        }

        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, params=params, files=files)

        result = response.json()

        if "media_id" in result:
            return result["media_id"]
        else:
            raise Exception(f"上传失败: {result}")

    def html_to_wechat(self, markdown_content: str) -> str:
        """
        将Markdown转换为微信公众号HTML格式
        """
        import re

        html = markdown_content

        # 标题转换
        html = re.sub(r'^# (.+)$', r'<h1 style="font-size:24px;font-weight:bold;margin:20px 0;">\1</h1>',
                      html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2 style="font-size:20px;font-weight:bold;margin:16px 0;">\1</h2>',
                      html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3 style="font-size:18px;font-weight:bold;margin:12px 0;">\1</h3>',
                      html, flags=re.MULTILINE)

        # 粗体和斜体
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

        # 段落
        html = re.sub(r'\n\n', '</p><p style="margin:12px 0;line-height:1.8;">', html)
        html = '<p style="margin:12px 0;line-height:1.8;">' + html + '</p>'

        # 列表
        html = re.sub(r'^- (.+)$', r'<li style="margin:8px 0;">\1</li>',
                      html, flags=re.MULTILINE)

        return html


if __name__ == "__main__":
    # 测试代码
    publisher = WeChatPublisher("your_app_id", "your_app_secret")
    # result = publisher.create_draft("测试标题", "<p>测试内容</p>")
    # print(result)
