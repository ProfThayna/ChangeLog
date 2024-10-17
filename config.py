from flask_swagger_ui import get_swaggerui_blueprint

# Configuração do Swagger
SWAGGER_URL = '/swagger'  # URL onde o Swagger estará disponível
API_URL = '/static/swagger.json'  # Caminho para o arquivo swagger.json

# Configuração do Blueprint para o Swagger
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "API de Versionamento"}
)