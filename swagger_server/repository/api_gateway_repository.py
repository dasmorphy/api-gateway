import json
from loguru import logger
from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.models.db.fcm_token_users import FcmTokenUser
from swagger_server.models.db.user_sessions import UserSessions
from sqlalchemy import Integer, and_, cast, exists, func, select, text
from swagger_server.resources.databases.postgresql import PostgreSQLClient
from swagger_server.resources.databases.redis import RedisClient
import jwt


class ApiGatewayRepository:
    
    def __init__(self):
        self.redis_client = RedisClient()
        self.postgres_client = PostgreSQLClient("POSTGRESQL")

        with open("public.pem", "r") as f:
            self.public_key = f.read()


    def validate_token(self, token_session, token_fcm, internal):
        user_id = None

        try:
            jwt.decode(
                token_session,
                self.public_key,
                algorithms=["RS256"]
            )

            user_id = self.redis_client.client.get(f"token:{token_session}")

            if not user_id:
                raise CustomAPIException("Usuario no autenticado o expirado", 401)
            
            ttl_remaining = self.redis_client.client.ttl(f"token:{token_session}")

            if ttl_remaining < 1800:  # menos de 30 min
                ttl = 60 * 60 * 24

                # renovar sesión
                self.redis_client.client.expire(f"token:{token_session}", ttl)

            return {
                "valid": True,
                "user_id": user_id
            }

        except jwt.ExpiredSignatureError:
            self.inactivate_session(token_session, token_fcm, str(user_id))
            raise CustomAPIException("Token expirado", 401)

        except jwt.InvalidTokenError:
            self.inactivate_session(token_session, token_fcm, str(user_id))
            raise CustomAPIException("Token inválido", 401)

        except Exception as exception:
            self.inactivate_session(token_session, token_fcm, str(user_id))
            logger.error('Error: {}', str(exception), internal=internal, external=internal)
            raise CustomAPIException("Usuario no autenticado o expirado", 401)


    def inactivate_session(self, token_session: str, token_fcm: str, user_id: str):
        with self.postgres_client.session_factory() as session:
            try:
                token_session_exist = session.execute(
                    select(UserSessions).where(UserSessions.token_session == token_session)
                ).scalar_one_or_none()

                if not user_id and token_session_exist:
                    user_id = str(token_session_exist.user_id)

                if token_session_exist:
                    session.delete(token_session_exist)

                token_fcm_exist = session.execute(
                    select(FcmTokenUser)
                    .where(
                        FcmTokenUser.user_id == user_id,
                        FcmTokenUser.fcm_token == token_fcm,
                        FcmTokenUser.is_active == True
                    )
                ).scalar_one_or_none()

                if token_fcm_exist:
                    token_fcm_exist.is_active = False


                session.commit()
            except Exception:
                logger.exception("Error desactivando FCM token y token de session")