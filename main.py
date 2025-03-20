from flask import Flask, jsonify, Response
from flask_jwt_extended import JWTManager

from app.api.base_router import router as base_router
from app.core.dependencies import get_mongo_client, get_settings

from app.middleware.response_middleware import after_request


settings = get_settings()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = settings.JWT_REFRESH_TOKEN_EXPIRES

jwt = JWTManager(app)


app_started: bool = False

@app.before_request
async def startup():
    global app_started
    if not app_started:
        mongodb = get_mongo_client()
        await mongodb.init_db()
        app_started = True

@app.teardown_appcontext
async def cleanup(exception=None):
    mongo = get_mongo_client()
    await mongo.disconnect()



app.before_request(after_request)

app.register_blueprint(base_router)

@app.errorhandler(Exception)
def handle_exception(error: Exception) -> Response:
    response_data = {
        "status": 500,
        "success": False,
        "error": {
            "code": 500,
            "message": str(error)
        }
    }
    return jsonify(response_data), 500

@app.route('/health')
def home():
    return jsonify({
        "data": "healthy"
    })