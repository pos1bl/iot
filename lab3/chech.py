from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://user:pass@postgres_db:5432/test_db"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        conn.set_client_encoding("utf-8")
        print(conn.encoding)
        result = conn.execute("SELECT version();")
        print(result.fetchone())
except Exception as e:
    print("Error:", e)
