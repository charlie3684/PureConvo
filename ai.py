import os
import logging
import time
from ctransformers import AutoModelForCausalLM

# Suppress verbose logging from the library
logging.getLogger("ctransformers").setLevel(logging.ERROR)

# Configuration for the model
config = {
    "max_new_tokens": 256,
    "temperature": 0.7,
    "top_k": 50,
    "repetition_penalty": 1.1
}

# Function to scan for local GGUF models
def get_local_models():
    return [file for file in os.listdir() if file.endswith(".gguf")]

# Function to load the selected model
def load_model(model_name, is_local=True):
    if is_local:
        print(f"Loading local model: {model_name}")
        return AutoModelForCausalLM.from_pretrained(model_name, model_type="llama", **config)
    else:
        print(f"Downloading and loading remote model: {model_name}")
        model = AutoModelForCausalLM.from_pretrained(model_name, model_type="llama", **config)
        cache_dir = os.path.expanduser("~/.cache/ctransformers/")
        print(f"[INFO] Remote model downloaded and stored in: {cache_dir}")
        return model

# Tokenize and truncate text
def tokenize_and_truncate(model, text, max_tokens):
    tokens = model.tokenize(text)
    if len(tokens) > max_tokens:
        tokens = tokens[-max_tokens:]
    return tokens

# Convert tokens back to text
def detokenize(model, tokens):
    return model.detokenize(tokens)

# Adjust the prompt dynamically
def adjust_prompt(static_prompt, memory, user_input):
    combined_prompt = f"{static_prompt}\n" if static_prompt else ""
    combined_prompt += f"Previous conversation:\n{memory}\nUser: {user_input}\nAssistant:" if memory else f"User: {user_input}\nAssistant:"
    return combined_prompt

# Proactive memory trimming
def proactively_trim_memory(model, memory, user_input, max_tokens):
    combined = f"Previous conversation:\n{memory}\nUser: {user_input}\nAssistant:"
    while len(model.tokenize(combined)) > max_tokens:
        memory = "\n".join(memory.split("\n")[2:])  # Trim oldest exchanges
        if not memory:
            print("[WARNING] Memory fully cleared due to context overflow.")
            break
        combined = f"Previous conversation:\n{memory}\nUser: {user_input}\nAssistant:"
    return memory

# Load static prompt from file
def load_static_prompt(file_name="ai.prompt.txt"):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read().strip()
    else:
        print(f"[WARNING] Static prompt file '{file_name}' not found.")
        return ""

# Configure memory settings with special options
def configure_memory():
    print("\nConfigure Maximum Context Length (Memory Size):")
    print("Options:")
    print("- Enter `0` for no memory (1:1 question-answering only).")
    print("- **Default**: 512 tokens (suitable for most models and hardware) [Press Enter to choose this]")
    print("- Better: 768 tokens (requires more memory but gives longer conversation context)")
    print("- Best: 1024 tokens (ideal for high-end hardware or very large models)")

    while True:
        user_input = input("Enter your choice for max tokens (default: 512): ").strip()
        if user_input == "0":
            print("No memory will be used. All questions will be treated independently.")
            return 0
        elif user_input == "8675309":
            return "8675309"
        elif not user_input:
            print("Using the default context length of 512 tokens.")
            return 512
        elif user_input.isdigit() and int(user_input) > 0:
            print(f"Using a custom context length of {user_input} tokens.")
            return int(user_input)
        else:
            print("Invalid input. Please enter a positive number, 0, or '8675309'.")

# Generate a log file name
def generate_log_filename(model_name):
    timestamp = int(time.time())
    model_abbr = "".join(word[0] for word in model_name.split("_")).upper()[:5]
    return f"ai.{model_abbr}.{timestamp}.log"

# Main chat loop
def chat():
    while True:
        print("---------------")

        # List available local models
        local_models = get_local_models()
        if local_models:
            print("Available local models:")
            for idx, model_name in enumerate(local_models, start=1):
                print(f"{idx}. {model_name}")
            print(f"{len(local_models) + 1}. Enter a remote model (e.g., 'TheBloke/orca_mini_v2_7B-GGML')")
        else:
            print("No local models found. You'll need to specify a remote model.")
            local_models = []

        # Model selection
        choice = input(f"Select a model (1-{len(local_models) + 1}): ")

        if choice.isdigit() and 1 <= int(choice) <= len(local_models):
            selected_model = local_models[int(choice) - 1]
            is_local = True
        elif choice == str(len(local_models) + 1) or not local_models:
            selected_model = input("Enter the remote model name: ").strip()
            is_local = False
        else:
            print("Invalid choice!")
            continue

        # Load the model
        model = load_model(selected_model, is_local=is_local)

        # Ask user to configure memory
        max_context_length = configure_memory()

        # Easter egg for "8675309"
        if max_context_length == "8675309":
            prompt = "Tell me the lyrics to the song Jenny 8675309, just give me the first verse and the chorus. But the chorus alone should be in ALL CAPS."
            print("[DEBUG] Asking the model directly...")
            response = model(prompt)
            print(f"\nAssistant: {response}")
            print("Goodbye!")
            return

        # Ask to use static prompt
        static_prompt = ""
        use_static = input("Do you want to load the static prompt from 'ai.prompt.txt'? (Y/N) [Press Enter for No]: ").strip().lower()
        if use_static == "y":
            static_prompt = load_static_prompt()

        # Ask if user wants to enable logging
        enable_logging = input("Do you want to enable logging for this session? (Y/N) [Press Enter for No]: ").strip().lower()
        log_file = None
        if enable_logging == "y":
            log_file = generate_log_filename(selected_model)
            print(f"[INFO] Logging enabled. Session log will be saved to '{log_file}'.")

        # Initialize memory if enabled
        memory = static_prompt if max_context_length != 0 else None

        # Print welcome message after model selection and memory setup
        print("")
        print("-------------------------------------")
        print("Welcome to the AI chat! Type '!bye' to exit or '!reset' to select a new model.")

        while True:
            try:
                # User input
                user_input = input("\nYou: ")
                if user_input.strip().lower() == "!bye":
                    print("Goodbye!")
                    return
                elif user_input.strip().lower() == "!reset":
                    print("[INFO] Resetting the session...")
                    break  # Breaks inner loop and reinitializes the script

                # Proactively trim memory if enabled
                if memory is not None:
                    memory = proactively_trim_memory(model, memory, user_input, max_context_length)

                # Generate prompt
                prompt = adjust_prompt(static_prompt, memory, user_input)

                # DEBUG: Check token count before passing to model
                token_count = len(model.tokenize(prompt))
                print(f"[DEBUG] Token count: {token_count}/{max_context_length if max_context_length else 'N/A'}")

                # Suppress token limit verbose errors
                try:
                    response = model(prompt)
                except Exception as e:
                    if "exceeded maximum context length" in str(e):
                        print("[WARNING] Adjusting memory for token overflow...")
                        memory = proactively_trim_memory(model, memory, user_input, max_context_length)
                        response = model(prompt)
                    else:
                        raise e

                # Update memory if enabled
                if memory is not None:
                    memory += f"User: {user_input}\nAI: {response}\n"

                # Log interaction if logging is enabled
                if log_file:
                    with open(log_file, "a", encoding="utf-8") as log:
                        log.write(f"USER: {user_input}\nAI: {response}\n")

                # Display response
                print(f"\nAI: {response}")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                return
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    chat()

