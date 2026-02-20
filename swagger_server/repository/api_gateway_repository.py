import json
from loguru import logger
from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.resources.databases.redis import RedisClient


class ApiGatewayRepository:
    
    def __init__(self):
        self.redis_client = RedisClient()


    def validate_token(self, token, internal, external):
        try:
            user_id = self.redis_client.client.get(f"token:{token}")

            if not user_id:
                raise CustomAPIException("Usuario no autenticado o expirado", 401)

            return {
                "valid": True,
                "user_id": int(user_id)
            }

        except Exception as exception:
            logger.error('Error: {}', str(exception), internal=internal, external=external)
            raise CustomAPIException("Usuario no autenticado o expirado", 401)