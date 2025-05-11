# SQL Query Agent

A Streamlit-based application that leverages LangChain and OpenAI to convert natural‑language questions into SQL queries, allow editing, and execute them against a MySQL database.

## Features

* **Natural Language to SQL**: Enter any English question, and the app generates a syntactically correct SQL query.
* **Edit Before Execution**: Review and modify the generated SQL query before running it.
* **Execute on MySQL**: Run the final SQL directly on your MySQL database and view the results.
* **Parallel Execution (Optional)**: Run multiple SQL statements concurrently (utility function provided).

## Prerequisites

* Python 3.8+
* MySQL database
* OpenAI API key

## Directory Structure

```
Database_reader/
├── backend.py         # Database connection, SQL‑generation, and helper functions
├── app.py             # Streamlit web UI
├── requirements.txt   # Python dependencies
├── .env.example       # Sample environment variables file
└── README.md          # Project documentation
```

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/Database_reader.git
   cd Database_reader
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

2. **In your browser**:

   * Enter your MySQL credentials (host, port, username, password, database).
   * Click **Connect to Database**.
   * Type a natural‑language question in the text box.
   * Click **Generate SQL Query** to see the LLM‑generated SQL.
   * Optionally edit the SQL in the editor.
   * Click **Run SQL Query** to execute and view results.

## Customization

* **SQL Generation Prompt**: Modify the prompt template in `backend.py` → `generate_sql_text()` to fit your schema or tone.
* **Model Settings**: Change the `model` or `temperature` in the `ChatOpenAI` constructor.
* **Parallel Queries**: Use `run_parallel_queries()` in `backend.py` to execute lists of SQL statements concurrently.

## Troubleshooting

* **ModuleNotFoundError**: Ensure you activated the `venv` and installed requirements.
* **Database Connection**: Verify your MySQL host, port, and credentials. Whitelist your client IP if needed.
* **OpenAI Errors**: Check that `OPENAI_API_KEY` is set and valid.

## License

This project is released under the [MIT License](LICENSE).
