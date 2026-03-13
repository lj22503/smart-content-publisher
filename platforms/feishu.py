"""
飞书发布器
使用飞书开放平台API创建文档
"""

import requests
from typing import Optional, Dict, Any


class FeishuPublisher:
    """飞书文档发布器"""

    API_BASE = "https://open.feishu.cn/open-apis"

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_token: Optional[str] = None

    def get_tenant_token(self) -> str:
        """获取tenant_access_token"""
        url = f"{self.API_BASE}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if result.get("code") == 0:
            self.tenant_token = result["tenant_access_token"]
            return self.tenant_token
        else:
            raise Exception(f"获取token失败: {result}")

    def create_document(self, title: str, folder_token: Optional[str] = None) -> Dict[str, Any]:
        """
        创建文档

        Args:
            title: 文档标题
            folder_token: 文件夹token（可选）
        """
        if not self.tenant_token:
            self.get_tenant_token()

        url = f"{self.API_BASE}/docx/v1/documents"
        headers = {
            "Authorization": f"Bearer {self.tenant_token}",
            "Content-Type": "application/json"
        }

        data = {"title": title}
        if folder_token:
            data["folder_token"] = folder_token

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if result.get("code") == 0:
            document = result["data"]["document"]
            return {
                "success": True,
                "document_id": document["document_id"],
                "title": document["title"],
                "url": f"https://open.feishu.cn/docx/{document['document_id']}"
            }
        else:
            return {
                "success": False,
                "error": result.get("msg", "未知错误"),
                "code": result.get("code", -1)
            }

    def add_content_blocks(self, document_id: str, blocks: list) -> Dict[str, Any]:
        """
        向文档添加内容块

        Args:
            document_id: 文档ID
            blocks: 内容块列表
        """
        if not self.tenant_token:
            self.get_tenant_token()

        url = f"{self.API_BASE}/docx/v1/documents/{document_id}/blocks/batch_create"
        headers = {
            "Authorization": f"Bearer {self.tenant_token}",
            "Content-Type": "application/json"
        }

        data = {
            "children": blocks
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return result

    def markdown_to_feishu_blocks(self, markdown_content: str) -> list:
        """
        将Markdown转换为飞书文档blocks格式
        """
        import re

        blocks = []
        lines = markdown_content.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 标题
            if line.startswith('# '):
                blocks.append({
                    "block_type": 1,  # heading1
                    "heading1": {
                        "elements": [{"type": "textRun", "textRun": {"content": line[2:]}}]
                    }
                })
            elif line.startswith('## '):
                blocks.append({
                    "block_type": 2,  # heading2
                    "heading2": {
                        "elements": [{"type": "textRun", "textRun": {"content": line[3:]}}]
                    }
                })
            elif line.startswith('### '):
                blocks.append({
                    "block_type": 3,  # heading3
                    "heading3": {
                        "elements": [{"type": "textRun", "textRun": {"content": line[4:]}}]
                    }
                })
            # 列表
            elif line.startswith('- '):
                blocks.append({
                    "block_type": 11,  # bullet
                    "bullet": {
                        "elements": [{"type": "textRun", "textRun": {"content": line[2:]}}]
                    }
                })
            # 普通段落
            else:
                blocks.append({
                    "block_type": 4,  # paragraph
                    "paragraph": {
                        "elements": [{"type": "textRun", "textRun": {"content": line}}]
                    }
                })

        return blocks


if __name__ == "__main__":
    # 测试代码
    publisher = FeishuPublisher("your_app_id", "your_app_secret")
    # result = publisher.create_document("测试文档")
    # print(result)
