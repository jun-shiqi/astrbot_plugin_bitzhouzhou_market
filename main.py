"""
比特周周加密市场分析插件 - 主入口文件
"""

import asyncio
from astrbot.api.star import Star, Context, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event import MessageChain


try:
    from astrbot.api import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from .services.okx_service import OKXService
from .services.rss_service import RSSService
from .services.llm_service import LLMService
from .core.analyzer import MarketAnalyzer
from .core.alert import PriceAlertSystem
from .core.broadcaster import send_message


@register(
    "astrbot_plugin_bitzhouzhou_market",
    "比特周周技术助手 Hugh Orion",
    "提供加密货币市场分析、价格预警和新闻播报功能。",
    "1.0.0",
    "https://github.com/bitzhouzhou/astrbot_plugin_bitzhouzhou_market"
)
class BitZhouZhouMarket(Star):

    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        self.config = config or {}
        self.okx_service = None
        self.rss_service = None
        self.llm_service = None
        self.analyzer = None
        self.alert_system = None
        self.broadcast_task = None
        self.alert_task = None

        self._init_services()
        self._start_tasks()

        logger.info("比特周周加密市场分析插件已加载")

    def _parse_list(self, value: str) -> list:
        """将逗号分隔的字符串解析为列表"""
        if not value or not value.strip():
            return []
        return [item.strip() for item in value.split(',') if item.strip()]

    def _get_targets(self) -> dict:
        """从扁平化配置中获取发送目标"""
        return {
            "private_users": self._parse_list(self.config.get('target_private_users', '')),
            "groups": self._parse_list(self.config.get('target_groups', ''))
        }

    def _get_alert_configs(self) -> list:
        """从扁平化配置中构建预警配置列表"""
        if not self.config.get('alert_enable', True):
            return []

        symbols = self._parse_list(self.config.get('alert_symbols', 'BTC-USDT'))
        targets = self._get_targets()
        alerts = []
        for symbol in symbols:
            alerts.append({
                'symbol': symbol,
                'enable': True,
                'up_percent': self.config.get('alert_up_percent', 5),
                'down_percent': self.config.get('alert_down_percent', 5),
                'interval_sec': 60,
                'targets': targets
            })
        return alerts

    def _init_services(self):
        """初始化服务"""
        # 初始化 OKX 服务（使用公开接口，无需API密钥）
        self.okx_service = OKXService(
            base_url='https://www.okx.com'
        )

        # 初始化 RSS 服务
        news_url = self.config.get('rss_news_url', '')
        flash_url = self.config.get('rss_flash_url', '')
        self.rss_service = RSSService(
            news_url=news_url if news_url else None,
            flash_url=flash_url if flash_url else None
        )

        # 初始化 LLM 服务
        self.llm_service = LLMService(
            enabled=self.config.get('llm_enabled', True),
            api_key=self.config.get('llm_api_key', ''),
            base_url=self.config.get('llm_base_url', ''),
            model=self.config.get('llm_model', 'gpt-4o-mini')
        )

        # 初始化分析器
        self.analyzer = MarketAnalyzer(self.okx_service, self.llm_service)

        # 初始化预警系统
        self.alert_system = PriceAlertSystem(self.okx_service, send_message)

    def _start_tasks(self):
        """启动定时任务"""
        if self.config.get('broadcast_enable', True):
            interval = self.config.get('broadcast_interval_sec', 300)
            self.broadcast_task = asyncio.create_task(self._broadcast_loop(interval))

        alert_configs = self._get_alert_configs()
        if alert_configs:
            self.alert_task = asyncio.create_task(self._alert_loop())

    async def _broadcast_loop(self, interval: int):
        """播报循环"""
        while True:
            try:
                await self._perform_broadcast()
            except Exception as e:
                logger.error(f"播报任务失败: {e}")
            await asyncio.sleep(interval)

    async def _alert_loop(self):
        """预警循环"""
        while True:
            try:
                alert_configs = self._get_alert_configs()
                await self.alert_system.check_price_alerts(alert_configs, self.context)
            except Exception as e:
                logger.error(f"预警任务失败: {e}")
            await asyncio.sleep(60)

    async def _perform_broadcast(self,event:AstrMessageEvent):
        """执行播报"""
        targets = self._get_targets()
        

        if self.config.get('broadcast_send_market', True):
            alert_configs = self._get_alert_configs()
            symbols = [a['symbol'] for a in alert_configs if a.get('enable')]
            if not symbols:
                symbols = ['BTC-USDT']
            market_analysis = await self.analyzer.analyze_market(symbols)
            await send_message(self,event,targets, market_analysis)

        if self.config.get('broadcast_send_news', True):
            news = await self.rss_service.get_news()
            news_summary = await self.analyzer.generate_news_summary(news)
            await self.my_send_massage(self,event,targets, news_summary)

        if self.config.get('broadcast_send_flash', True):
            flash = await self.rss_service.get_flash()
            flash_summary = await self.analyzer.generate_flash_summary(flash)
            await self.my_send_massage(self,event,targets,flash_summary)

    async def terminate(self):
        """插件被卸载/停用时调用"""
        logger.info("比特周周加密市场分析插件正在卸载")
        if self.broadcast_task:
            self.broadcast_task.cancel()
        if self.alert_task:
            self.alert_task.cancel()
        logger.info("比特周周加密市场分析插件已终止")

   