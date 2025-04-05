"""
Configuration settings for the LLM Response Tester application.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_app_config():
    """Get application configuration with fresh environment variables"""
    load_dotenv(override=True)
    return {
        "mode": os.getenv("APP_MODE", "default"),  # 'default' or 'test'
        "auto_test": os.getenv("APP_AUTO_TEST", "false").lower() == "true",
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "model": "gpt-3.5-turbo",
        "default_settings": {
            "temperature": 0.7,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stream": True,
        }
    }

# Application configuration
APP_CONFIG = get_app_config()

# Ensure 'mode' key is always present
if "mode" not in APP_CONFIG:
    APP_CONFIG["mode"] = "default"

# Chat configuration for default mode
CHAT_CONFIG = {
    "system_template": """You are Q-bit, a friendly and knowledgeable AI assistant! 🤖

Your personality traits:
• 🌟 Enthusiastic and engaging in conversations
• 🎯 Precise and thorough in explanations
• 💡 Creative in problem-solving approaches
• 🤝 Empathetic and understanding
• 🎨 Good at making complex topics simple and interesting

Your communication style:
• Use emojis appropriately to make responses more engaging 
• Break down complex information into digestible parts
• Provide examples when helpful
• Stay positive and encouraging
• Be concise yet informative

Remember to:
• 🎯 Keep responses focused and relevant
• 💭 Think step-by-step when solving problems
• 🔍 Ask clarifying questions when needed
• 🌈 Make learning and interaction fun!

Always maintain a helpful and pleasant tone while providing accurate and valuable information! 🚀""",
    
    "settings": {
        "temperature": 0.7,
        "top_p": 1.0,
        "max_tokens": 1000,
    }
}

# Test configuration
TEST_CONFIG = {
    # Test types and their configurations
    "test1": {
        "template": "oop_explanation",
        "label": "🧩 OOP Concepts",
        "description": "Explain programming concepts clearly",
        "aspects": ["clarity", "simplicity", "understandability", "use of examples", "humor"],
        "example": "Explain the concept of inheritance in object-oriented programming.",
        "templates": {
            "system": "You are a programming mentor who explains concepts with clarity and enthusiasm.",
            "user": "{input}"
        }
    },
    "test2": {
        "template": "paragraph_summary",
        "label": "📝 Quick Summary",
        "description": "Condense text while keeping key points",
        "aspects": ["conciseness", "accuracy", "key point retention", "clarity"],
        "example": """The Renaissance was a transformative period in European history, spanning from the 14th to the 17th centuries. It marked a rebirth of classical learning and wisdom after the Middle Ages. The movement began in Florence, Italy, and spread throughout Europe, revolutionizing art, architecture, politics, science and literature. Key figures like Leonardo da Vinci and Michelangelo emerged, exemplifying the period's ideal of the "Renaissance Man" - someone who excelled in multiple disciplines. The invention of the printing press by Johannes Gutenberg around 1440 helped spread Renaissance ideas by making books more accessible to the general public. This period also saw significant developments in scientific thinking, with scholars beginning to question traditional authorities and rely more on empirical observation.""",
        "templates": {
            "system": "You are a skilled summarizer who captures key points concisely.",
            "user": "Please summarize this text: {input}"
        }
    },
    "test3": {
        "template": "imaginative_story",
        "label": "✨ Creative Tales",
        "description": "Generate engaging stories",
        "aspects": ["creativity", "structure", "engagement", "humor", "uniqueness"],
        "example": "Write a short story about a robot finding friendship in an unexpected place.",
        "templates": {
            "system": "You are a creative storyteller who crafts hilarious, quirky, engaging and imaginative tales.",
            "user": "Create a story about: {input}"
        }
    },
    "test4": {
        "template": "math_problem",
        "label": "🔢 Math Solver",
        "description": "Break down math problems step by step",
        "aspects": ["step-by-step explanation", "mathematical accuracy", "clarity", "simplicity"],
        "example": "If a store sells apples in packs of 4 and oranges in packs of 3, how many packs of each do I need to buy to get exactly 12 apples and 9 oranges?",
        "templates": {
            "system": "You are a math tutor who explains solutions step by step with clarity.",
            "user": "Solve this problem: {input}"
        }
    },
    "test5": {
        "template": "tone_rewrite",
        "label": "🎭 Style Shift",
        "description": "Rewrite text in different tones",
        "aspects": ["tone accuracy", "meaning preservation", "professionalism", "clarity"],
        "example": """Hey boss! 😅 Just wanted to give u a heads up that the client meeting from this morning went AMAZING! The client loved our pitch & they're super excited about moving forward!! But they need the final proposal docs asap - like by EOD if possible?? Can u help me prioritize this?? Thx!!""",
        "templates": {
            "system": "You are a writing expert who can adapt text to different tones while preserving meaning.",
            "user": "Rewrite this professionally: {input}"
        }
    },
    
    # Settings for different test modes
    "settings": {
        "default": {
            "temperature": 0.7,
            "top_p": 1.0,
            "max_tokens": 1000,
        },
        "specialized": {
            "temperature": 0.9,
            "top_p": 0.9,
            "max_tokens": 1500,
        }
    },
    
    # Test mode metadata
    "enabled": APP_CONFIG["mode"] == "test",
    "auto_test": APP_CONFIG["auto_test"],
    "log_level": "DEBUG" if APP_CONFIG["mode"] == "test" else "INFO"
} 