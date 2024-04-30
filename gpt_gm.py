import os
import discord
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai_client = OpenAI(base_url="https://api.openai.com/v1", api_key=OPENAI_API_KEY)
intents = discord.Intents.all()
discord_client = discord.Client(intents=intents)

def read_rules(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("The rules file was not found.")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# Load Mafia game rules from a text file
# game_rules = read_rules("game_rules.txt")
# base_prompt = f"You are a game master of a party game. Game rules: {game_rules} \n\n"

base_prompt = 'You are a game master of a party game.'

game_log = []  # This will store all game-related commands and events
message_history = []  # This will store all messages for summarization

@discord_client.event
async def on_ready():
    print(f'Logged in as {discord_client.user}!')
    # game_rules = await discord_client.wait_for("Please enter the game rules for Mafia. Send them in a single message.")


@discord_client.event
async def on_message(message):
    message_history.append(f"{message.author}:{message.content}")

    if message.author == discord_client.user:
        game_log.append(f"{message.author}:{message.content}")
        return

    if message.content.startswith('m!'):
        game_log.append(f"{message.author}:{message.content}")

        if message.content == 'm!rules':
            game_rules = await discord_client.wait_for("Please enter the game rules for Mafia. Send them in a single message.")
            base_prompt = f"You are a game master of a party game. Game rules: {game_rules} \n\n"

        command = message.content[2:].strip()
        prompt = f"History and current state: {game_log_to_str} \n User command: {command} \n Now continue to host the game and speak as the game master"
        try:
            response = await gpt_query(message, messages=[
                {
                "role": "system",
                "content": base_prompt
                },
                {
                "role": "user",
                "content": prompt
                },
            ],)
            gpt_response = response['choices'][0]['text'].strip()
            if gpt_response:
                await message.channel.send(gpt_response)
        except Exception as e:
            print(e)
            await message.channel.send("Error processing your command. Please try again.")

def game_log_to_str():
    return "\n".join(game_log)

async def summarize_game():
    global base_prompt
    prompt = (base_prompt +
              f"Summarize the following game events into the current state of the game:\n{game_log_to_str()}")
    try:
        response = openai_client.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=250,  # Adjust max_tokens according to needs
            stop=None  # Ensure the model generates content until it deems complete
        )
        summarized_log = response['choices'][0]['text'].strip()
        global game_log
        game_log = [summarized_log]  # Replace the detailed log with the summarized one
    except Exception as e:
        print(f"Error during summarization: {e}")


async def gpt_query(message, messages):
    try:
        response = openai_client.chat.completions.create(
                messages= messages,
                model="gpt-3.5-turbo",
            )
        await message.channel.send(response.choices[0].message.content)
    except Exception as e:
        await message.channel.send("Unable to generate description")
        print(e)  # For debugging


discord_client.run(DISCORD_BOT_TOKEN)
