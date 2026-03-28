import logging
from typing import Dict, List
from astrbot.api.platform import Platform
logger = logging.getLogger(__name__)


async def send_message(context, targets: Dict[str, List[str]], message: str):
    """
    统一发送消息函数

    Args:
        context: AstrBot Context 实例
        targets: 发送目标，格式为 {"private_users": [], "groups": []}
        message: 要发送的消息内容
    """
    # 获取所有已注册的平台适配器
    platforms = self.context.platform_manager.get_insts()
    
    for platform in platforms:
        adapter = platform.platform_instance

        # 发送私聊消息
        private_users = targets.get("private_users", [])
        for user_id in private_users:
            try:
                await adapter.send_msg(
                    target_type="private",
                    target_id=user_id,
                    message=message
                )
                logger.info(f"成功向用户 {user_id} 发送消息")
            except Exception as e:
                logger.error(f"向用户 {user_id} 发送消息失败: {e}")

        # 发送群消息
        groups = targets.get("groups", [])
        for group_id in groups:
            try:
                await adapter.send_msg(
                    target_type="group",
                    target_id=group_id,
                    message=message
                )
                logger.info(f"成功向群 {group_id} 发送消息")
            except Exception as e:
                logger.error(f"向群 {group_id} 发送消息失败: {e}")