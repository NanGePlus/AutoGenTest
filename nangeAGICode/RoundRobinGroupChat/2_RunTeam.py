import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.task import Console, MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models import OpenAIChatCompletionClient




os.environ["OPENAI_BASE_URL"] = "https://api.wlai.vip/v1"
os.environ["OPENAI_API_KEY"] = "sk-OzsROOHNA58LNRx6Jt0da5CJYOH6RYPt1Ty1PqkrJrUxv3pk"


# 定义LLM
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    # api_key="sk-OzsROOHNA58LNRx6Jt0da5CJYOH6RYPt1Ty1PqkrJrUxv3pk",
    # base_url="https://api.wlai.vip/v1"
)


async def main() -> None:
    # 定义Agent
    primary_agent = AssistantAgent(
        name="primary",
        model_client=model_client,
        system_message="你是一个乐于助人的AI智能助手。"
    )

    # 定义Agent
    critic_agent = AssistantAgent(
        name="critic",
        model_client=model_client,
        system_message="提供建设性反馈意见。记住只有当你的反馈意见得到处理后再允许回复 “南哥AGI研习社”。"

    )

    # 定义终止条件  如果提到特定文本则终止对话
    text_termination = TextMentionTermination("南哥AGI研习社")
    # 定义终止条件，在 5 条信息后停止任务
    max_message_termination = MaxMessageTermination(10)
    # 使用`|` 运算符组合终止条件，在满足任一条件时停止任务
    termination = text_termination | max_message_termination

    # 定义Team Team的类型选择为RoundRobinGroupChat
    reflection_team = RoundRobinGroupChat(participants=[primary_agent, critic_agent], termination_condition=termination, max_turns=None)

    # 1、运行team并使用官方提供的Console工具以适当的格式输出
    stream = reflection_team.run_stream(task="写一首关于秋季的短诗")
    await Console(stream)

    # # 2、恢复任务 同时保留上一个任务的上下文
    # stream = reflection_team.run_stream(task="将这首诗用英文写一遍。")
    # await Console(stream)

    # # 3、恢复前一个任务 不用传递具体任务 team将从上个任务中断的地方继续支持
    # stream = reflection_team.run_stream()
    # await Console(stream)

# 运行main
asyncio.run(main())

