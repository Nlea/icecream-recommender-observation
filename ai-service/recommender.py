
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
mood = "adventourous"
weather = "Broken clouds"
location = "Berlin"
promp = "Please return 1 icecream falavour recommentation for my mood, the weather and the location I am based in. I want a recommendation for " + mood + " mood and for a " + weather +" day in " + location

client = OpenAI(
    # This is the default and can be omitted
    # api_key=os.environ.get("OPENAI_API_KEY"),
    
)

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": promp}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")