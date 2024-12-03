import os
import asyncio
from autogen_agentchat.agents import AssistantAgent, Handoff
from autogen_agentchat.task import Console, TextMentionTermination, HandoffTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models import OpenAIChatCompletionClient




os.environ["OPENAI_BASE_URL"] = "https://api.wlai.vip/v1"
os.environ["OPENAI_API_KEY"] = "sk-OzsROOHNA58LNRx6Jt0da5CJYOH6RYPt1Ty1PqkrJrUxv3pk"




async def main() -> None:
    # 定义Agent
    weather_agent = AssistantAgent(
        name="weather_agent",
        model_client=OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            # api_key="sk-OzsROOHNA58LNRx6Jt0da5CJYOH6RYPt1Ty1PqkrJrUxv3pk",
            # base_url="https://api.wlai.vip/v1"
        ),
        description="一个和用户交互的智能体。",
        system_message="不知道答案时，一定要转给用户。任务完成后回复“南哥AGI研习社”",
        handoffs=[Handoff(target="user", message="移交给用户。")],
    )

    # 定义终止条件  如果提到特定文本则终止对话
    text_termination = TextMentionTermination("南哥AGI研习社")
    # 定义终止条件  在Agent发送HandoffMessage消息时终止对话
    handoff_termination = HandoffTermination(target="user")
    # 使用`|` 运算符组合终止条件，在满足任一条件时停止任务
    termination = handoff_termination | text_termination

    # 定义Team Team的类型选择为RoundRobinGroupChat
    agent_team = RoundRobinGroupChat(participants=[weather_agent], termination_condition=termination, max_turns=None)

    # 运行team并使用官方提供的Console工具以适当的格式输出
    stream = agent_team.run_stream(task="上海的天气如何?")
    await Console(stream)

    # 运行team并使用官方提供的Console工具以适当的格式输出
    stream = agent_team.run_stream(task="上海正在下雨,天气很糟糕。")
    await Console(stream)

# 运行main
asyncio.run(main())

