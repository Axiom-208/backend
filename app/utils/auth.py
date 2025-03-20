from datetime import datetime

import bcrypt
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from app.core.dependencies import get_settings
from app.schema.session import Session

settings = get_settings()


class AuthenticationHandler:

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())


    @staticmethod
    def generate_tokens(user_id: str):
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        return access_token, refresh_token


    @staticmethod
    async def store_session(user_id: str, refresh_token: str):
        session = Session(user_id=user_id, refresh_token=refresh_token, created_at=datetime.now())
        await session.insert()


    @staticmethod
    async def refresh_access_token():
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            return jsonify({"message": "No refresh token provided"}), 401

        session = await Session.find_one(Session.refresh_token == refresh_token)
        if not session:
            return jsonify({"message": "Invalid refresh token"}), 403

        try:
            decoded = decode_token(refresh_token)
            new_access_token = create_access_token(identity=decoded["sub"])
            return jsonify({"access_token": new_access_token})
        except:
            return jsonify({"message": "Refresh token expired"}), 403


    @staticmethod
    async def logout_user():
        refresh_token = request.cookies.get("refresh_token")

        if refresh_token:
            session = await Session.find_one({"refresh_token": refresh_token})
            if session:
                await session.delete()

        response = jsonify({"message": "Logged out successfully"})
        response.delete_cookie("refresh_token")
        return response

