# Easy LLM Examples

This directory contains comprehensive examples demonstrating how to use the `easy_llm` utility functions.

## Setup

Before running the examples, make sure you have the appropriate API keys set in your environment:

```bash
# For OpenAI models
export OPENAI_API_KEY="your-openai-api-key"

# For Google models
export GOOGLE_API_KEY="your-google-api-key"

# For Mistral models
export MISTRAL_API_KEY="your-mistral-api-key"

# For Azure models
export AZURE_OPENAI_API_KEY="your-azure-api-key"
export AZURE_OPENAI_ENDPOINT="your-azure-endpoint"
```

## Running Examples

### Run All Examples
```bash
python llm_examples.py
```

### Run Specific Example
```bash
# Run example 1 (Basic Usage)
python llm_examples.py --example 1

# Run example 2 (Streaming)
python llm_examples.py --example 2

# Run example 3 (Different Providers)
python llm_examples.py --example 3
```

## Available Examples

### Example 1: Basic Usage
- Simple question-answer with default settings
- Custom model and temperature settings
- Shows the beautified output format

### Example 2: Streaming Responses
- Real-time streaming of LLM responses
- Custom streaming with different models
- Shows how to handle streaming chunks

### Example 3: Different LLM Providers
- Tests multiple providers (Google, OpenAI, Mistral)
- Shows error handling for missing API keys
- Compares responses across providers

### Example 4: Custom Model Settings
- High temperature for creative responses
- Low temperature for factual responses
- Custom token limits

### Example 5: Error Handling
- Invalid model names
- Missing API keys
- Graceful error handling

### Example 6: Direct Model Loading
- Loading models directly with `load_chat_model`
- Using models with LangChain's native interface
- Custom model configuration

### Example 7: Interactive Chat
- Interactive console chat (commented out)
- Shows how to start an interactive session
- Built-in commands and features

### Example 8: Batch Processing
- Processing multiple questions in sequence
- Error handling for batch operations
- Efficient batch processing

### Example 9: Model Comparison
- Comparing responses from different models
- Side-by-side comparison of capabilities
- Model-specific characteristics

## Quick Start Examples

### Basic Question
```python
from utils.easy_llm import ask_llm

response = ask_llm("What is machine learning?")
print(response)
```

### Streaming Response
```python
from utils.easy_llm import ask_llm_stream

for chunk in ask_llm_stream("Explain quantum computing"):
    print(chunk, end='', flush=True)
```

### Interactive Chat
```python
from utils.easy_llm import interactive_llm_chat

interactive_llm_chat(model_name="google/gemini-2.0-flash-001")
```

### Custom Settings
```python
from utils.easy_llm import ask_llm

response = ask_llm(
    "Write a creative story",
    model_name="openai/gpt-4o-mini",
    temperature=0.9,
    max_tokens=300
)
```

## Supported Models

### OpenAI
- `openai/gpt-4o-mini`
- `openai/gpt-4o`
- `openai/gpt-3.5-turbo`

### Google
- `google/gemini-2.0-flash-001`
- `google/gemini-1.5-flash`
- `google/gemini-1.5-pro`

### Mistral
- `mistral/mistral-large-latest`
- `mistral/mistral-medium-latest`
- `mistral/mistral-small-latest`

### Azure OpenAI
- `azureopenai/gpt-35-turbo`
- `azureopenai/gpt-4`
- `azureopenai/gpt-4o`

## Troubleshooting

### Common Issues

1. **API Key Not Set**
   ```
   ❌ Error: API key not found
   ```
   Solution: Set the appropriate environment variable for your provider.

2. **Invalid Model Name**
   ```
   ❌ Error: Unknown model provider
   ```
   Solution: Use the correct model format: `provider/model-name`

3. **Rate Limiting**
   ```
   ❌ Error: Rate limit exceeded
   ```
   Solution: Wait a moment and try again, or use a different model.

4. **Network Issues**
   ```
   ❌ Error: Connection timeout
   ```
   Solution: Check your internet connection and try again.

### Getting Help

If you encounter issues:

1. Check that your API keys are correctly set
2. Verify you have the required dependencies installed
3. Check the model name format
4. Ensure you have sufficient API credits/quota

## Dependencies

Make sure you have the following packages installed:

```bash
pip install langchain-openai langchain-google-genai langchain-mistralai python-dotenv
```

## License

This example code is provided as-is for educational purposes. 