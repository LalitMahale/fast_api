from groq import Groq
import os
from text import mytext
from dotenv import load_dotenv
load_dotenv()

class Response:
    def __init__(self):
        self.client = Groq(api_key = os.getenv("GROQ_API"))
    
    def chatbot(self,query:str) -> str:
        try:
            res = self.client.chat.completions.create(
            messages=[
                {"role":"system",
                "content":f"You are a Question answer chatbot. You have to understand the given content based on that provide answer. If don't know tell unable to get details. only give answers do not provide addition text.",
                    "role": "user",
                    "content": f"Content : {mytext}\n\n Question : what is your name",
                }
            ],
            model="llama-3.3-70b-versatile",
        )
            return res.choices[0].message.content
        except Exception as e:
            print(e)




if __name__ == "__main__":
    res = Response().chatbot(query="hi")
    print(res)