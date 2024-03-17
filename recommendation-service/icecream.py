import os
from dotenv import load_dotenv
from openai import OpenAI

class IcecreamRecommendation:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    def get_recommendation(self, **input):

        print(input)
        try:
        
           name= input["name"]
           diet =input["dietRestrictions"]
           mood = input["mood"]
           location = input["location"]
           weather = input["weather"]

        except:
            name = "Nele"
            diet = "vegan"
            mood = "sleepy"
            location = "Zurich"
            weather = "rainy"
        promp = ""

        if 'dietRestrictions' not in input:
            promp = f"Please return 1 ice cream flavor recommendation for {name}'s mood, the weather, and the location they are based in. Please return a recommendation for a {mood} mood and for a {weather} in {location}. Please address the person by their name."
        elif 'weather' not in input:
            promp = f"Please return 1 ice cream flavor recommendation for {name} mood and their diet restriction: {mood} mood and {diet} diet. Please address the person by their name."
        else:
            promp = f"Please return 1 ice cream flavor recommendation for {name} mood, their diet restriction, the weather, and the location they are based in. Please return a recommendation for a {mood} mood and for a {diet} diet and for a {weather} day in {location}. Please address the person by their name."

        print(promp)


        stream = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": promp}],
            stream=True,
        )
        recommendation = ""
        for chunk in stream:
            recommendation += chunk.choices[0].delta.content or ""
        return recommendation