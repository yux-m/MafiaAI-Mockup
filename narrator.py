from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai_client = OpenAI(base_url="https://api.openai.com/v1", api_key=os.getenv("OPENAI_API_KEY"))

def generate_narration(server, message):
    """
    generates the narrations given latest moves in the night
    TODO: what if we generated user personas based on the messages each player sends and used that to color narration
    """
    round, latest_death = server.predictorAI.world_facts[-1]

    if round==server.round:
        # there's been a death in the latest round
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": " %s." % word,
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1
            )
            joke = response.choices[0].message.content
            # print("Joke response:", joke)
            await message.channel.send(joke)
        except Exception as e:
            await message.channel.send("Sorry, openai isn't working")
            print(e) 
    
        return None
    else:
        # no deaths in the latest round
        return None


