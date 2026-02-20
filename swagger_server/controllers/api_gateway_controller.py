from timeit import default_timer
from flask import Response, request, stream_with_context
from flask.views import MethodView
from loguru import logger
import connexion

from swagger_server.exception.custom_error_exception import CustomAPIException
from swagger_server.repository.api_gateway_repository import ApiGatewayRepository
from swagger_server.uses_cases.api_gateway_use_case import ApiGatewayUseCase
from swagger_server.utils.transactions.transaction import generate_internal_transaction_id


class ApiGatewayView(MethodView):
    def __init__(self):
        self.logger = logger
        api_gateway_repository = ApiGatewayRepository()
        self.api_gateway_use_case = ApiGatewayUseCase(api_gateway_repository)

    def get_validate_token_user(self):  # noqa: E501
        function_name = "get_validate_token_user"
        response = {}
        status_code = 500
        try:
            if connexion.request.headers:
                start_time = default_timer()
                internal_transaction_id = str(generate_internal_transaction_id())
                message = f"start request: {function_name}"
                logger.info(message, internal=internal_transaction_id, external=internal_transaction_id)
                result = self.api_gateway_use_case.validate_token(request.headers, internal_transaction_id)
                response["error_code"] = 0
                response["message"] = "Historial de bitacoras obtenido correctamente"
                response["data"] = result
                end_time = default_timer()
                logger.info(f"Fin de la transacción, procesada en : {end_time - start_time} milisegundos",
                            internal=internal_transaction_id, external=internal_transaction_id)
                status_code = 200
        except Exception as ex:
            response, status_code = CustomAPIException.check_exception(ex, function_name, internal_transaction_id)
            
        return response, status_code