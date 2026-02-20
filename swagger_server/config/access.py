import os
from dotenv import load_dotenv

load_dotenv()

def access():
    return {
        "DB": {
            "REDIS": {
                "HOST": os.getenv('REDIS_HOST'),
                "PORT": os.getenv('REDIS_PORT'),
            }
        }
    }

def access_mode():
    return access()
