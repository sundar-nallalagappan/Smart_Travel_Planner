from src.prompt import attaction_prompt, weather_prompt

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated, Sequence, List, Dict
from langchain_core.messages import BaseMessage
import operator
from src.node import attractions_activities, analyze_weather, finalize_plan, route_from_attraction_llm
from src.tool_aggregator import attract_activities_tool, weather_tool

attraction_tools = attract_activities_tool()
weather_tool     = weather_tool()
    
def workflow():
    workflow = StateGraph(MessagesState)
    workflow.add_node("Trip Attractions", attractions_activities)
    workflow.add_node("attraction_tools", ToolNode(attraction_tools))

    workflow.add_node("Analyze_Weather", analyze_weather)
    workflow.add_node("weather_tools", ToolNode(weather_tool))

    workflow.add_node("Finalize Plan", finalize_plan)

    workflow.add_edge(START, "Trip Attractions")
    workflow.add_conditional_edges("Trip Attractions", route_from_attraction_llm,
                                {
                                    'attraction_tools':'attraction_tools',
                                    'Analyze_Weather':'Analyze_Weather'
                                })
    workflow.add_edge('attraction_tools', "Trip Attractions")



    workflow.add_edge("Analyze_Weather", 'weather_tools')
    workflow.add_edge("weather_tools", "Finalize Plan")


    workflow.add_edge("Finalize Plan", END)

    app = workflow.compile()
    return app