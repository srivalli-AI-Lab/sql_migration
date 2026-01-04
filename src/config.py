import os
from dotenv import load_dotenv
import getpass

def load_config():
    """Load and set environment variables from .env file or prompt if necessary."""
    # Load .env file
    load_dotenv()

    # Check if OPENAI_API_KEY is set
    if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"]:
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")