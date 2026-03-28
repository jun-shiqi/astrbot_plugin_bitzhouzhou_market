import logging
import aiohttp

logger = logging.getLogger(__name__)


class OKXService:
    def __init__(self, base_url: str = "https://www.okx.com"):
        self.base_url = base_url.rstrip('/')

    @staticmethod
    def _get_public_headers():
        """公开接口请求头（不需要鉴权）"""
        return {"Content-Type": "application/json"}

    async def _public_get(self, request_path: str):
        """发送公开 GET 请求"""
        try:
            headers = self._get_public_headers()
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}{request_path}", headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("code") == "0":
                            return data.get("data", [])
                        else:
                            logger.error(f"OKX API 错误: {data.get('msg')}")
                            return None
                    else:
                        logger.error(f"OKX API 请求失败: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"OKX API 请求异常: {e}")
            return None

    async def get_instruments(self, inst_type: str = "SPOT"):
        """获取交易产品基础信息"""
        request_path = f"/api/v5/public/instruments?instType={inst_type}"
        return await self._public_get(request_path)

    async def get_ticker(self, symbol: str):
        """获取交易对行情数据"""
        request_path = f"/api/v5/market/ticker?instId={symbol}"
        result = await self._public_get(request_path)
        if result and isinstance(result, list) and len(result) > 0:
            return result[0]
        return None

    async def get_market_data(self, symbols: list):
        """批量获取多个交易对的行情数据"""
        market_data = {}
        for symbol in symbols:
            ticker = await self.get_ticker(symbol)
            if ticker:
                market_data[symbol] = ticker
        return market_data

    async def get_index_tickers(self, inst_id: str):
        """获取指数行情"""
        request_path = f"/api/v5/market/index-tickers?instId={inst_id}"
        result = await self._public_get(request_path)
        if result and isinstance(result, list) and len(result) > 0:
            return result[0]
        return None

    async def get_index_candles(self, inst_id: str, bar: str = "1m", limit: str = "100"):
        """获取指数K线数据"""
        request_path = f"/api/v5/market/index-candles?instId={inst_id}&bar={bar}&limit={limit}"
        return await self._public_get(request_path)

    async def get_mark_price(self, inst_type: str, inst_id: str = None):
        """获取标记价格"""
        if inst_id:
            request_path = f"/api/v5/public/mark-price?instType={inst_type}&instId={inst_id}"
        else:
            request_path = f"/api/v5/public/mark-price?instType={inst_type}"
        return await self._public_get(request_path)

    async def get_open_interest(self, inst_type: str, inst_id: str = None):
        """获取持仓总量"""
        if inst_id:
            request_path = f"/api/v5/public/open-interest?instType={inst_type}&instId={inst_id}"
        else:
            request_path = f"/api/v5/public/open-interest?instType={inst_type}"
        return await self._public_get(request_path)

    async def get_funding_rate(self, inst_id: str):
        """获取永续合约当前资金费率"""
        request_path = f"/api/v5/public/funding-rate?instId={inst_id}"
        result = await self._public_get(request_path)
        if result and isinstance(result, list) and len(result) > 0:
            return result[0]
        return None

    async def get_price_limit(self, inst_id: str):
        """获取限价"""
        request_path = f"/api/v5/public/price-limit?instId={inst_id}"
        result = await self._public_get(request_path)
        if result and isinstance(result, list) and len(result) > 0:
            return result[0]
        return None

    async def get_system_time(self):
        """获取系统时间"""
        request_path = "/api/v5/public/time"
        result = await self._public_get(request_path)
        if result and isinstance(result, list) and len(result) > 0:
            return result[0]
        return None