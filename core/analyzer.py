import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class MarketAnalyzer:
    def __init__(self, okx_service, llm_service):
        self.okx_service = okx_service
        self.llm_service = llm_service
    
    async def analyze_market(self, symbols: List[str]):
        """分析市场数据"""
        logger.info(f"进入分析")
        try:
            # 获取市场数据
            market_data = await self.okx_service.get_market_data(symbols)
            if not market_data:
                return "获取市场数据失败"
            
            # 构建基础分析报告
            report = "【加密市场分析】\n\n"
            
            # 获取额外的市场数据
            additional_data = {}
            for symbol in symbols:
                # 提取币种名称（如 BTC-USDT -> BTC）
                ccy = symbol.split('-')[0]
                # 获取持仓总量
                open_interest = await self.okx_service.get_open_interest('SWAP', f'{ccy}-USDT-SWAP')
                # 获取资金费率
                funding_rate = await self.okx_service.get_funding_rate(f'{ccy}-USDT-SWAP')
                # 获取指数行情
                index_ticker = await self.okx_service.get_index_tickers(f'{ccy}-USDT')
                
                additional_data[symbol] = {
                    'open_interest': open_interest,
                    'funding_rate': funding_rate,
                    'index_ticker': index_ticker
                }
            
            # 使用 LLM 分析市场
            llm_analysis = await self.llm_service.analyze_market(market_data)
            
            # 添加 LLM 分析
            report += f"{llm_analysis}\n\n"
            
            # 添加详细数据
            report += "【详细数据】\n"
            for symbol, data in market_data.items():
                price = data.get('last', 'N/A')
                change = data.get('change24h', 'N/A')
                high = data.get('high24h', 'N/A')
                low = data.get('low24h', 'N/A')
                volume = data.get('vol24h', 'N/A')
                
                report += f"{symbol}:\n"
                report += f"  价格: {price}\n"
                report += f"  24h 变化: {change}%\n"
                report += f"  24h 最高: {high}\n"
                report += f"  24h 最低: {low}\n"
                report += f"  24h 成交量: {volume}\n"
                
                # 添加额外数据
                extra = additional_data.get(symbol, {})
                if extra.get('open_interest') and isinstance(extra['open_interest'], list) and len(extra['open_interest']) > 0:
                    oi = extra['open_interest'][0].get('oi', 'N/A')
                    oi_usd = extra['open_interest'][0].get('oiUsd', 'N/A')
                    report += f"  持仓总量: {oi}\n"
                    report += f"  持仓总量(USD): {oi_usd}\n"
                if extra.get('funding_rate'):
                    rate = extra['funding_rate'].get('fundingRate', 'N/A')
                    funding_time = extra['funding_rate'].get('fundingTime', 'N/A')
                    report += f"  资金费率: {rate}\n"
                    report += f"  资金费时间: {funding_time}\n"
                if extra.get('index_ticker'):
                    idx_px = extra['index_ticker'].get('idxPx', 'N/A')
                    report += f"  指数价格: {idx_px}\n"
                
                report += "\n"
            
            return report
        except Exception as e:
            logger.error(f"市场分析失败: {str(e)}")
            return "市场分析失败"
    
    async def generate_news_summary(self, news: List[Dict]):
        """生成新闻摘要"""
        try:
            if not news:
                return "暂无新闻"
            
            # 使用 LLM 总结新闻
            llm_summary = await self.llm_service.summarize_news(news)
            
            # 构建新闻摘要
            summary = "【加密货币新闻摘要】\n\n"
            summary += f"{llm_summary}\n\n"
            
            # 添加最新新闻
            summary += "【最新新闻】\n"
            for i, item in enumerate(news[:3]):
                summary += f"{i+1}. {item['title']}\n"
                summary += f"   链接: {item['link']}\n\n"
            
            return summary
        except Exception as e:
            logger.error(f"新闻摘要生成失败: {str(e)}")
            return "新闻摘要生成失败"
    
    async def generate_flash_summary(self, flash: List[Dict]):
        """生成快讯摘要"""
        try:
            if not flash:
                return "暂无快讯"
            
            # 构建快讯摘要
            summary = "【加密货币快讯】\n\n"
            for i, item in enumerate(flash[:10]):
                summary += f"{i+1}. {item['title']}\n"
            
            return summary
        except Exception as e:
            logger.error(f"快讯摘要生成失败: {str(e)}")
            return "快讯摘要生成失败"