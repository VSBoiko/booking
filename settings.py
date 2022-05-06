import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def dump(value):
    print((json.dumps(value, indent=4, sort_keys=True)))

BNOVO_API = "https://api.sandbox.reservationsteps.ru/v1/api"
BNOVO_PUBLIC_API = "https://public-api.reservationsteps.ru/v1/api"

BNOVO_ACCOUNT_ID = str(os.getenv("BNOVO_ACCOUNT_ID"))
BNOVO_USERNAME = str(os.getenv("BNOVO_USERNAME"))
BNOVO_PASSWORD = str(os.getenv("BNOVO_PASSWORD"))
