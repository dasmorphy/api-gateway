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
        },
        "RABBITMQ": {
            "HOST": os.getenv('RABBITMQ_HOST'),
            "PORT": os.getenv('RABBIT_PORT'),
            "VHOST": os.getenv('RABBIT_VHOST'),
            "USER": os.getenv('RABBIT_USER'),
            "PASS": os.getenv('RABBITMQ_PASS').strip("'")
        }
    }

def access_mode():
    return access()
