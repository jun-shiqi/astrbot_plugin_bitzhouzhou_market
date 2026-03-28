import logging
import time
from typing import Dict, List

logger = logging.getLogger(__name__)

class PriceAlertSystem:
    def __init__(self, okx_service, broadcaster):
        self.okx_service = okx_service
        self.broadcaster = broadcaster
        self.last_alert_time = {}  # 用于记录每个币种的最后预警时间，避免重复触发
    
    async def check_price_alerts(self, alerts_config: List[Dict], bot):
        """检查价格预警"""
        for alert in alerts_config:
            if not alert.get('enable', False):
                continue
            
            symbol = alert['symbol']
            up_percent = alert.get('up_percent', 5)
            down_percent = alert.get('down_percent', 5)
            targets = alert.get('targets', {})
            
            # 检查冷却时间
            last_alert = self.last_alert_time.get(symbol, 0)
            if time.time() - last_alert < 300:  # 5分钟冷却时间
                continue
            
            # 获取最新价格
            ticker = await self.okx_service.get_ticker(symbol)
            if not ticker:
                continue
            
            try:
                current_price = float(ticker.get('last', 0))
                open_price = float(ticker.get('open24h', 0))
                
                if open_price == 0:
                    continue
                
                # 计算价格变化百分比
                change_percent = ((current_price - open_price) / open_price) * 100
                
                # 检查上涨预警
                if change_percent >= up_percent:
                    message = f"【价格预警】{symbol} 上涨 {change_percent:.2f}%\n" \
                              f"当前价格: {current_price}\n" \
                              f"24h 开盘: {open_price}\n" \
                              f"预警阈值: {up_percent}%"
                    await self.broadcaster(bot, targets, message)
                    self.last_alert_time[symbol] = time.time()
                    logger.info(f"发送 {symbol} 上涨预警: {change_percent:.2f}%")
                
                # 检查下跌预警
                elif change_percent <= -down_percent:
                    message = f"【价格预警】{symbol} 下跌 {abs(change_percent):.2f}%\n" \
                              f"当前价格: {current_price}\n" \
                              f"24h 开盘: {open_price}\n" \
                              f"预警阈值: {down_percent}%"
                    await self.broadcaster(bot, targets, message)
                    self.last_alert_time[symbol] = time.time()
                    logger.info(f"发送 {symbol} 下跌预警: {abs(change_percent):.2f}%")
            except Exception as e:
                logger.error(f"检查 {symbol} 价格预警失败: {str(e)}")
                continue
    
    def get_alert_list(self, alerts_config: List[Dict]):
        """获取预警列表"""
        if not alerts_config:
            return "暂无价格预警配置"
        
        alert_list = "【价格预警列表】\n\n"
        for alert in alerts_config:
            symbol = alert['symbol']
            enable = "启用" if alert.get('enable', False) else "禁用"
            up_percent = alert.get('up_percent', 5)
            down_percent = alert.get('down_percent', 5)
            interval = alert.get('interval_sec', 60)
            targets = alert.get('targets', {})
            
            alert_list += f"{symbol}:\n"
            alert_list += f"  状态: {enable}\n"
            alert_list += f"  上涨预警: {up_percent}%\n"
            alert_list += f"  下跌预警: {down_percent}%\n"
            alert_list += f"  检测间隔: {interval}秒\n"
            alert_list += f"  发送目标: QQ好友 {len(targets.get('private_users', []))} 个, 群 {len(targets.get('groups', []))} 个\n\n"
        
        return alert_list