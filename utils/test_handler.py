"""
Test handler module for managing test mode functionality in the LLM Response Tester.
"""

import chainlit as cl
from config import APP_CONFIG, TEST_CONFIG
from utils.response_handler import generate_comparison
from utils.ui import show_mode_switch_button, show_test_options, show_mode_transition

# List of keys that are not test configurations
NON_TEST_KEYS = {"settings", "enabled", "auto_test", "log_level"}

@cl.action_callback("switch_mode")
async def switch_mode():
    """Switch between test and default modes."""
    # Safely get current mode
    current_mode = APP_CONFIG.get("mode", "default")
    new_mode = "test" if current_mode == "default" else "default"
    
    # Update APP_CONFIG
    APP_CONFIG["mode"] = new_mode
    
    # Update user session
    cl.user_session.set("mode", new_mode)
    
    await show_mode_transition(new_mode == "test")

@cl.action_callback("select_test1")
@cl.action_callback("select_test2")
@cl.action_callback("select_test3")
@cl.action_callback("select_test4")
@cl.action_callback("select_test5")
async def on_test_select(action: cl.Action):
    """Handle test selection."""
    test_key = action.value
    test_config = TEST_CONFIG[test_key]
    
    message = cl.Message(content=test_config["example"])
    await generate_comparison(message, cl.user_session.get("client"), test_config)
    await show_test_options()

async def show_mode_switch_button():
    """Display the mode switch button."""
    mode_emoji = "🧪" if APP_CONFIG["mode"] == "test" else "💬"
    switch_to = "chat" if APP_CONFIG["mode"] == "test" else "test"
    
    await cl.Message(
        content=f"{mode_emoji} Currently in {APP_CONFIG['mode']} mode",
        actions=[
            cl.Action(
                name="switch_mode",
                value="switch",
                label=f"Switch to {switch_to} mode",
                description=f"Try {switch_to} mode instead"
            )
        ]
    ).send()

async def show_test_options():
    """Display available test options to the user."""
    actions = [
        cl.Action(
            name=f"select_{test_key}",
            value=test_key,
            label=config["label"],
            description=config["description"]
        )
        for test_key, config in TEST_CONFIG.items()
        if test_key not in NON_TEST_KEYS
    ]
    
    await cl.Message(
        content="🧪 Choose your experiment:",
        actions=actions
    ).send()

async def handle_message(message: cl.Message, client):
    """Main entry point for handling messages in test mode."""
    cl.user_session.set("client", client)
    await show_test_options()
    return True

async def switch_to_test_mode():
    """Switch to test mode and show test options."""
    await cl.Message(content="🧪 Entering test lab...").send()
    await show_mode_switch_button()
    await show_test_options()

async def switch_to_default_mode():
    """Switch to default mode and show welcome message."""
    await cl.Message(content="💬 Switching to chat mode...").send()
    await show_mode_switch_button()
    await cl.Message(content="👋 Ready for a chat! What's on your mind? ✨").send() 