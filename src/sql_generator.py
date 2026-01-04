from langchain_core.prompts import PromptTemplate  # Import if not already present
from langchain_core.output_parsers import StrOutputParser  # For parsing LLM output to string


def create_sql_chain(llm, prompt_template):
    """Create a runnable chain for SQL generation."""
    # Chain the prompt with the LLM and a string output parser
    chain = prompt_template | llm | StrOutputParser()
    return chain

def generate_sql(chain, new_schema, old_query, column_mapping, table_mapping, old_schema):
    """Generate an SQL query based on the user question."""
    # Use .invoke() instead of .run() for runnables
    return chain.invoke({
        "new_schema": new_schema,
        "old_query": old_query,
        "column_mapping": column_mapping,
        "table_mapping": table_mapping,
        "old_schema": old_schema
    })