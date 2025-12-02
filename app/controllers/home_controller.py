from flask import Blueprint, render_template, request, current_app
from werkzeug.utils import secure_filename
import os
import shutil
# CORRECCIÓN: El nombre del módulo debe ser exacto (TrafficSignModel con mayúsculas)
from app.models.TrafficSignModel import TrafficSignModel

# Definir el Blueprint indicando la carpeta de vistas correcta
home_bp = Blueprint('home', __name__, template_folder='../views')

# Instanciar el modelo
traffic_model = TrafficSignModel()

def limpiar_uploads():
    """Elimina todas las imágenes en la carpeta uploads"""
    upload_folder = os.path.join(current_app.root_path, 'static/uploads')
    if os.path.exists(upload_folder):
        for filename in os.listdir(upload_folder):
            filepath = os.path.join(upload_folder, filename)
            try:
                if os.path.isfile(filepath):
                    os.remove(filepath)
            except Exception as e:
                print(f"Error al eliminar {filepath}: {e}")

@home_bp.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = None
    img_url = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No se subió ningún archivo")
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('index.html', error="Nombre de archivo vacío")

        if file:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static/uploads')
            
            os.makedirs(upload_folder, exist_ok=True)
            
            # Limpiar imágenes anteriores
            limpiar_uploads()
            
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            # Llamada al modelo
            prediction, confidence = traffic_model.predecir(filepath)
            
            # Ruta relativa para HTML
            img_url = f"static/uploads/{filename}"

    return render_template('index.html', 
                         prediction=prediction, 
                         confidence=confidence, 
                         img_url=img_url)