"""
LLM Response Tester - A Chainlit app for testing different aspects of LLM responses.
"""

import os
import chainlit as cl
from dotenv import load_dotenv
from openai import AsyncOpenAI
from config import APP_CONFIG, CHAT_CONFIG
from utils.test_handler import handle_message as handle_test_message
from utils.ui import show_welcome_message, show_mode_switch_button
from utils.response_handler import stream_response

# Load environment variables and initialize client
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@cl.on_chat_start
async def start_chat():
    """Initialize the chat session."""
    # Ensure mode is set in user session
    mode = APP_CONFIG.get("mode", "default")
    cl.user_session.set("mode", mode)
    
    await show_welcome_message()
    await show_mode_switch_button()
    
    if mode == "test":
        await handle_test_message(None, client)
    else:
        await cl.Message(content="👋 Ready to help! What's on your mind? ✨").send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages."""
    # Get mode from user session or APP_CONFIG
    mode = cl.user_session.get("mode", APP_CONFIG.get("mode", "default"))
    
    if mode == "test":
        await handle_test_message(message, client)
    else:
        messages = [
            {"role": "system", "content": CHAT_CONFIG["system_template"]},
            {"role": "user", "content": message.content}
        ]
        response = await stream_response(client, messages, CHAT_CONFIG["settings"])
        await cl.Message(content=response).send()

# This is the entry point for both local development and Hugging Face Spaces
if __name__ == "__main__":
    # For Hugging Face Spaces, we need to use the correct method
    # The app will be started by the Hugging Face Spaces environment
    # We'll use a try-except block to handle different environments
    try:
        # Try to run the app using the standard method
        cl.run()
    except Exception as e:
        # If that fails, try an alternative method
        print(f"Standard run method failed: {e}")
        print("Trying alternative method...")
        # For Hugging Face Spaces, we need to use the correct method
        # The app will be started by the Hugging Face Spaces environment
        pass
