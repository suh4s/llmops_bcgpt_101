"""
Response Handler Module - Manages LLM API interactions and response processing.
"""

import os
from typing import Dict, List, Any, Tuple, Optional
from openai import AsyncOpenAI
import chainlit as cl
from config import TEST_CONFIG, CHAT_CONFIG
from utils.ui import stream_comparison_message
from utils.formatting import format_template_text

# Constants moved from test_mode.py
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

def create_client() -> AsyncOpenAI:
    """Create a new OpenAI client instance."""
    return AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def adjust_settings_for_aspects(base_settings: Dict[str, Any], aspects: List[str]) -> Dict[str, Any]:
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

async def stream_response(client: Optional[AsyncOpenAI], messages: List[Dict[str, str]], settings: Dict[str, Any]) -> str:
    """Stream a response from the LLM API."""
    # Create a new client if none was provided
    if client is None:
        client = create_client()
        
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        **settings,
        stream=True
    )
    
    response_text = ""
    async for chunk in response:
        if chunk.choices[0].delta.content is not None:
            response_text += chunk.choices[0].delta.content
    
    return response_text

async def generate_comparison(message: cl.Message, client: Optional[AsyncOpenAI], test_config: Dict[str, Any]):
    """Generate and display a comparison of default and specialized responses."""
    # Create a new client if none was provided
    if client is None:
        client = create_client()
        
    # Get templates and settings
    default_settings = TEST_CONFIG["settings"]["default"]
    specialized_settings = adjust_settings_for_aspects(
        TEST_CONFIG["settings"]["specialized"],
        test_config["aspects"]
    )
    
    # Create messages
    default_messages = [
        {"role": "system", "content": CHAT_CONFIG["system_template"]},
        {"role": "user", "content": message.content}
    ]
    
    specialized_messages = [
        {"role": "system", "content": test_config["templates"]["system"]},
        {"role": "user", "content": test_config["templates"]["user"].format(input=message.content)}
    ]
    
    # Get responses
    default_response = await stream_response(client, default_messages, default_settings)
    specialized_response = await stream_response(client, specialized_messages, specialized_settings)
    
    # Prepare prompt comparison
    prompt_comparison = {
        "default_system": format_template_text(CHAT_CONFIG["system_template"]),
        "default_user": format_template_text(message.content),
        "specialized_system": format_template_text(test_config["templates"]["system"]),
        "specialized_user": format_template_text(test_config["templates"]["user"].format(input=message.content))
    }
    
    # Prepare parameter comparison
    param_comparison = []
    for param in ["temperature", "top_p", "max_tokens", "frequency_penalty", "presence_penalty"]:
        default_val = default_settings.get(param, 0)
        specialized_val = specialized_settings.get(param, 0)
        change = specialized_val - default_val
        
        impact = PARAM_IMPACTS[param.replace("_", " ").title()]
        impact_desc = impact["increase"] if change > 0 else impact["decrease"]
        
        param_comparison.append({
            "name": param.replace("_", " ").title(),
            "default": default_val,
            "specialized": specialized_val,
            "change": change,
            "impact": impact_desc
        })
    
    # Stream the comparison message
    await stream_comparison_message(
        test_config=test_config,
        message_content=message.content,
        aspects=test_config["aspects"],
        default_response=default_response,
        specialized_response=specialized_response,
        prompt_comparison=prompt_comparison,
        param_comparison=param_comparison
    ) 