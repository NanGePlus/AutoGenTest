import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.task import Console, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models import OpenAIChatCompletionClient
from autogen_agentchat.base import TaskResult




os.environ["OPENAI_BASE_URL"] = "https://api.wlai.vip/v1"
os.environ["OPENAI_API_KEY"] = "sk-OzsROOHNA58LNRx6Jt0da5CJYOH6RYPt1Ty1PqkrJrUxv3pk"



# 定义Tool
async def get_weather(city: str) -> str:
    return f"The weather in {city} is 73 degrees and Sunny."


async def main() -> None:
    # 定义Agent
    weather_agent = AssistantAgent(
        name="weather_agent",
        model_client=OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            # api_key="sk-OzsROOHNA58LNRx6Jt0da5CJYOH6RYPt1Ty1PqkrJrUxv3pk",
            # base_url="https://api.wlai.vip/v1"
        ),
        description="一个通过使用工具为用户提供天气信息的智能体。",
        system_message="你是一个乐于助人的AI智能助手。擅长使用工具解决任务。任务完成后，回复南哥AGI研习社",
        handoffs=None,
        tools=[get_weather],
    )

    # 定义终止条件  如果提到特定文本则终止对话
    termination = TextMentionTermination("南哥AGI研习社")

    # 定义Team Team的类型选择为RoundRobinGroupChat
    agent_team = RoundRobinGroupChat(participants=[weather_agent], termination_condition=termination, max_turns=None)

    # 1、run()方法运行team
    result = await agent_team.run(task="上海的天气如何?")
    print(result)

    # # 2、run_stream()方法运行team
    # async for message in agent_team.run_stream(task="上海的天气如何?"):
    #     if isinstance(message, TaskResult):
    #         print("Stop Reason:", message.stop_reason)
    #     else:
    #         print(message)

    # # 3、run_stream()方法运行team并使用官方提供的Console工具以适当的格式输出
    # stream = agent_team.run_stream(task="上海的天气如何?")
    # await Console(stream)


# 运行main
asyncio.run(main())

