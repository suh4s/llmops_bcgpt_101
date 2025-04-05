"""
UI Components Module - Handles all UI-related functionality.
"""

import chainlit as cl
from config import APP_CONFIG, TEST_CONFIG
from typing import List

# Constants
NON_TEST_KEYS = {"settings", "enabled", "auto_test", "log_level"}

async def show_welcome_message():
    """Display the welcome message."""
    # Safely get mode from APP_CONFIG
    mode = APP_CONFIG.get("mode", "default")
    
    await cl.Message(content=f"""
```
✨ Welcome to the AI Lab! ✨

╭──────────────────────────────╮
│  🎯 Mode: {mode.upper()}           │
│  🤖 GPT-3.5 Turbo           │
│                            │
│  🔮 What's Possible:        │
│  • 🧪 Test Responses       │
│  • 📝 Try Templates        │
│  • 🎛️ Tune Parameters      │
╰──────────────────────────────╯

Let's experiment! 🚀
```
""").send()

async def show_mode_switch_button():
    """Display the mode switch button."""
    # Safely get mode from APP_CONFIG
    mode = APP_CONFIG.get("mode", "default")
    mode_emoji = "🧪" if mode == "test" else "💬"
    switch_to = "chat" if mode == "test" else "test"
    
    await cl.Message(
        content=f"{mode_emoji} Currently in {mode} mode",
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

async def show_mode_transition(to_test_mode: bool):
    """Show transition message when switching modes."""
    if to_test_mode:
        await cl.Message(content="🧪 Entering test lab...").send()
        await show_mode_switch_button()
        await show_test_options()
    else:
        await cl.Message(content="💬 Switching to chat mode...").send()
        await show_mode_switch_button()
        await cl.Message(content="👋 Ready for a chat! What's on your mind? ✨").send()

async def stream_comparison_message(
    test_config: dict,
    message_content: str,
    aspects: List[str],
    default_response: str,
    specialized_response: str,
    prompt_comparison: dict,
    param_comparison: List[dict]
):
    """Stream a formatted comparison message."""
    comparison_msg = cl.Message(content="")
    
    # Add test information
    await comparison_msg.stream_token(f"""# Test: {test_config["label"]}

| Field | Value |
|:------|:-------|
| Description | {test_config["description"]} |
| Input | {message_content} |
| Template Type | {test_config["template"]} |
| Evaluating | {', '.join(aspects)} |
""")
    
    # Add responses
    await comparison_msg.stream_token("\n## Default Response\n")
    await comparison_msg.stream_token(default_response)
    
    await comparison_msg.stream_token("\n\n## Specialized Response\n")
    await comparison_msg.stream_token(specialized_response)
    
    # Add analysis
    await comparison_msg.stream_token("\n\n## Analysis\n")
    await comparison_msg.stream_token("This test evaluates:\n")
    for aspect in aspects:
        await comparison_msg.stream_token(f"- **{aspect}**\n")
    
    # Add prompt comparison
    await comparison_msg.stream_token("\n### Prompt Comparison\n\n")
    await comparison_msg.stream_token("| Mode | System Role | User Template |\n")
    await comparison_msg.stream_token("|:-----|:------------|:--------------|")
    await comparison_msg.stream_token(f"\n| Default | {prompt_comparison['default_system']} | {prompt_comparison['default_user']} |")
    await comparison_msg.stream_token(f"\n| Specialized | {prompt_comparison['specialized_system']} | {prompt_comparison['specialized_user']} |\n\n")
    
    # Add configuration comparison
    await comparison_msg.stream_token("### Configuration Comparison\n\n")
    await comparison_msg.stream_token("| Parameter | Default | Specialized | Change | Impact |\n")
    await comparison_msg.stream_token("|:----------|:---------|:------------|:-------|:--------|\n")
    
    for param in param_comparison:
        await comparison_msg.stream_token(
            f"| {param['name']} | {param['default']:.2f} | {param['specialized']:.2f} | "
            f"{param['change']:+.2f} | {param['impact']} |\n"
        )
    
    await comparison_msg.send() 