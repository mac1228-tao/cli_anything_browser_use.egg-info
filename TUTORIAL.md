# Browser-Use CLI 完整教程

本教程将详细介绍如何安装和使用 `cli-anything-browser-use`，这是一个基于 browser-use 库的 AI 浏览器自动化命令行工具。

## 目录

1. [环境准备](#1-环境准备)
2. [安装 CLI](#2-安装-cli)
3. [基本使用](#3-基本使用)
4. [DeepAgent 集成示例](#4-deepagent-集成示例)
5. [进阶用法](#5-进阶用法)
6. [常见问题](#6-常见问题)

---

## 1. 环境准备

### 1.1 安装 Python 依赖

首先，确保你的系统已经安装了 Python 3.10 或更高版本：

```bash
# 检查 Python 版本
python3 --version
```

### 1.2 安装 browser-use 库

```bash
# 使用 uv 安装 browser-use（推荐）
uv add browser-use

# 或者使用 pip
pip install browser-use
```

### 1.3 安装 Chromium 浏览器

browser-use 需要 Chromium 浏览器来控制浏览器：

```bash
# 安装 Chromium 和系统依赖
uvx browser-use install
```

### 1.4 配置 API 密钥

创建一个 `.env` 文件来存储你的 API 密钥：

```bash
# 创建 .env 文件
touch .env
```

编辑 `.env` 文件，添加以下内容（选择其中一个）：

```bash
# 方式 1: 使用 Browser Use Cloud（推荐）
BROWSER_USE_API_KEY=your-browser-use-api-key

# 方式 2: 使用 OpenAI
# OPENAI_API_KEY=your-openai-api-key

# 方式 3: 使用 Anthropic
# ANTHROPIC_API_KEY=your-anthropic-api-key

# 方式 4: 使用 Google
# GOOGLE_API_KEY=your-google-api-key
```

获取 API 密钥：
- Browser Use Cloud: https://cloud.browser-use.com/new-api-key
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Google: https://aistudio.google.com/app/apikey

---

## 2. 安装 CLI

### 2.1 克隆或下载 CLI-Anything

```bash
# 进入 CLI-Anything 目录
cd /home/ubuntu/program/CLI-Anything/browser-use/agent-harness

# 或者如果你是从 GitHub 克隆
# git clone https://github.com/HKUDS/CLI-Anything.git
# cd CLI-Anything/browser-use/agent-harness
```

### 2.2 安装 CLI 包

```bash
# 使用 pip 安装为可编辑模式
pip install -e .

# 或者安装为标准包
# pip install .
```

### 2.3 验证安装

```bash
# 检查 CLI 是否安装成功
cli-anything-browser-use --help
```

你应该看到类似的输出：

```
Usage: python -m cli_anything.browser_use [OPTIONS] COMMAND [ARGS]...

  Browser-Use CLI — AI-powered browser automation.

  Run without a subcommand to enter interactive REPL mode.

Options:
  --json  Output as JSON
  --help  Show this message and exit.

Commands:
  agent    Agent commands for running browser automation tasks.
  browser  Browser session management commands.
  config   Configuration management commands.
  repl     Start interactive REPL session.
  session  Session management commands.
```

---

## 3. 基本使用

### 3.1 一次性命令模式

#### 运行自动化任务

```bash
# 运行一个简单的任务
cli-anything-browser-use agent run "搜索今天的天气"

# 指定模型
cli-anything-browser-use agent run "搜索新闻" --model gpt-4

# 限制最大步数
cli-anything-browser-use agent run "打开百度" --max-steps 10
```

#### 浏览器控制

```bash
# 打开网页
cli-anything-browser-use browser open https://www.example.com

# 获取浏览器信息
cli-anything-browser-use browser info

# 截图
cli-anything-browser-use browser screenshot -p screenshot.png

# 关闭浏览器
cli-anything-browser-use browser close
```

#### 会话管理

```bash
# 查看当前会话状态
cli-anything-browser-use session status

# 保存当前会话
cli-anything-browser-use session save my-work

# 加载已有会话
cli-anything-browser-use session load my-work

# 列出所有保存的会话
cli-anything-browser-use session list
```

#### 配置管理

```bash
# 查看当前配置
cli-anything-browser-use config show

# 设置配置项
cli-anything-browser-use config set model gpt-4
```

### 3.2 JSON 输出模式

所有命令都支持 `--json` 参数，方便程序解析：

```bash
# 获取 JSON 格式的会话状态
cli-anything-browser-use --json session status

# 输出示例
# {
#   "context": "browser-use",
#   "history_length": 0,
#   "undo_stack_length": 0,
#   "redo_stack_length": 0,
#   "session_dir": "/home/user/.cli-anything-browser-use/sessions"
# }
```

### 3.3 交互式 REPL 模式

不指定子命令时，将进入交互式 REPL 模式：

```bash
# 启动 REPL
cli-anything-browser-use
```

在 REPL 中，你可以输入命令：

```
◆  cli-anything · Browser-Use    v1.0.0   
│   Type help for commands, quit to exit    │
╰────────────────────────────────────────────╯

browser-use ❯ agent run 搜索今天的天气
browser-use ❯ browser open https://www.baidu.com
browser-use ❯ session save my-session
browser-use ❯ quit
```

---

## 4. DeepAgent 集成示例

### 4.1 什么是 DeepAgent？

DeepAgent 是一个深度学习代理框架，可以与 browser-use 集成来实现更智能的浏览器自动化。

### 4.2 在 Python 代码中使用

以下是一个完整的示例，展示如何在 Python 脚本中使用 browser-use：

```python
#!/usr/bin/env python3
"""
Browser-Use DeepAgent 示例
这个示例展示如何创建 AI 浏览器代理并执行自动化任务
"""

import asyncio
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入 browser-use
from browser_use import Agent, Browser, BrowserSession
from browser_use.agent.views import AgentHistoryList


async def example_basic_task():
    """示例 1: 基础任务"""
    print("=" * 50)
    print("示例 1: 执行基础任务")
    print("=" * 50)
    
    # 创建浏览器会话
    browser = Browser(
        headless=False,  # 设置为 True 可以无头运行
    )
    
    # 创建代理
    agent = Agent(
        task="打开百度并搜索 'browser-use'",
        llm=None,  # 将使用默认的 ChatBrowserUse
        browser=browser,
    )
    
    # 运行代理
    history = await agent.run()
    
    # 输出结果
    print(f"完成任务: {history.is_done()}")
    print(f"访问的URL: {history.urls()}")
    print(f"执行步数: {history.number_of_steps()}")
    print(f"最终结果: {history.final_result()}")
    
    # 关闭浏览器
    await browser.close()


async def example_with_custom_llm():
    """示例 2: 使用自定义 LLM"""
    print("=" * 50)
    print("示例 2: 使用自定义 LLM")
    print("=" * 50)
    
    from browser_use import ChatOpenAI, ChatAnthropic, ChatGoogle
    
    browser = Browser(headless=True)
    
    # 使用 OpenAI
    llm = ChatOpenAI(model="gpt-4")
    
    # 或使用 Anthropic
    # llm = ChatAnthropic(model="claude-sonnet-4-20250514")
    
    # 或使用 Google
    # llm = ChatGoogle(model="gemini-2.0-flash")
    
    agent = Agent(
        task="访问 GitHub 并获取 browser-use 仓库的 star 数量",
        llm=llm,
        browser=browser,
    )
    
    history = await agent.run()
    print(f"Star 数量: {history.final_result()}")
    
    await browser.close()


async def example_with_tools():
    """示例 3: 使用自定义工具"""
    print("=" * 50)
    print("示例 3: 使用自定义工具")
    print("=" * 50)
    
    from browser_use import Agent, Controller, Tools, ActionResult
    from browser_use.browser.session import BrowserSession
    
    # 创建控制器和自定义工具
    controller = Controller()
    
    @controller.action("获取当前时间")
    def get_current_time() -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @controller.action("计算器")
    def calculator(a: int, b: int, operation: str = "add") -> int:
        if operation == "add":
            return a + b
        elif operation == "sub":
            return a - b
        elif operation == "mul":
            return a * b
        elif operation == "div":
            return a // b if b != 0 else 0
        return 0
    
    browser = Browser(headless=True)
    
    agent = Agent(
        task="打开计算器网站或使用内置的计算器工具计算 10 + 20",
        controller=controller,
        browser=browser,
    )
    
    history = await agent.run()
    print(f"计算结果: {history.final_result()}")
    
    await browser.close()


async def example_structured_output():
    """示例 4: 结构化输出"""
    print("=" * 50)
    print("示例 4: 结构化输出")
    print("=" * 50)
    
    from pydantic import BaseModel
    from browser_use import Agent
    
    # 定义输出模型
    class SearchResult(BaseModel):
        title: str
        url: str
        snippet: str
    
    class NewsSummary(BaseModel):
        headlines: list[str]
        source: str
        date: str
    
    browser = Browser(headless=True)
    
    agent = Agent(
        task="搜索最新的 AI 新闻并返回 3 条标题",
        browser=browser,
        output_model_schema=NewsSummary,
    )
    
    history = await agent.run()
    
    # 获取结构化输出
    result = history.structured_output
    if result:
        print(f"新闻来源: {result.source}")
        print(f"日期: {result.date}")
        print("标题列表:")
        for i, headline in enumerate(result.headlines, 1):
            print(f"  {i}. {headline}")
    
    await browser.close()


async def example_session_persistence():
    """示例 5: 会话持久化"""
    print("=" * 50)
    print("示例 5: 会话持久化")
    print("=" * 50)
    
    browser = Browser(headless=True)
    
    # 创建代理
    agent = Agent(
        task="打开百度并搜索 'Python'",
        browser=browser,
    )
    
    # 运行任务
    history = await agent.run()
    
    # 保存会话状态
    # browser_use 支持保存浏览器状态
    print(f"任务完成，访问了 {len(history.urls())} 个页面")
    
    # 关闭浏览器
    await browser.close()


async def example_multi_step_workflow():
    """示例 6: 多步骤工作流"""
    print("=" * 50)
    print("示例 6: 多步骤工作流")
    print("=" * 50)
    
    browser = Browser(headless=True)
    
    # 复杂任务示例
    task = """
    1. 打开 https://news.ycombinator.com/
    2. 获取前 5 条新闻的标题和链接
    3. 点击第一个链接
    4. 提取页面内容
    5. 返回结果
    """
    
    agent = Agent(
        task=task,
        browser=browser,
        max_steps=20,
    )
    
    history = await agent.run()
    
    print(f"完成状态: {history.is_done()}")
    print(f"总步数: {history.number_of_steps()}")
    print(f"最终结果: {history.final_result()}")
    
    await browser.close()


async def example_with_options():
    """示例 7: 高级选项"""
    print("=" * 50)
    print("示例 7: 高级选项配置")
    print("=" * 50)
    
    browser = Browser(
        headless=True,
        window_size={'width': 1920, 'height': 1080},
        # 启用下载
        accept_downloads=True,
        downloads_path='./downloads',
        # 代理配置
        # proxy=ProxySettings(server="http://proxy:8080"),
    )
    
    agent = Agent(
        task="下载 Python 官网的 Logo 图片",
        browser=browser,
        # 视觉选项
        use_vision=True,
        vision_detail_level='high',
        # 行为选项
        max_steps=50,
        max_actions_per_step=3,
        max_failures=5,
        # 初始动作
        initial_actions=[
            {'go_to_url': {'url': 'https://www.python.org/'}}
        ],
    )
    
    history = await agent.run()
    print(f"下载完成: {history.is_done()}")
    
    await browser.close()


async def main():
    """运行所有示例"""
    # 确保 .env 文件已加载
    load_dotenv()
    
    # 注意: 运行这些示例需要有效的 API 密钥
    # 注释掉你不想要运行的示例
    
    try:
        # await example_basic_task()
        # await example_with_custom_llm()
        # await example_with_tools()
        # await example_structured_output()
        # await example_session_persistence()
        # await example_multi_step_workflow()
        # await example_with_options()
        
        print("\n所有示例完成!")
        
    except Exception as e:
        print(f"运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
```

### 4.3 在 CLI 中使用 DeepAgent 风格的工作流

```bash
# 使用 CLI 执行复杂工作流

# 1. 打开浏览器并导航
cli-anything-browser-use browser open https://news.ycombinator.com

# 2. 保存会话状态
cli-anything-browser-use session save hn-research

# 3. 查看历史
cli-anything-browser-use agent history

# 4. 撤销操作
cli-anything-browser-use agent undo

# 5. 重做操作
cli-anything-browser-use agent redo
```

### 4.4 完整的自动化脚本示例

创建一个自动化脚本来执行复杂的浏览器任务：

```python
#!/usr/bin/env python3
"""
DeepAgent 自动化脚本示例
执行一个完整的新闻研究工作流
"""

import asyncio
import json
from datetime import datetime
from browser_use import Agent, Browser, ChatBrowserUse
from browser_use.agent.views import AgentHistoryList


class NewsResearchAgent:
    """新闻研究代理"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.agent = None
        self.results = []
    
    async def initialize(self):
        """初始化浏览器和代理"""
        self.browser = Browser(headless=self.headless)
        self.agent = Agent(
            task="",  # 稍后设置
            llm=ChatBrowserUse(),
            browser=self.browser,
            max_steps=100,
        )
    
    async def search_news(self, topic: str, num_results: int = 5):
        """搜索新闻"""
        task = f"""
        1. 打开 Google 新闻: https://news.google.com
        2. 搜索 "{topic}"
        3. 获取前 {num_results} 条新闻的:
           - 标题
           - 来源
           - 发布日期
           - 链接
        4. 以结构化格式返回结果
        """
        
        self.agent.task = task
        history = await self.agent.run()
        
        self.results = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "num_results": history.number_of_steps(),
            "urls": history.urls(),
            "final_result": history.final_result(),
        }
        
        return self.results
    
    async def extract_content(self, url: str):
        """提取页面内容"""
        task = f"""
        1. 打开: {url}
        2. 提取页面的:
           - 标题
           - 主要内容
           - 关键信息
        3. 返回提取的内容
        """
        
        self.agent.task = task
        history = await self.agent.run()
        
        return history.final_result()
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
    
    def save_results(self, filepath: str):
        """保存结果到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {filepath}")


async def main():
    """主函数"""
    # 创建研究代理
    agent = NewsResearchAgent(headless=True)
    
    try:
        # 初始化
        await agent.initialize()
        print("代理已初始化")
        
        # 搜索 AI 新闻
        print("\n搜索 AI 新闻...")
        results = await agent.search_news("人工智能", num_results=5)
        print(f"找到 {results['num_results']} 个步骤")
        print(f"访问的URL: {results['urls']}")
        
        # 保存结果
        agent.save_results("news_research.json")
        
        # 如果有结果，提取第一个链接的内容
        if results['urls']:
            print(f"\n提取内容: {results['urls'][0]}")
            content = await agent.extract_content(results['urls'][0])
            print(f"内容: {content[:200]}...")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理
        await agent.close()
        print("\n代理已关闭")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 5. 进阶用法

### 5.1 配置文件

创建 `browser-use-config.json` 来存储默认配置：

```json
{
  "model": {
    "provider": "browser-use",
    "temperature": 0.0
  },
  "browser": {
    "headless": false,
    "window_size": {
      "width": 1920,
      "height": 1080
    },
    "accept_downloads": true,
    "downloads_path": "./downloads"
  },
  "agent": {
    "max_steps": 100,
    "max_actions_per_step": 3,
    "use_vision": true
  }
}
```

### 5.2 自定义工具

```python
from browser_use import Controller

controller = Controller()

@controller.action("发送邮件")
async def send_email(to: str, subject: str, body: str):
    # 实现发送邮件逻辑
    return f"邮件已发送到: {to}"

agent = Agent(
    task="联系 support@example.com 关于技术问题",
    controller=controller,
    browser=browser,
)
```

### 5.3 错误处理和重试

```python
from browser_use import Agent

agent = Agent(
    task="执行任务",
    browser=browser,
    max_failures=3,  # 失败后重试次数
    final_response_after_failure=True,  # 失败后尝试返回结果
)
```

---

## 6. 常见问题

### Q1: 浏览器无法启动

**解决方案:**
```bash
# 重新安装 Chromium
uvx browser-use install

# 或者手动安装
# apt-get install chromium-browser
```

### Q2: API 密钥错误

**解决方案:**
```bash
# 检查 .env 文件
cat .env

# 确保 API 密钥正确设置
export BROWSER_USE_API_KEY=your-key
```

### Q3: 页面加载超时

**解决方案:**
```python
browser = Browser(
    headless=True,
    minimum_wait_page_load_time=1.0,  # 增加等待时间
    wait_for_network_idle_page_load_time=1.0,
)
```

### Q4: 如何实现无头模式

```python
browser = Browser(headless=True)  # 默认就是无头模式
```

### Q5: 如何保持浏览器会话

```python
browser = Browser(
    keep_alive=True,  # 任务完成后保持浏览器打开
)
```

### Q6: 如何处理下载

```python
browser = Browser(
    accept_downloads=True,
    downloads_path="/path/to/downloads",
)
```

---

## 参考资料

- [browser-use 官方文档](https://docs.browser-use.com)
- [browser-use GitHub](https://github.com/browser-use/browser-use)
- [CLI-Anything 项目](https://github.com/HKUDS/CLI-Anything)

---

## 下一步

1. 尝试运行示例代码
2. 探索更多 browser-use 功能
3. 创建自己的自动化工作流
4. 贡献到 CLI-Anything 项目
