# backend.py

import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from concurrent.futures import ThreadPoolExecutor

# Load environment variables from .env
load_dotenv()

# -----------------------------------------------------------------------------
# 1) Database connection for MySQL
# -----------------------------------------------------------------------------
def connect_to_db(db_host: str, db_user: str, db_pass: str, db_name: str, db_port: str) -> SQLDatabase:
    """
    Given MySQL credentials and host info, returns a SQLDatabase instance.
    """
    # percent-encode the password in case it contains special characters
    safe_pass = quote_plus(db_pass)
    uri = f"mysql+pymysql://{db_user}:{safe_pass}@{db_host}:{db_port}/{db_name}"
    return SQLDatabase.from_uri(uri)


# -----------------------------------------------------------------------------
# 2) Create the LangChain SQL Agent (optional; not used for pure text→SQL)
# -----------------------------------------------------------------------------
_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def create_agent(db: SQLDatabase):
    """
    Wraps the SQLDatabase in a LangChain "openai-tools" agent that can
    describe schema, recover from errors, etc.
    """
    return create_sql_agent(llm=_llm, db=db, agent_type="openai-tools", verbose=True)


# -----------------------------------------------------------------------------
# 3) Pure Text → SQL generator
# -----------------------------------------------------------------------------
def generate_sql_text(db: SQLDatabase, question: str) -> str:
    """
    Uses an LLMChain to convert a natural-language question into
    a single, syntactically correct SQL query against `db`.
    Returns the raw SQL string (no markdown or explanation).
    """
    # grab table names to give the model context
    tables = ", ".join(db.get_usable_table_names())

    prompt_template = """
You are an expert SQL generator.  
The database has these tables:

{tables}

Write a single, syntactically correct SQL query to answer this question:

{question}

Return **only** the SQL statement, without any backticks, numbering, or explanation.
"""
    prompt = PromptTemplate.from_template(prompt_template)
    chain = LLMChain(llm=_llm, prompt=prompt)

    sql = chain.run(tables=tables, question=question)
    return sql.strip()


# -----------------------------------------------------------------------------
# 4) (Optional) Run multiple queries in parallel
# -----------------------------------------------------------------------------
def run_parallel_queries(db: SQLDatabase, queries: list[str]) -> list:
    """
    Given a list of raw SQL strings, executes them in parallel
    and returns a list of their results.
    """
    def run_one(q):
        return db.run(q)

    with ThreadPoolExecutor() as exec:
        return list(exec.map(run_one, queries))
