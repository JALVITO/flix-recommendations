import os

def get_postgres_uri():
    host = os.environ.get("DB_HOST", "postgres")
    port = os.environ.get("DB_PORT", 5433)
    password = os.environ.get("DB_PASS", "abc123")
    user = os.environ.get("DB_USER", "movies")
    db_name = os.environ.get("DB_NAME", "movies")
    uri = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    # print(uri)
    return uri
