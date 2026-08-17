import json
from loguru import logger
from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.resources.databases.redis import RedisClient
import jwt

from swagger_server.service.rabbitMQ import RabbitMQClient


class ApiGatewayRepository:
    
    def __init__(self):
        self.redis_client = RedisClient()
        self.rabbitMQ = RabbitMQClient()
        with open("public.pem", "r") as f:
            self.public_key = f.read()


    def validate_token(self, token, channel, internal):
        data_queue = {
            "channel": channel,
            "data": {
                "project_id": 1,
                "token": token,
            },
            "externalTransactionId": internal
        }
        try:
            jwt.decode(
                token,
                self.public_key,
                algorithms=["RS256"]
            )

            user_id = self.redis_client.client.get(f"token:{token}")

            if not user_id:
                # El JWT era válido, pero la sesión ya no existe en Redis.
                # Mandamos al micro de logout para que haga limpieza.
                self.send_event(data_queue, internal)
                raise CustomAPIException("Usuario no autenticado o expirado", 401)
            
            ttl_remaining = self.redis_client.client.ttl(f"token:{token}")

            if ttl_remaining < 1800:  # menos de 30 min
                ttl = 60 * 60 * 24

                # renovar sesión
                self.redis_client.client.expire(f"token:{token}", ttl)

            return {
                "valid": True,
                "user_id": user_id
            }

        except jwt.ExpiredSignatureError:
            self.send_event(data_queue, internal)
            raise CustomAPIException("Token expirado", 401)

        except jwt.InvalidTokenError:
            raise CustomAPIException("Token inválido", 401)

        except CustomAPIException:
            raise

        except Exception as exception:
            logger.error('Error: {}', str(exception), internal=internal, external=internal)
            raise CustomAPIException("Usuario no autenticado o expirado", 401)


    def send_event(self, data_queue, internal):
        try:
            self.rabbitMQ.send_event(
                routing_key="zentinel.logout.session",
                body=data_queue
            )

        except Exception as exception:
            logger.error("No se pudo enviar evento de logout a RabbitMQ: {}", str(exception), internal=internal, external=internal)