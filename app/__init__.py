import os
from flask import Flask
from .config import DevelopmentConfig, StagingConfig, ProductionConfig
from .db import Base, engine
from .logger import setup_logger
from prometheus_flask_exporter import PrometheusMetrics


def create_app() -> Flask:
    flask_env = os.getenv("FLASK_ENV", "development")

    if flask_env == "production":
        config_class = ProductionConfig
    elif flask_env == "staging":
        config_class = StagingConfig
    else:
        config_class = DevelopmentConfig

    app = Flask(__name__)
    app.config.from_object(config_class())

    logger = setup_logger()
    logger.info("✅ Flask app initialized")

    # ✅ Ensure DB tables exist before serving or seeding
    with app.app_context():
        print("📦 Creating database tables (if not exist)...")
        Base.metadata.create_all(bind=engine)

    # ✅ Set up Prometheus metrics
    metrics = PrometheusMetrics(app)
    metrics.info("app_info", "Application info", version="1.0.0")

    # Custom metric example (counts requests by route)
    metrics.register_default(
        metrics.counter(
            "by_path_counter",
            "Request count by request paths",
            labels={"path": lambda: request.path}
        )
    )

    # Lazy imports to avoid circular deps during app init
    from .routes.health import bp as health_bp
    from .routes.loans import bp as loans_bp
    from .routes.stats import bp as stats_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(loans_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")

    return app
