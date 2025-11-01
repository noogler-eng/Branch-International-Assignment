from flask import Flask
from .config import DevelopmentConfig, StagingConfig, ProductionConfig

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

    # Lazy imports to avoid circular deps during app init
    from .routes.health import bp as health_bp
    from .routes.loans import bp as loans_bp
    from .routes.stats import bp as stats_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(loans_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")

    return app
