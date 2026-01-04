import gradio as gr    
from src.schema_loader import load_mapping, load_old_schema, load_schema, load_tbl_mapping
from src.llm_setup import setup_llm, create_prompt_template
from src.sql_generator import create_sql_chain, generate_sql

def build_app():
    """Build and return the Gradio application."""
    # Load schema
    new_schema = load_schema()
    old_schema = load_old_schema()

    column_mapping=load_mapping()

    table_mapping=load_tbl_mapping()


    # Initialize LLM and prompt
    llm = setup_llm()
    prompt_template = create_prompt_template()

    # Create SQL generation chain
    chain = create_sql_chain(llm, prompt_template)

    # Define Gradio UI
    with gr.Blocks() as demo:
        gr.Markdown("## 🏦 Snow flake SQL Generator")
        gr.Markdown("SQL Server to Snowflake Query Conversion.")

        with gr.Row():
            user_input = gr.Textbox(label="Enter your question", placeholder="e.g. older version of your SQL query...")
        with gr.Row():
            output = gr.Textbox(label="Generated Query", lines=10)

        btn = gr.Button("Generate SQL")
        btn.click(
            fn=lambda question: generate_sql(chain,new_schema, question, column_mapping, table_mapping, old_schema),
            inputs=user_input,
            outputs=output
        )

    return demo