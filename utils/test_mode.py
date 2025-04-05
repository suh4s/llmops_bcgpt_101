"""
Test Mode Module - Handles test and comparison functionality for LLM responses.
"""

import chainlit as cl
from config import TEST_CONFIG, CHAT_CONFIG

# Map aspects to parameter adjustments
ASPECT_PARAMS = {
    # Creativity-related aspects
    "creativity": {"temperature": 0.9, "top_p": 0.9},
    "uniqueness": {"temperature": 0.9, "presence_penalty": 0.6},
    "humor": {"temperature": 0.8, "frequency_penalty": 0.3},
    
    # Accuracy-related aspects
    "accuracy": {"temperature": 0.5, "top_p": 0.8},
    "mathematical accuracy": {"temperature": 0.3, "top_p": 0.9},
    
    # Structure and clarity aspects
    "clarity": {"temperature": 0.6, "presence_penalty": 0.2},
    "step-by-step explanation": {"temperature": 0.4, "frequency_penalty": 0.3},
    "structure": {"temperature": 0.5, "presence_penalty": 0.4},
    
    # Conciseness aspects
    "conciseness": {"max_tokens": 800, "presence_penalty": 0.4},
    "key point retention": {"temperature": 0.5, "presence_penalty": 0.3},
    
    # Style aspects
    "tone accuracy": {"temperature": 0.7, "presence_penalty": 0.4},
    "professionalism": {"temperature": 0.6, "frequency_penalty": 0.2},
    
    # Engagement aspects
    "engagement": {"temperature": 0.8, "presence_penalty": 0.3},
    "use of examples": {"temperature": 0.7, "presence_penalty": 0.4},
    
    # Understanding aspects
    "simplicity": {"temperature": 0.5, "top_p": 0.8},
    "understandability": {"temperature": 0.6, "frequency_penalty": 0.2}
}

# Parameter impact descriptions
PARAM_IMPACTS = {
    "Temperature": {
        "increase": "More creative and diverse responses, but potentially less focused",
        "decrease": "More focused and deterministic responses, but potentially less creative"
    },
    "Top P": {
        "increase": "More diverse token selection, but potentially less precise",
        "decrease": "More focused token selection, but potentially less varied"
    },
    "Max Tokens": {
        "increase": "Allows for longer responses",
        "decrease": "Forces more concise responses"
    },
    "Frequency Penalty": {
        "increase": "Reduces repetition and encourages diverse vocabulary",
        "decrease": "Allows more natural repetition of terms"
    },
    "Presence Penalty": {
        "increase": "Encourages covering new topics and ideas",
        "decrease": "Allows focusing on the same topics"
    }
}

def adjust_settings_for_aspects(base_settings, aspects):
    """Adjust API parameters based on the aspects being tested."""
    settings = base_settings.copy()
    param_counts = {"temperature": 0, "top_p": 0, "max_tokens": 0, "frequency_penalty": 0, "presence_penalty": 0}
    param_sums = param_counts.copy()
    
    for aspect in aspects:
        if aspect in ASPECT_PARAMS:
            for param, value in ASPECT_PARAMS[aspect].items():
                param_sums[param] += value
                param_counts[param] += 1
    
    for param in param_counts:
        if param_counts[param] > 0:
            value = param_sums[param] / param_counts[param]
            settings[param] = int(value) if param == "max_tokens" else value
    
    return settings

def format_template_text(text):
    """Format template text for table display with proper wrapping."""
    text = text.replace("\n", " ")
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= 60:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return "<br>".join(lines)

async def handle_test_message(message: cl.Message, client, test_config):
    """Handle test mode messages by comparing default and specialized responses."""
    # Get templates and settings
    default_settings = TEST_CONFIG["settings"]["default"]
    specialized_settings = adjust_settings_for_aspects(
        TEST_CONFIG["settings"]["specialized"],
        test_config["aspects"]
    )
    
    # Create messages for default mode (using general template)
    default_messages = [
        {"role": "system", "content": CHAT_CONFIG["system_template"]},
        {"role": "user", "content": message.content}
    ]
    
    # Create messages for specialized mode (using test-specific template)
    specialized_messages = [
        {"role": "system", "content": test_config["templates"]["system"]},
        {"role": "user", "content": test_config["templates"]["user"].format(input=message.content)}
    ]
    
    # Get responses
    default_response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=default_messages,
        **default_settings,
        stream=True
    )
    
    specialized_response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=specialized_messages,
        **specialized_settings,
        stream=True
    )
    
    # Create comparison message
    comparison_msg = cl.Message(content="")
    
    # Add test information
    await comparison_msg.stream_token(f"""# Test: {test_config["label"]}

| Field | Value |
|:------|:-------|
| Description | {test_config["description"]} |
| Input | {message.content} |
| Template Type | {test_config["template"]} |
| Evaluating | {', '.join(test_config["aspects"])} |
""")
    
    # Add responses
    await comparison_msg.stream_token("\n## Default Response\n")
    async for chunk in default_response:
        if chunk.choices[0].delta.content is not None:
            await comparison_msg.stream_token(chunk.choices[0].delta.content)
    
    await comparison_msg.stream_token("\n\n## Specialized Response\n")
    async for chunk in specialized_response:
        if chunk.choices[0].delta.content is not None:
            await comparison_msg.stream_token(chunk.choices[0].delta.content)
    
    # Add analysis
    await comparison_msg.stream_token("\n\n## Analysis\n")
    await comparison_msg.stream_token("This test evaluates:\n")
    for aspect in test_config["aspects"]:
        await comparison_msg.stream_token(f"- **{aspect}**\n")
    
    # Add prompt comparison
    await comparison_msg.stream_token("\n### Prompt Comparison\n\n")
    await comparison_msg.stream_token("| Mode | System Role | User Template |\n")
    await comparison_msg.stream_token("|:-----|:------------|:--------------|")
    
    # Format and add rows
    default_system = format_template_text(CHAT_CONFIG["system_template"])
    default_user = format_template_text(message.content)
    specialized_system = format_template_text(test_config["templates"]["system"])
    specialized_user = format_template_text(test_config["templates"]["user"].format(input=message.content))
    
    await comparison_msg.stream_token(f"\n| Default | {default_system} | {default_user} |")
    await comparison_msg.stream_token(f"\n| Specialized | {specialized_system} | {specialized_user} |\n\n")
    
    # Add configuration comparison
    await comparison_msg.stream_token("### Configuration Comparison\n\n")
    await comparison_msg.stream_token("| Parameter | Default | Specialized | Change | Impact |\n")
    await comparison_msg.stream_token("|:----------|:---------|:------------|:-------|:--------|\n")
    
    # Compare parameters
    for param in ["temperature", "top_p", "max_tokens", "frequency_penalty", "presence_penalty"]:
        default_val = default_settings.get(param, 0)
        specialized_val = specialized_settings.get(param, 0)
        change = specialized_val - default_val
        
        impact = PARAM_IMPACTS[param.replace("_", " ").title()]
        impact_desc = impact["increase"] if change > 0 else impact["decrease"]
        
        await comparison_msg.stream_token(
            f"| {param.replace('_', ' ').title()} | {default_val:.2f} | {specialized_val:.2f} | "
            f"{change:+.2f} | {impact_desc} |\n"
        )
    
    await comparison_msg.send() 