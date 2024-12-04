# 1、项目介绍
## 1.1、本次分享介绍                      
(1)AutoGen框架介绍                                                                             
(2)AutoGen功能测试               
相关视频:       
https://www.bilibili.com/video/BV1tGzSYxEZe/                               
https://youtu.be/jbEXvhWACqk                              

## 1.2 AutoGen介绍
AutoGen是微软发布的一个用于构建AI Agent系统的开源框架，简化了事件驱动、分布式、可扩展和弹性Agent应用程序的创建过程                     
通过AutoGen可以快速构建AI Agent协作的系统并自主或在人类监督下执行任务                      
github地址:https://github.com/microsoft/autogen                               
### (1)版本      
**AutoGen0.2**                  
当前的稳定版本，一直维护                       
**AutoGen0.4**                    
是最新架构的第一版本，此版本仍处于开发阶段                              
V0.4版本是对AutoGen的一次从头开始的重写，目的是为构建Agent创建一个更健壮、可扩展、更易用的跨语言库          
这是一个突破性的变化，该版本后续还会支持AutoGen Studio           
预计会在年底(2024)前发布0.4新版本             
本期视频内容均为使用V0.4版本进行相关介绍和代码测试             

### (2)核心功能       
**异步消息传递**              
Agent通过异步消息进行通信，支持事件驱动和请求/响应交互模式                 
**全面的类型支持**                   
在所有的接口中使用类型，并在构建时强制进行类型检查，注重质量和内聚性                  
**可拓展性和分布式**                  
设计复杂的分布式Agent应用网络，可跨组织边界运行                      
**模块化和可扩展**                             
利用可插拔组件定制系统，支持自定义Agent、工具、模型等                        
**跨语言支持**                  
跨不同编程语言，目前支持python和.NET，不久会支持更多语言                                
**可观察性和调试**                    
用于跟踪、追踪和调试Agent交互和工作流的内置功能和工具，包括支持行业标准的OpenTelemetry                 
                          
### (3)应用接口             
AutoGen的应用接口采用分层架构设计，存在多套软件接口                          
目前，应用程序可以使用3个主要应用接口:Core、AgentChat、Extensions                           
**Core:事件驱动型接口，核心接口，autogen-core**                        
按照Agent模式构建                      
支持Agent之间异步消息传递(类似于RPC)，或通过主题广播(类似pub/sub)来处理和生成类型化消息                       
Agent可以是分布式的，可以用不同的编程语言实现，同时还可以相互通信                      
如果要是想构建可扩展性的事件驱动Agent系统，可以从Core接口开始                    
**AgentChat:任务驱动型应用接口，autogen-agentchat**                      
建立在Core核心层之上，抽象了许多底层系统概念                     
允许定义会话Agent，将它们组织成Team，然后运行Team协作完成任务                      
如果要是只想基于任务去构建Agent系统，可以从AgentChat接口开始                      
**Extensions:第三方系统接口，扩展包，autogen-ext**                    
主要为第三方系统实现的核心接口，如OpenAI模型客户端接口等               
除内置扩展外，该扩展包还容纳社区贡献的扩展接口                  

### (4)Agent属性
**name**                   
指定Agent的名称                        
**model_client**                  
指定Agent使用的大语言模型              
**description**            
Agent的描述信息            
**handoffs**          
负责Agent的移交           
**system_message**                 
Agent的系统提示词                           
**tools**                    
提供给Agent使用的工具集合                

