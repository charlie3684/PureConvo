# PureConvo

**PureConvo** is a minimalist and efficient Python-based AI chat application. Designed for simplicity and ease of use, it enables users to interact with AI models locally or remotely, with options to configure memory, load a static prompt, and log conversations. Whether you're looking for a lightweight AI companion or a customizable chatbot for experiments, PureConvo delivers a seamless and straightforward experience.

---

## Features

- **Local or Remote Models**:
  - Use `.gguf` models stored locally or download remote models directly to the cache.

- **Customizable Memory**:
  - Retain context between interactions or choose a memory-less one-off chat.

- **Static Prompt Loading**:
  - Personalize the chatbot's behavior by providing instructions in a `ai.prompt.txt` file.

- **Session Logging**:
  - Log user-AI interactions in timestamped files for later reference.

---

## Installation

### Prerequisites
1. Python 3.x
2. Required dependencies:
   ```bash
   pip install -r requirements.txt```

## Setup
```git clone https://github.com/charlie3684/PureConvo.git
cd PureConvo```

Optional:
Place any local .gguf models in the same directory (optional).
Create a ai.prompt.txt file (optional) to define a static prompt for the AI.

## Usage
```python3 ai.py```

## Workflow
1. Select a Model: Choose from detected local models or enter the option to download a remote model.
2. Configure Memory: Set the token limit for context retention or disable memory entirely.
3. Static Prompt: Option to load a static prompt from ai.prompt.txt if available.
4. Enable Logging: Option to save interactions to a file for future reference.

## Commands

```!bye: Exit the chat session.
!reset: Restart the session to load a new model or reset memory.```



## Examples

### Example 1```
Welcome to PureConvo! Type '!bye' to exit or '!reset' to select a new model.

You: Hello!
AI: Hello! How can I assist you today?

You: Who is the President of the United States?
AI: The current President of the United States is Joe Biden (as of 2024).

You: !bye
Goodbye!```


## Example 2
With ai.prompt.txt Content: 
```You are a Shakespearean assistant. Respond with poetic verse.```

Session:
```Do you want to load the static prompt from 'ai.prompt.txt'? (Y/N) [Press Enter for No]: Y

Welcome to PureConvo! Type '!bye' to exit or '!reset' to select a new model.

You: Hello!
AI: Greetings, kind soul, on this fair day!
       How may I serve thee in thine own way?

You: What’s the weather like?
AI: Alas, I cannot see beyond these halls,
       Yet weather's whim forever calls.
```

## Example 3
```Enter your choice for max tokens (default: 512): 8675309
[DEBUG] Asking the model directly...

AI: 
Jenny, I got your number,
I need to make you mine!
CHORUS: 867-5309! 867-5309!```


## Contributing
Contributions are welcome! Feel free to fork this repository, create a branch, and submit a pull request with improvements or new features.


# Author
charlie3684 / GPT
