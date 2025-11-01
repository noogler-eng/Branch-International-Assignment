from flask import Blueprint, jsonify
from sqlalchemy import text
from app.db import engine

bp = Blueprint("health", __name__)

@bp.route("/health", methods=["GET"])
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return jsonify({"status": "ok", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "database": str(e)}), 500
