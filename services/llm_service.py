import logging
import aiohttp

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, enabled: bool, api_key: str, base_url: str, model: str):
        self.enabled = enabled
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
    
    async def analyze_market(self, market_data: dict):
        """使用 LLM 分析市场数据"""
        if not self.enabled or not self.api_key or not self.base_url:
            return "LLM 未启用或配置不完整"
        
        try:
            # 构建提示词
            prompt = f"请分析以下加密货币市场数据，提供简要的市场分析和趋势判断：\n\n"
            for symbol, data in market_data.items():
                price = data.get('last', 'N/A')
                change = data.get('change24h', 'N/A')
                prompt += f"{symbol}: 价格 {price}，24h 变化 {change}%\n"
            
            # 构建请求体
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的加密货币市场分析师，请提供简洁、专业的市场分析。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            # 发送请求
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/v1/chat/completions", headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        logger.error(f"LLM API 请求失败: {response.status}")
                        return "LLM 分析失败"
        except Exception as e:
            logger.error(f"LLM 分析失败: {str(e)}")
            return "LLM 分析失败"
    
    async def summarize_news(self, news: list):
        """使用 LLM 总结新闻"""
        if not self.enabled or not self.api_key or not self.base_url:
            return "LLM 未启用或配置不完整"
        
        try:
            # 构建提示词
            prompt = "请总结以下加密货币相关新闻，提供简洁的要点：\n\n"
            for item in news:
                prompt += f"- {item['title']}\n"
            
            # 构建请求体
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的加密货币新闻分析师，请提供简洁、专业的新闻总结。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 300
            }
            
            # 发送请求
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/v1/chat/completions", headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        logger.error(f"LLM API 请求失败: {response.status}")
                        return "LLM 总结失败"
        except Exception as e:
            logger.error(f"LLM 总结失败: {str(e)}")
            return "LLM 总结失败"