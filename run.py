from src.config import load_config
from src.app import build_app

if __name__ == "__main__":
    # Load environment variables
    load_config()

    # Build and launch the Gradio app
    app = build_app()
    app.launch()