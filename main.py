import openai
import telegram
import os
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters

load_dotenv()

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = os.getenv(key="OPENAI_API_KEY")

# Replace YOUR_BOT_TOKEN with the token you received from the BotFather
bot = telegram.Bot(token=os.getenv(key="BOT_TOKEN"))

conversation = []

retention = 15


def handle_message(update, context):
    global conversation

    # Get the text of the message
    try:
        text = update.message.text

        conversation.append(text)

        prompt = "\n\n".join(conversation[-retention:])

        print("Prompt: ", prompt)

    # Use GPT-3 to generate a response to the message
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            temperature=0.7,
        )

        conversation.append(response.choices[0].text)

        # Send the response to the user
        update.message.reply_text(response.choices[0].text)

    except Exception as e:
        print(e)
        update.message.reply_text("Error: " + str(e))
        conversation = []


# Set up a handler for incoming messages
updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher
message_handler = MessageHandler(Filters.text, handle_message)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()
