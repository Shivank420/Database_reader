# app.py
import streamlit as st
from backend import (
    connect_to_db,
    create_agent,
    generate_sql_text,
)
from langchain_community.utilities import SQLDatabase

st.title("SQL Query Agent")

# — DB credentials —
db_host = st.text_input("Enter Database Host")
db_user = st.text_input("Enter Database Username")
db_pass = st.text_input("Enter Database Password", type="password")
db_name = st.text_input("Enter Database Name")
db_port = st.text_input("Enter Database Port", value="3306")

# init session state
if "db" not in st.session_state:
    st.session_state.db = None
if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = None

# Connect button
if st.button("Connect to Database"):
    try:
        db: SQLDatabase = connect_to_db(db_host, db_user, db_pass, db_name, db_port)
        st.session_state.db = db
        st.session_state.agent_executor = create_agent(db)
        st.success(f"Connected to {db_name}")
    except Exception as e:
        st.error(f"Connection error: {e}")

# user’s natural-language question
question = st.text_area("Enter your question:")

# 1) GENERATE → SQL  
if st.button("Generate SQL Query"):
    if not question:
        st.warning("Type a question first")
    elif not st.session_state.db:
        st.error("Connect to the database first")
    else:
        try:
            sql = generate_sql_text(st.session_state.db, question)
            st.session_state["generated_sql"] = sql
            st.subheader("🧾 Generated SQL")
            st.code(sql, language="sql")
        except Exception as e:
            st.error(f"SQL generation failed: {e}")

# 2) EDIT & RUN  
if "generated_sql" in st.session_state:
    st.subheader("Edit the SQL Query")
    edited = st.text_area("SQL Query", st.session_state.generated_sql, height=150)

    if st.button("▶️ Run SQL Query"):
        if not st.session_state.db:
            st.error("Connect to the database first")
        else:
            try:
                # directly execute on the DB
                results = st.session_state.db.run(edited)
                st.subheader("📊 Results")
                st.write(results)
            except Exception as e:
                st.error(f"Query execution error: {e}")
