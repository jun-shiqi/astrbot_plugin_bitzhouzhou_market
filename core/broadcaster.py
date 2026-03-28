import logging
from typing import Dict, List
from astrbot.api.platform import Platform
from astrbot.api.event import MessageChain
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult

logger = logging.getLogger(__name__)


async def send_message(self,event:AstrMessageEvent ,targets: Dict[str, List[str]], message: str):
    """
    统一发送消息函数

    Args:
        context: AstrBot Context 实例
        targets: 发送目标，格式为 {"private_users": [], "groups": []}
        message: 要发送的消息内容
    """
    # 获取所有已注册的平台适配器
    platforms = self.context.platform_manager.get_insts()
    
    
    # 发送私聊消息
    private_users = targets.get("private_users", [])
    for user_id in private_users:
        try:
    
            from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot # 得到 client
            payloads = {
                "message_type": "private",
                "user_id": str(user_id),
                "message": message
            }
            ret = await client.api.call_action('send_msg', **payloads) # 调用 协议端  API
            logger.info(f"成功向用户 {user_id} 发送消息")
        except Exception as e:
            logger.error(f"向用户 {user_id} 发送消息失败: {e}")
            
    # 发送群消息
    groups = targets.get("groups", [])
    for group_id in groups:
        try:
            from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot # 得到 client
            payloads = {
                "message_type": "group",
                "user_id": str(group_id),
                "message": message
            }
            ret = await client.api.call_action('send_msg', **payloads) # 调用 协议端  API
            logger.info(f"成功向群 {group_id} 发送消息")
        except Exception as e:
            logger.error(f"向群 {group_id} 发送消息失败: {e}")