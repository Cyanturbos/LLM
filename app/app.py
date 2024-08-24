from openai import AsyncOpenAI
import chainlit as cl

# Create an AsyncOpenAI client
client = AsyncOpenAI()

# Default Settings for OpenAI API requests
settings = {
    "model": "gpt-4o-mini",
    "temperature": 0,
}

# Set the initial message history at the start of the chat
@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful bot."}],
    )

# Processing messages from the user interface
@cl.on_message
async def on_message(message: cl.Message):
    # Gets the message history of the current session
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    # Create an empty message object ready to stream content
    msg = cl.Message(content="")
    await msg.send()

    # Call the OpenAI API to enable streaming output
    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    # The content of the stream output is gradually received and sent to the front-end
    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    # Adds the content of the AI reply to the message history
    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()