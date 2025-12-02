from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.secret_key = 'clave_secreta'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

    # Registrar Rutas
    # Importamos DENTRO de la función para evitar errores
    from app.controllers.home_controller import home_bp
    app.register_blueprint(home_bp)

    return app