### (5)Team:官方提供5中预设Team
在AgentChat中Team由一个或多个Agent组成，定义了Agent组如何协作完成任务
Team通过接收任务和返回任务结果与应用程序交互                 
Team是有状态的，并在多个任务中保持上下文，需要终止条件来决定何时停止处理当前任务                                  
**BaseGroupChat**                    
Team的基类，其他4中Team预设类别均继承该基类                                      
**RoundRobinGroupChat**                   
该预设Team中的参与者(Agent)以顺序循环的方式轮流向所有参与者发布信息                   
该预设Team允许所有的Agent共享上下文，并以循环方式轮流做出响应            
其属性如下:         
participants:设置Team的参与者(Agent) ,List列表                           
termination_condition:Team终止条件，默认None则无限期运行              
max_turns:Team支持的最大会话回合数，默认None则无限制            
**SelectorGroupChat**                   
该预设Team中的参与者(Agent)以推荐选择的方式轮流向所有参与者发布信息                    
每次消息发布后，都会使用ChatCompletionClient(LLM)选择下一个发言者(Agent)                      
其属性如下:            
participants:设置Team的参与者(Agent) ,List列表                 
model_client:设置LLM，ChatCompletionClient             
termination_condition:Team终止条件，默认None则无限期运行                  
max_turns:Team支持的最大会话回合数，默认None则无限制                 
selector_prompt:用于选择下一个发言者(Agent)的prompt模版                   
allow_repeated_speaker:是否允许连续选择同一个发言者(Agent)，默认False则不允许                     
selector_func:自定义选择器函数，用于获取对话历史记录并返回下一个发言者(Agent),若启动该功能则LLM选择会失效，若该函数返回None,则LLM会主动接管进行下一位发言者(Agent)的选择                   
**Swarm**                   
该预设Team中的参与者(Agent)以移交方式向所有参与者发布信息                   
参与者列表中的第一个参与者是初始发言者，下一位发言者是根据HandoffsMessage消息中指定的参与者。若无移交信息，则当前发言者继续发言              
其属性如下:         
participants:设置Team的参与者(Agent) ,List列表                           
termination_condition:Team终止条件，默认None则无限期运行              
max_turns:Team支持的最大会话回合数，默认None则无限制    
**MagenticOneGroupChat**                   
官方正在开发中，相应源码暂没相关注释                                   
               
### (6)Team:运行接口
**run()**               
处理任务并返回任务结果             
**run_stream()**               
类似于run()，处理任务并返回异步生成器消息内容和最终任务结果             
**reset()**               
若上一个任务与下一个任务无关，则重置Team的状态            
否则，Team可以利用上一个任务的上下文来处理下一个任务            

### (7)Termination:终止Team 
Team运行后可以一直运行下去，在很多情况下需要知道何时停止运行，这就是终止条件的作用                 
终止条件是有状态的，但在每次运行run()或run_stream()结束后会自动重置              
多个终止条件支持使用AND或OR运算符进行组合                
目前支持如下8种终止条件:           
**MaxMessageTermination**
在生成指定数量的消息，包括Agent和Task消息后则终止                        
**TextMentionTermination**           
当在消息中提到特定的文本或字符串则终止                    
**TokenUsageTermination**             
当使用了一定数量的tokens时则终止                
**TimeoutTermination**           
在指定的持续时间(以秒为单位)后终止             
**HandoffTermination**          
在请求移交至特定目标后终止。特别适合需要用户干预的场景               
**SourceMatchTermination**             
在特定的Agent做出响应之后终止           
**ExternalTermination**             
允许从运行外部对终止进行控制。特被适合用户界面集成(如聊天中的停止按钮)场景                   
**StopMessageTermination**            
当Agent发出StopMessage时终止                   


# 2、前期准备工作
## 2.1 开发环境搭建:anaconda、pycharm
anaconda:提供python虚拟环境，官网下载对应系统版本的安装包安装即可                                      
pycharm:提供集成开发环境，官网下载社区版本安装包安装即可                                               
可参考如下视频进行安装，【大模型应用开发基础】集成开发环境搭建Anaconda+PyCharm                                                          
https://www.bilibili.com/video/BV1q9HxeEEtT/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                             
https://youtu.be/myVgyitFzrA          

## 2.2 大模型相关配置
(1)GPT大模型使用方案              
(2)非GPT大模型(国产大模型)使用方案(OneAPI安装、部署、创建渠道和令牌)                 
(3)本地开源大模型使用方案(Ollama安装、启动、下载大模型)                         
可参考如下视频:                         
提供一种LLM集成解决方案，一份代码支持快速同时支持gpt大模型、国产大模型(通义千问、文心一言、百度千帆、讯飞星火等)、本地开源大模型(Ollama)                       
https://www.bilibili.com/video/BV12PCmYZEDt/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                 
https://youtu.be/CgZsdK43tcY           


# 3、项目初始化
## 3.1 下载源码
GitHub或Gitee中下载工程文件到本地，下载地址如下：                
https://github.com/NanGePlus/AutoGenTest                                                               
https://gitee.com/NanGePlus/AutoGenTest                                    

## 3.2 构建项目
使用pycharm构建一个项目，为项目配置虚拟python环境               
项目名称：AutoGenTest                                                 

## 3.3 将相关代码拷贝到项目工程中           
直接将下载的文件夹中的文件拷贝到新建的项目目录中               

## 3.4 安装项目依赖          
命令行终端中执行如下命令安装依赖包            
pip install 'autogen-agentchat==0.4.0.dev8'                                                       
pip install 'autogen-ext[openai]==0.4.0.dev8'                
pip install asyncio==3.4.3               

# 4、测试
相关测试代码在nangeAGICode/RoundRobinGroupChat文件夹下               


   






















