from langchain_openai import AzureChatOpenAI, ChatOpenAI  # Use AzureChatOpenAI for Azure OpenAI
from langchain_core.prompts import PromptTemplate
import os  # For environment variables
def setup_llm():
    """Initialize the OpenAI LLM."""
    return ChatOpenAI(model="gpt-4.1", temperature=0)

def create_prompt_template():
    """Create the prompt template for SQL to Snowflake conversion with table, column, and relation mapping."""
    return PromptTemplate(
        input_variables=["new_schema", "old_query", "table_mapping", "column_mapping", "old_schema"],
        template="""You are an expert SQL developer specializing in Snowflake's SQL dialect. Your task is to convert the provided SQL query, written for an old database schema, to a Snowflake-compatible SQL query based on the provided new Snowflake schema, table mapping, and column mapping. The old query uses table and column names from an old schema, which differs from the new Snowflake schema in structure, including table relationships (e.g., joins, foreign keys, or dependencies). Only use the tables and columns listed in the new schema. If the query references any tables not listed in the new schema or not mapped in the table mapping, return: "The requested table(s) are not listed in the new schema or table mapping."

**Old Schema (Optional)**: If provided, use the old schema to understand the structure and context of the old query, including table relationships (e.g., foreign keys, join conditions, or dependencies). This helps identify the query's intent and handle structural and relational differences between the old and new schemas. If the old schema is not provided, rely on the table and column mappings and the new schema, making reasonable assumptions about relationships based on foreign key constraints and noting them in the explanation.

**Table Mapping**: Use the provided table mapping (JSON format: {{"old_table": "new_table", ...}}) to replace old table names from the old schema with the corresponding new table names in the Snowflake schema. If a table in the old query is not listed in the table mapping or new schema, note this in the explanation and suggest how to handle it (e.g., flag as an error or suggest a similar table based on the old schema's context, if provided).

**Column Mapping**: Use the provided column mapping (JSON format: {{"old_column": "new_column", ...}}) to replace old column names from the old schema with the corresponding new column names in the Snowflake schema. If a column in the old query is not listed in the column mapping or new schema, note this in the explanation and suggest how to handle it (e.g., exclude the column, flag as an error, or suggest a similar column based on the old schema's context, if provided).

**Relation Mapping and Join Conditions**: The old schema’s relationships (e.g., foreign keys, join conditions) may differ significantly from the new schema due to restructuring (e.g., tables split into multiple tables, new intermediate tables, or changed foreign keys). For each join in the old query:
1. Identify the relationship in the old schema (e.g., foreign key or join condition, such as `table1.col1 = table2.col2`).
2. Map this relationship to the new schema by:
   - Analyzing the foreign key constraints in the new schema to determine the correct join path.
   - Identifying all necessary intermediate tables required to link the mapped tables (e.g., if table A joins directly to table B in the old schema, but in the new schema, A connects to B through tables C and D, include joins for A-to-C, C-to-D, and D-to-B).
   - Ensuring join columns exist in the new schema’s tables and align with the foreign key constraints.
3. Avoid assuming direct joins between tables unless explicitly supported by the new schema’s foreign key relationships. For example, do not join two tables directly (e.g., `table1.id = table2.id`) if the new schema requires intermediate tables to establish the relationship.
4. Validate the join path by:
   - Checking that each join condition uses columns that exist in the new schema and are part of the defined foreign key relationships.
   - Ensuring the join path preserves the original query’s logic (e.g., linking the same entities, such as properties to their payments).
   - Confirming that the join path does not introduce incorrect or unrelated data (e.g., joining on columns that are not foreign keys in the new schema).
5. If a join cannot be mapped due to missing tables, columns, or relationships in the new schema, flag it in the explanation, specify why (e.g., "No direct relationship exists between table1 and table2 in the new schema"), and suggest alternatives (e.g., excluding the join, using a different table/column, or querying the user for clarification).
If the old schema is not provided, infer relationships from the new schema’s foreign key constraints and the table/column mappings, explicitly noting any assumptions (e.g., "Assumed table1 joins to table2 via column1 based on new schema’s foreign key constraint") and potential issues in the explanation.

Ensure the converted query:
- Adheres to Snowflake's ANSI-compliant SQL dialect, using `LIMIT` or `OFFSET ... FETCH` for row-limiting, `DATEADD` for date operations, `CONCAT` or `||` for string concatenation, and handling semi-structured data with `VARIANT` types or `GET_PATH` if applicable.
- Accounts for structural and relational differences between the old and new schemas (e.g., data type changes, missing columns, or altered table relationships), using the old schema for context if provided.
- Optimizes for Snowflake where possible, suggesting clustering keys, materialized views, or efficient join strategies if applicable.
- Preserves the original query's logic and results as closely as possible, noting any deviations due to schema or relational differences.
- Includes inline comments in the SQL code to explain each change, including table/column replacements, join adjustments, dialect changes, and any Snowflake-specific optimizations.

**Old Schema (if provided):**
{old_schema}

**New Snowflake Schema:**
{new_schema}

**Table Mapping (old table name -> new table name):**
{table_mapping}

**Column Mapping (old column name -> new column name):**
{column_mapping}

**Original SQL Query (based on old schema):**
{old_query}

**Output Format:**
Return a JSON object with two keys:
- "new_query": The converted Snowflake-compatible SQL query (as a string). If the query references tables not in the new schema or table mapping, return: "The requested table(s) are not listed in the new schema or table mapping".
- "explanation": A detailed step-by-step explanation of the changes made, including:
  - Table and column name replacements based on the mappings.
  - Adjustments for dialect differences (e.g., `FETCH FIRST` to `LIMIT`), schema changes, or relational differences (e.g., data type mismatches, missing columns, or altered join conditions, using the old schema for context if provided).
  - Detailed mapping of each join condition from the old schema to the new schema, including:
    - The original join condition and its purpose (e.g., linking properties to payments).
    - The new join path, including all intermediate tables and foreign key columns used.
    - Validation that the new join path preserves the original query’s logic.
  - Any potential issues (e.g., unmapped tables/columns, unsupported functions, or logic changes due to schema or relational differences).
  - Suggestions for handling unmapped or missing elements (e.g., alternative tables/columns or excluding parts of the query, leveraging the old schema if provided).
  - Optimization recommendations for Snowflake, if applicable (e.g., "Consider clustering on application_id for faster joins" or "Use a materialized view for frequently accessed data").

**Example Output:**
```json
{{
  "new_query": "SELECT new_column1, new_column2 FROM new_table_name LIMIT 10;",
  "explanation": "1. Replaced old_table with new_table_name based on the provided table mapping.\n2. Replaced old_column1 with new_column1 and old_column2 with new_column2 based on the provided column mapping.\n3. Adjusted join condition: In the old schema, old_table joined with another_table on old_column3 = another_table.id. In the new schema, new_table_name connects to new_another_table through intermediate tables new_intermediate_table1 and new_intermediate_table2, per the new schema’s foreign key constraints (e.g., new_table_name.fk1 = new_intermediate_table1.id, new_intermediate_table1.fk2 = new_intermediate_table2.id, new_intermediate_table2.fk3 = new_another_table.id). Validated that this join path links the same entities as the original query (e.g., properties to their payments).\n4. Changed FETCH FIRST to LIMIT: Snowflake prefers LIMIT for row restriction.\n5. Noted that old_column4 was unmapped and excluded, as it does not exist in the new schema; based on the old schema, old_column4 was an INTEGER column, but no equivalent was found.\n6. Noted data type change: old_column1 was VARCHAR in the old schema but is INTEGER in the new schema; no conversion needed for this query.\n7. Potential issue: The join path includes two intermediate tables, which may impact performance; consider clustering on new_intermediate_table1 on fk1 for faster joins.\n8. Optimization: Consider using a materialized view for new_table_name if this query is frequently executed."
}}
```"""
    )