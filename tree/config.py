from pathlib import Path

# TODO : update
BUILD_DIRECTORY = Path.home() / ("build_results")
TAXO_DIRECTORY = BUILD_DIRECTORY / "taxo"
GENOMES_DIRECTORY = BUILD_DIRECTORY / "genomes"

# LMDATA_DIRECTORY = "/var/www/html/data"
LMDATA_DIRECTORY = BUILD_DIRECTORY / "lmdata"

DB_HOST = "localhost"
DB_NAME = "tree"
DB_USER = "lm"
DB_PASSWD = "gvC5b78Ch9nDePjF"

PSYCOPG_CONNECT_URL = (
    f"dbname='{DB_NAME}' user='{DB_USER}' host='{DB_HOST}' password='{DB_PASSWD}'"
)
