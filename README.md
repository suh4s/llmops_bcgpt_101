---
title: Llm App
emoji: 🚀
colorFrom: yellow
colorTo: indigo
sdk: docker
pinned: false
license: openrail
short_description: llmops beyond chatgpt demo app
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# LLM Response Tester 🚀

A Chainlit app for testing different aspects of LLM responses.

## Quick Start

1. **Installation**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`

3. **Running the App**
   ```bash
   chainlit run app.py
   ```

4. **Usage**
   - Switch between chat and test modes using the button
   - In test mode, you can compare different parameter settings
   - In chat mode, you can have a normal conversation with the AI

## Hugging Face Spaces

This app is configured to run on Hugging Face Spaces. The app will be started automatically by the Hugging Face Spaces environment.

## Features

- Test different parameter settings
- Compare responses side by side
- Switch between chat and test modes
- Stream responses in real-time

## Overview

The LLM Response Tester is a tool designed to help you test and compare LLM responses across different scenarios. It features a dual-mode interface:

1. **Chat Mode**: Regular interaction with the AI assistant (Q-bit)
2. **Test Mode**: Specialized testing with parameter optimization

## Project Structure

```
llmops/
├── app.py              # Main application entry point
├── config.py           # Configuration and test settings
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── utils/             # Utility modules
│   ├── ui.py          # UI components and display functions
│   ├── formatting.py  # Text formatting utilities
│   ├── test_handler.py # Test mode coordination
│   └── response_handler.py # LLM API interaction
```

## Test Types

1. **🧩 OOP Concepts**
   - Explains programming concepts clearly
   - Tests: clarity, simplicity, understandability, examples, humor
   - Example: "Explain the concept of inheritance in object-oriented programming."

2. **📝 Quick Summary**
   - Condenses text while keeping key points
   - Tests: conciseness, accuracy, key point retention, clarity
   - Example: Comprehensive text about the Renaissance period

3. **✨ Creative Tales**
   - Generates engaging stories
   - Tests: creativity, structure, engagement, humor, uniqueness
   - Example: "Write a short story about a robot finding friendship in an unexpected place."

4. **🔢 Math Solver**
   - Breaks down math problems step by step
   - Tests: step-by-step explanation, mathematical accuracy, clarity, simplicity
   - Example: "If a store sells apples in packs of 4 and oranges in packs of 3, how many packs of each do I need to buy to get exactly 12 apples and 9 oranges?"

5. **🎭 Style Shift**
   - Rewrites text in different tones
   - Tests: tone accuracy, meaning preservation, professionalism, clarity
   - Example: Converting informal business communication to professional format

## Parameter Optimization

The system automatically adjusts various parameters based on the test aspects:

- **Temperature**: Controls response creativity and randomness
- **Top P**: Manages token selection diversity
- **Max Tokens**: Adjusts response length
- **Frequency Penalty**: Controls vocabulary repetition
- **Presence Penalty**: Manages topic diversity

Each aspect (e.g., creativity, clarity, accuracy) influences these parameters differently to optimize the response for the specific test type.

## Development

### Adding a New Test Type

1. Add the test configuration to `TEST_CONFIG` in `config.py`:
   ```python
   "test_key": {
       "template": "template_name",
       "label": "🔍 Test Label",
       "description": "Test description",
       "aspects": ["aspect1", "aspect2"],
       "example": "Example input",
       "templates": {
           "system": "System prompt",
           "user": "User prompt template with {input}"
       }
   }
   ```

2. Add any new aspects to `ASPECT_PARAMS` in `response_handler.py` if needed.

### Modifying Parameters

Adjust parameter settings in:
- `CHAT_CONFIG["settings"]` for default chat mode
- `TEST_CONFIG["settings"]` for test mode
- `ASPECT_PARAMS` for aspect-specific adjustments

## License

MIT License - See LICENSE file for details
