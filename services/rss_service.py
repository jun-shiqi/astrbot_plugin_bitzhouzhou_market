import logging
import aiohttp
import feedparser

logger = logging.getLogger(__name__)

class RSSService:
    def __init__(self, news_url: str = None, flash_url: str = None):
        self.news_url = news_url if news_url else "https://rss.odaily.news/rss/post"
        self.flash_url = flash_url if flash_url else "https://rss.odaily.news/rss/newsflash"
    
    async def _fetch_rss(self, url: str):
        """获取 RSS 数据"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        return feedparser.parse(content)
                    else:
                        logger.error(f"RSS 请求失败: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"获取 RSS 数据失败: {str(e)}")
            return None
    
    async def get_news(self, limit: int = 5):
        """获取新闻数据"""
        if not self.news_url:
            return []
        
        feed = await self._fetch_rss(self.news_url)
        if not feed or not feed.get('entries'):
            return []
        
        news = []
        for entry in feed['entries'][:limit]:
            news.append({
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'summary': entry.get('summary', '')
            })
        return news
    
    async def get_flash(self, limit: int = 10):
        """获取快讯数据"""
        if not self.flash_url:
            return []
        
        feed = await self._fetch_rss(self.flash_url)
        if not feed or not feed.get('entries'):
            return []
        
        flash = []
        for entry in feed['entries'][:limit]:
            flash.append({
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'published': entry.get('published', '')
            })
        return flash