from flask import Flask
from database import db
from config import Config



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from controllers.cliente import cliente_bp
    from controllers.admin import admin_bp

    app.register_blueprint(cliente_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)