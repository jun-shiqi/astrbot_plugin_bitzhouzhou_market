# 比特周周加密市场分析插件

## 插件介绍

比特周周加密市场分析插件是一个为 AstrBot 设计的加密货币市场分析工具，提供以下功能：

- **价格预警**：支持按币种独立配置价格预警，可设置上涨/下跌百分比，绑定发送目标
- **市场播报**：定时推送行情分析、快讯和资讯
- **多目标发送**：支持向多个 QQ 好友和群发送消息
- **LLM 增强**：优先使用 LLM 进行行情分析

## 安装方法

1. 将插件目录 `astrbot_plugin_bitzhouzhou_market` 复制到 AstrBot 的插件目录
2. 重启 AstrBot 加载插件
3. 在 AstrBot 配置界面中配置插件参数

## 配置说明

插件提供完整的配置界面，主要配置项包括：

### 1. RSS 配置
- `news_url`：新闻 RSS URL
- `flash_url`：快讯 RSS URL

### 2. 发送目标配置
- `private_users`：QQ 好友列表
- `groups`：QQ 群列表

### 3. 价格预警配置
- `symbol`：交易对（如 BTC-USDT）
- `enable`：是否启用
- `up_percent`：上涨预警百分比
- `down_percent`：下跌预警百分比
- `interval_sec`：检测间隔（秒）
- `targets`：发送目标（可单独指定）

### 4. 播报配置
- `enable`：是否启用播报
- `interval_sec`：播报间隔（秒）
- `send_market`：是否发送行情分析
- `send_news`：是否发送资讯
- `send_flash`：是否发送快讯
- `targets`：发送目标

### 5. LLM 配置
- `enabled`：是否启用 LLM
- `api_key`：LLM API Key
- `base_url`：LLM API 基础 URL
- `model`：模型名称

## 命令系统

- `/bit 预警列表`：查看当前所有价格预警配置
- `/bit 添加预警 BTC`：添加 BTC 价格预警（可选）
- `/bit 删除预警 BTC`：删除 BTC 价格预警（可选）

## 项目结构

```
astrbot_plugin_bitzhouzhou_market/
├── core/
│   ├── alert.py          # 价格预警系统
│   ├── broadcaster.py    # 统一发送函数
│   ├── analyzer.py       # 市场分析器
├── services/
│   ├── okx_service.py    # OKX API 服务
│   ├── rss_service.py    # RSS 服务
│   ├── llm_service.py    # LLM 服务
├── main.py               # 插件入口
├── metadata.yaml         # 插件元数据
├── README.md             # 文档
├── _conf_schema.json     # 配置 schema
├── okxAPI.txt            # OKX API 文档
├── odailyRSS.txt         # Odaily RSS 文档
```

## 技术特点

- **配置驱动**：所有功能均可通过配置界面调整
- **模块化设计**：核心功能分离到不同模块
- **异步处理**：使用 async/await 提高性能
- **强异常处理**：确保插件稳定运行
- **多目标发送**：支持向多个 QQ 好友和群发送消息
- **预警绑定**：每个预警可单独指定发送目标

## 注意事项

- 请确保 LLM 配置正确，否则无法使用 LLM 增强功能
- 请合理设置预警间隔，避免频繁 API 请求
- 请确保机器人在指定的群中，否则群消息发送会失败

## 作者

比特周周技术助手 Hugh Orion

## 版本

v1.0.0