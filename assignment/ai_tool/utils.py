import re

def clean_sql(sql_text):
    sql_text = sql_text.strip()

    # Remove markdown blocks like ```sql ```
    sql_text = re.sub(r"```sql|```", "", sql_text)

    # Extract only SELECT query
    match = re.search(r"(SELECT .*;?)", sql_text, re.IGNORECASE | re.DOTALL)

    if match:
        return match.group(1).strip()

    return sql_text

def parse_llm_output(text):
    sql = ""
    explanation = ""

    try:
        if "SQL:" in text:
            parts = text.split("SQL:")[1]

            if "EXPLANATION:" in parts:
                sql_part, explanation = parts.split("EXPLANATION:")
                sql = sql_part.strip()
                explanation = explanation.strip()
            else:
                sql = parts.strip()
        else:
            sql = text.strip()

    except:
        pass

    return sql, explanation