from pyowm.owm import OWM
from langchain.tools import tool

@tool
def get_real_time_weather(location:str)->str:
    """
    Fetching real-time weather
    
    Args:
        location(str) : Location for which the real time weather details to be extracted
    
    Returns:
        str: Real time weather in celsius and detailed status
    """
    
    owm = OWM('1dcfe2a2cd866a984f6dc862bfc8a584')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(f"{location}")
    weather = observation.weather

    print(weather)
    print(f"Temp: {weather.temperature('celsius')['temp']} °C")
    print(f"Status: {weather.detailed_status}")
    
    return f"{location} Temperature: {weather.temperature('celsius')['temp']} °C & Status: {weather.detailed_status}"
