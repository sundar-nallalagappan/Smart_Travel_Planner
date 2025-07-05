from langchain.tools import Tool
from src.tools.attract_activities import exploration
from src.tools.weather_analysis import get_real_time_weather

def attract_activities_tool():
    explore = exploration()
    attraction_tools = [
         Tool.from_function(
            name="Search_attraction",
            func=explore.search_attraction,
            description="Tool to search for the top tourist attractions in the requested holiday destination. Location(format:str) is the input and output is in string format."
         ),
         Tool.from_function(
            name="Search_key_restaurant",
            func=explore.search_restaurants,
            description="Tool to search for the top restaurants in the requested holiday destination. Location(format:str) is the input and output is in string format."
         ),
         Tool.from_function(
            name="Search_possible_transportation",
            func=explore.search_transporation,
            description="Tool to search for the transportation possibilities for the tourist in the requested holiday destination. Location(format:str) is the input and output is in string format."
         )
         ]
    print(attraction_tools)
    return attraction_tools

def weather_tool():
    return [get_real_time_weather]