from swagger_server.repository.api_gateway_repository import ApiGatewayRepository


class ApiGatewayUseCase:

    def __init__(self, api_gateway_repository: ApiGatewayRepository):
        self.api_gateway_repository = api_gateway_repository

    def validate_token(self, headers, internal):
        return self.api_gateway_repository.validate_token(headers.get('Authorization'), internal)