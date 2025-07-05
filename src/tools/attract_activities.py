from langchain_openai import ChatOpenAI
from langchain_community.tools import TavilySearchResults

class exploration:
    def __init__(self):
        self.tavily   = TavilySearchResults(max_results=3)
        
    def summarizer(self,results, instruction):
        input_messages = [{"role": "user", "content": f"{instruction}: {results}"}]
        summarizer = ChatOpenAI(model="o3-mini")
        summary=summarizer.invoke(input_messages)
        return summary
    
    def search_attraction(self, location:str):
        attraction_search_results = self.tavily.run(f"Top tourist attractions, must try tourist activities & current important events in {location}")
        
        instruction = "Extract the tourist attraction places from the provided context. Later this will be used for travel & trip planning"
        if isinstance(attraction_search_results, list):
            full_string = '\n'.join(rec['content'] for rec in attraction_search_results)
            #print('full_string:', full_string)
            attraction_results = self.summarizer(full_string, instruction)
        else:
            attraction_results = self.summarizer(attraction_search_results, instruction)
        return attraction_results

    def search_restaurants(self, location:str):
        restaurant_search_results = self.tavily.run(f"Significant Restaurants(all budget ranges) for a tourist to try in {location}")
        #print(f"restaurant results: {restaurant_search_results}]")
        
        instruction = "Extract the ssignificant restaurants & cost associated from the provided context. Later this will be used for travel & trip planning"
        if isinstance(restaurant_search_results, list):
            full_string = '\n'.join(rec['content'] for rec in restaurant_search_results)
            #print('full_string:', full_string)
            restaurant_results = self.summarizer(full_string, instruction)
        else:
            restaurant_results = self.summarizer(restaurant_search_results, instruction)
        return restaurant_results
    
    def search_transporation(self, location:str):
        transport_search_results = self.tavily.run(f"Possible local transportation & cost details for a tourist to commute {location}")
        #print(f"transport_search_results: {transport_search_results}]")
        
        instruction = "Extract the Possible transportation details for a tourist to commute from the provided context. Later this will be used for travel & trip planning"
        if isinstance(transport_search_results, list):
            full_string = '\n'.join(rec['content'] for rec in transport_search_results)
            #print('full_string:', full_string)
            transport_results = self.summarizer(full_string, instruction)
        else:
            transport_results = self.summarizer(transport_search_results, instruction)
        return transport_results 
