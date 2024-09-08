from openai import OpenAI, OpenAIError, RateLimitError, APIError, Timeout
import os
from dotenv import load_dotenv

# Function to save the API key to a .env file
def save_api_key_to_env(api_key, key_name="OPENAI_API_KEY"):
    if os.path.exists(".env"):
        os.remove(".env")  # Remove existing .env file if it exists
    with open(".env", "w") as env_file:
        env_file.write(f"{key_name}={api_key}\n")
    print(".env file created with the API key.")

def get_openai_api_key():
    # Check if API key is present in environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Prompt the user to enter the API key if not found
        manual_api_key = input("Enter your OpenAI API key: ")
        save_api_key_to_env(manual_api_key)
        # Reload the environment with the new API key
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
    return api_key

# Load environment variables
load_dotenv()

# Get the API key
api_key = get_openai_api_key()

# Ensure the API key is loaded
try:
    client = OpenAI(api_key=api_key)
    print("OpenAI client initialized successfully.")
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    exit(1)

# List to store conversation history
conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]

def gpt_response(user_input):
    print("Generating response...\n")
    """
    Generate a response from GPT-4 based on user input and conversation history.
    """
    try:
        # Add the user input to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Send the conversation history to GPT-4
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history
        )

        # Extract the assistant's reply
        assistant_reply = response.choices[0].message.content

        # Add the assistant's reply to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    except RateLimitError:
        return "Error: Rate limit exceeded. Try again later."
    except Timeout:
        return "Error: Request timed out. Try again."
    except APIError as e:
        return f"Error: OpenAI API error: {e}"
    except OpenAIError as e:
        return f"Error: Unable to communicate with OpenAI API: {e}"

def run_chatbot():
    print("\nWelcome to the GPT-4 Command Line Chatbot!\n")
    print("Type 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        response = gpt_response(user_input)
        print(f"GPT-4: {response}\n")

if __name__ == "__main__":
    run_chatbot()
