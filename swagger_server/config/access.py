import os
from dotenv import load_dotenv

load_dotenv()

def access():
    return {
        "DB": {
            "REDIS": {
                "HOST": os.getenv('REDIS_HOST'),
                "PORT": os.getenv('REDIS_PORT'),
            },
            "POSTGRESQL": {
                "USER": os.getenv('POSTGRESQL_USER'),
                "PASSWORD": os.getenv('POSTGRESQL_PASSWORD').strip("'"),
                "HOST": os.getenv('POSTGRESQL_HOST'),
                "PORT": os.getenv('POSTGRESQL_PORT'),
                "DB": os.getenv('POSTGRESQL_DB')
            },
        }
    }

def access_mode():
    return access()
