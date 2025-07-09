#!/usr/bin/env python3
"""
Examples demonstrating how to use the easy_llm module functions.

This file shows various ways to interact with LLMs using the utility functions.
Make sure you have the appropriate API keys set in your environment:
- OPENAI_API_KEY for OpenAI models
- GOOGLE_API_KEY for Google models
- MISTRAL_API_KEY for Mistral models
- Azure configuration for Azure models
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent / "src"))

from utils.easy_llm import (
    ask_llm,
    ask_llm_stream,
    interactive_llm_chat,
    load_chat_model
)


def example_1_basic_usage():
    """Example 1: Basic usage of ask_llm function"""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Simple question
    response = ask_llm("What is the capital of France?")
    print(response)
    
    print("\n" + "-" * 40 + "\n")
    
    # Question with custom model
    response = ask_llm(
        "Explain quantum computing in simple terms",
        model_name="google/gemini-2.0-flash-001",
        temperature=0.3
    )
    print(response)


def example_2_streaming_usage():
    """Example 2: Streaming responses"""
    print("=" * 60)
    print("Example 2: Streaming Responses")
    print("=" * 60)
    
    print("Streaming response for: 'What is machine learning?'")
    print("-" * 40)
    
    for chunk in ask_llm_stream("What is machine learning?"):
        print(chunk, end='', flush=True)
    
    print("\n" + "-" * 40 + "\n")
    
    # Custom streaming with different model
    print("Streaming with OpenAI GPT-4:")
    print("-" * 40)
    
    for chunk in ask_llm_stream(
        "Write a short poem about coding",
        model_name="openai/gpt-4o-mini",
        temperature=0.9,
        max_tokens=200
    ):
        print(chunk, end='', flush=True)


def example_3_different_providers():
    """Example 3: Using different LLM providers"""
    print("=" * 60)
    print("Example 3: Different LLM Providers")
    print("=" * 60)
    
    providers = [
        ("Google Gemini", "google/gemini-2.0-flash-001"),
        ("OpenAI GPT-4", "openai/gpt-4o-mini"),
        ("Mistral", "mistral/mistral-large-latest"),
    ]
    
    question = "What are the three laws of robotics?"
    
    for provider_name, model_name in providers:
        print(f"\n{provider_name} ({model_name}):")
        print("-" * 40)
        try:
            response = ask_llm(question, model_name=model_name)
            print(response)
        except Exception as e:
            print(f"❌ Error with {provider_name}: {str(e)}")
            print("(Make sure you have the appropriate API key set)")


def example_4_custom_settings():
    """Example 4: Custom model settings"""
    print("=" * 60)
    print("Example 4: Custom Model Settings")
    print("=" * 60)
    
    # Creative writing with high temperature
    print("Creative writing (high temperature):")
    print("-" * 40)
    response = ask_llm(
        "Write a creative story about a robot learning to paint",
        model_name="openai/gpt-4o-mini",
        temperature=0.9,
        max_tokens=300
    )
    print(response)
    
    print("\n" + "-" * 40 + "\n")
    
    # Factual response with low temperature
    print("Factual response (low temperature):")
    print("-" * 40)
    response = ask_llm(
        "What is the chemical formula for water?",
        model_name="google/gemini-2.0-flash-001",
        temperature=0.1,
        max_tokens=100
    )
    print(response)


def example_5_error_handling():
    """Example 5: Error handling examples"""
    print("=" * 60)
    print("Example 5: Error Handling")
    print("=" * 60)
    
    # Test with invalid model
    print("Testing with invalid model:")
    print("-" * 40)
    try:
        response = ask_llm("Hello", model_name="invalid/model")
        print(response)
    except Exception as e:
        print(f"❌ Expected error: {str(e)}")
    
    print("\n" + "-" * 40 + "\n")
    
    # Test with missing API key (if not set)
    print("Testing with potentially missing API key:")
    print("-" * 40)
    try:
        response = ask_llm("Hello", model_name="openai/gpt-4")
        print(response)
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        print("(This is expected if OPENAI_API_KEY is not set)")


def example_6_model_loading():
    """Example 6: Direct model loading and usage"""
    print("=" * 60)
    print("Example 6: Direct Model Loading")
    print("=" * 60)
    
    try:
        # Load a model directly
        model = load_chat_model("google/gemini-2.0-flash-001", temperature=0.7)
        print(f"✅ Model loaded successfully: {type(model).__name__}")
        
        # Use the model directly
        from langchain_core.messages import HumanMessage
        message = HumanMessage(content="What is the speed of light?")
        response = model.invoke([message])
        
        print(f"\n💡 Response: {response.content}")
        
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")


def example_7_interactive_chat():
    """Example 7: Interactive chat (commented out to avoid blocking)"""
    print("=" * 60)
    print("Example 7: Interactive Chat")
    print("=" * 60)
    
    print("To start an interactive chat, uncomment the following line:")
    print("interactive_llm_chat()")
    
    # Uncomment the line below to start interactive chat
    # interactive_llm_chat(model_name="google/gemini-2.0-flash-001")


def example_8_batch_questions():
    """Example 8: Batch processing multiple questions"""
    print("=" * 60)
    print("Example 8: Batch Processing")
    print("=" * 60)
    
    questions = [
        "What is Python?",
        "What is machine learning?",
        "What is the difference between AI and ML?",
        "What are neural networks?",
    ]
    
    print("Processing multiple questions:")
    print("-" * 40)
    
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question}")
        print("-" * 20)
        try:
            response = ask_llm(question, max_tokens=150)
            print(response)
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def example_9_comparison_demo():
    """Example 9: Compare responses from different models"""
    print("=" * 60)
    print("Example 9: Model Comparison")
    print("=" * 60)
    
    question = "Explain the concept of recursion in programming"
    
    models_to_test = [
        ("Google Gemini", "google/gemini-2.0-flash-001"),
        ("OpenAI GPT-4", "openai/gpt-4o-mini"),
    ]
    
    for model_name, model_id in models_to_test:
        print(f"\n{model_name} Response:")
        print("=" * 40)
        try:
            response = ask_llm(question, model_name=model_id, max_tokens=200)
            print(response)
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def run_all_examples():
    """Run all examples"""
    print("🚀 Running Easy LLM Examples")
    print("Make sure you have appropriate API keys set in your environment!")
    print("=" * 80)
    
    examples = [
        example_1_basic_usage,
        example_2_streaming_usage,
        example_3_different_providers,
        example_4_custom_settings,
        example_5_error_handling,
        example_6_model_loading,
        example_7_interactive_chat,
        example_8_batch_questions,
        example_9_comparison_demo,
    ]
    
    for example in examples:
        try:
            example()
            print("\n" + "=" * 80 + "\n")
        except Exception as e:
            print(f"❌ Error running {example.__name__}: {str(e)}")
            print("\n" + "=" * 80 + "\n")


def run_specific_example(example_number: int):
    """Run a specific example by number"""
    examples = {
        1: example_1_basic_usage,
        2: example_2_streaming_usage,
        3: example_3_different_providers,
        4: example_4_custom_settings,
        5: example_5_error_handling,
        6: example_6_model_loading,
        7: example_7_interactive_chat,
        8: example_8_batch_questions,
        9: example_9_comparison_demo,
    }
    
    if example_number in examples:
        print(f"🚀 Running Example {example_number}")
        print("=" * 80)
        examples[example_number]()
    else:
        print(f"❌ Example {example_number} not found. Available examples: 1-9")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Easy LLM examples")
    parser.add_argument(
        "--example", 
        type=int, 
        help="Run a specific example (1-9). If not specified, runs all examples."
    )
    
    args = parser.parse_args()
    
    if args.example:
        run_specific_example(args.example)
    else:
        run_all_examples() 