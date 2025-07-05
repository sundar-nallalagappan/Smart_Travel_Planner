from src.prompt import attaction_prompt, weather_prompt
from src.tool_aggregator import attract_activities_tool, weather_tool

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated, Sequence, List, Dict
from langchain_core.messages import BaseMessage
from src.llm import initiate_llm
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from src.prompt import final_planner
from langchain_core.prompts import PromptTemplate
from typing import Optional

class FinalPlanner(BaseModel):
    attactions_activities: Optional[str]=Field(description="Important attractions & key activities in the requested destination")
    lodging_choices: Optional[str]=Field(description="Available lodging options to stay if requested by the customer")
    local_transport: Optional[str]=Field(description="Possible local transportation options available to commute within the city")
    weather_details: Optional[str]=Field(description="Suggestions based on the weather during the stay. 2 lines about points to pay attention")
    itenary        : Optional[str]=Field(description="Day to day itenary plan with bulleted points based on attactions & activies")

parser=PydanticOutputParser(pydantic_object=FinalPlanner)

    
attraction_tools = attract_activities_tool()
weather_tool     = weather_tool()
llm              = initiate_llm()

llm_with_attraction_tools = llm.bind_tools(attraction_tools)
llm_with_weather_tool     = llm.bind_tools(weather_tool)

def attractions_activities(state: MessagesState):
    question = state['messages']
    print(f'attractions_activities-question: {question}')
    final_promt = [attaction_prompt] + question
    #print(f'final_promt: {final_promt}')
    
    response=llm_with_attraction_tools.invoke(final_promt)

    #print(f"response: {response}  TYPE: {type(response)}")
    return_state = {
    #"messages": state["messages"] + [response]
    "messages": [response]
    }
    print(f"[RETURNING STATE] = {return_state}")
    return return_state

def analyze_weather(state: MessagesState):
    question = state['messages'][0]
    print(f'analyze_weather-question: {question}')
    final_promt = [weather_prompt] + [question]
    #print(f'final_promt: {final_promt}')
    
    response=llm_with_weather_tool.invoke(final_promt)

    return_state = {
    #"messages": state["messages"] + [response]
    "messages": [response]
    }
    print(f"[RETURNING STATE] = {return_state}")
    return return_state
    
    
def finalize_plan(state:MessagesState):
    print('finalize_plan')

    
    #all_messages = state["messages"]
    #final_planner_template = final_planner.format(question=state["messages"][0].content, 
    #                                            format_instructions=parser.get_instructions())
    prompt = PromptTemplate(
        template=final_planner,
        input_variables=['question', 'plan_details'],
        partial_variables={"format_instructions":parser.get_format_instructions()}
    )
    
    plan_details_text = "\n".join(f"{type(m).__name__}: {m.content}" for m in state["messages"])
                                
    chain = prompt | llm | parser
    llm_response = chain.invoke({'question': state["messages"][0].content,
                                'plan_details': plan_details_text})
        
    print("Finalize plan:", llm_response) 
    response_text = llm_response.model_dump_json(indent=2) 
    
    return_state = {
    #"messages": state["messages"] + [response]
    "messages": [AIMessage(content=response_text)]
    }
    print(f"[RETURNING STATE] = {llm_response}")
    return return_state
    
    
    '''
    for msg in all_messages:
        print(f"Type: {type(msg).__name__}")
        print(f"Content: {msg.content}")
        print(f"Additional kwargs: {msg.additional_kwargs}")
        print("-" * 50)
    '''    
        
def route_from_attraction_llm(state: MessagesState) -> str:
    last = state["messages"][-1]
    print(f'route from attaraction llm: {last}, {last.additional_kwargs}')
    
    if isinstance(last, AIMessage) and "tool_calls" in last.additional_kwargs:
        return "attraction_tools"
    else:
        return "Analyze_Weather" 
