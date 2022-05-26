import os

def get_postgres_uri():
    user = os.environ.get("DB_USER", "movies")
    password = os.environ.get("DB_PASS", "abc123")
    host = os.environ.get("DB_HOST", "db")
    port = os.environ.get("DB_PORT", 5432)
    db_name = os.environ.get("DB_NAME", "movies")
    uri = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    # print(uri)
    return uri
