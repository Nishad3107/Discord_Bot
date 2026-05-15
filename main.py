import os
import discord
from discord.ext import commands
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)


@bot.command(name="gemini")
async def query(ctx, *, question):
    if not question:
        await ctx.send("Please provide a question!")
        return

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(question)
        if response and hasattr(response, "text"):
            response_text = response.text
            for chunk in [
                response_text[i : i + 1900] for i in range(0, len(response_text), 1900)
            ]:
                await ctx.send(chunk)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


bot.run(DISCORD_TOKEN)
