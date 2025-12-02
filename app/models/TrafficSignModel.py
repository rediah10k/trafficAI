import os
import random
import time
import numpy as np

# Intentamos importar TensorFlow, pero no es obligatorio para la simulación
try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing import image
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

class TrafficSignModel:
    def __init__(self):
        self.model = None
        
        # Diccionario de clases (GTSRB)
        self.classes = {
            0: 'Límite velocidad (20km/h)', 1: 'Límite velocidad (30km/h)', 
            2: 'Límite velocidad (50km/h)', 3: 'Límite velocidad (60km/h)', 
            4: 'Límite velocidad (70km/h)', 5: 'Límite velocidad (80km/h)', 
            6: 'Fin límite (80km/h)', 7: 'Límite velocidad (100km/h)', 
            8: 'Límite velocidad (120km/h)', 9: 'Prohibido adelantar', 
            10: 'Prohibido adelantar (camiones)', 11: 'Intersección con prioridad', 
            12: 'Calzada con prioridad', 13: 'Ceda el paso', 
            14: 'Stop (Alto)', 15: 'Prohibido vehículos', 
            16: 'Prohibido camiones', 17: 'Prohibido paso', 
            18: 'Peligro general', 19: 'Curva peligrosa a izquierda', 
            20: 'Curva peligrosa a derecha', 21: 'Curvas peligrosas (izq)', 
            22: 'Suelo irregular', 23: 'Pavimento deslizante', 
            24: 'Carretera estrecha (der)', 25: 'Obras en la vía', 
            26: 'Semáforo', 27: 'Peatones', 28: 'Niños cruzando', 
            29: 'Cruce de ciclistas', 30: 'Hielo/Nieve', 
            31: 'Cruce de animales salvajes', 32: 'Fin límites velocidad', 
            33: 'Giro a la derecha obligatorio', 34: 'Giro a la izquierda obligatorio', 
            35: 'Recto obligatorio', 36: 'Recto o derecha obligatorio', 
            37: 'Recto o izquierda obligatorio', 38: 'Paso obligatorio derecha', 
            39: 'Paso obligatorio izquierda', 40: 'Rotonda obligatoria', 
            41: 'Fin prohibición adelantar', 42: 'Fin prohibición adelantar (camiones)'
        }

        # Buscamos el modelo .h5
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base_path, '../static/ai_weights/modelo_trafico.h5')
        
        # LÓGICA DE CARGA SEGURA
        if os.path.exists(self.model_path) and TF_AVAILABLE:
            try:
                print(f"🔄 Cargando modelo desde: {self.model_path}...")
                self.model = load_model(self.model_path)
                print("✅ MODELO CARGADO EXITOSAMENTE")
            except Exception as e:
                print(f"❌ Error al cargar .h5: {e}")
                print("⚠️ Se usará MODO SIMULACIÓN")
        else:
            print(f"ℹ️ No se encontró modelo en: {self.model_path}")
            print("✨ ACTIVANDO MODO SIMULACIÓN (Ideal para pruebas de interfaz)")

    def predecir(self, image_path):
        """
        Retorna: (Etiqueta, Confianza)
        """
        # --- CASO 1: MODO SIMULACIÓN (Si no hay modelo cargado) ---
        if self.model is None:
            # Simula un pequeño tiempo de pensamiento
            time.sleep(0.8)
            
            # Elegir una clase al azar para probar la UI
            dummy_id = random.choice(list(self.classes.keys()))
            label = self.classes[dummy_id] + " (Simulado)"
            
            # Confianza alta aleatoria
            confidence_val = random.uniform(0.85, 0.99)
            confidence_str = f"{confidence_val * 100:.1f}%"
            
            return label, confidence_str

        # --- CASO 2: MODO REAL (Si hay modelo) ---
        try:
   
            img = image.load_img(image_path, target_size=(48, 48))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0

            predictions = self.model.predict(img_array)
            class_id = np.argmax(predictions)
            confidence = np.max(predictions)

            label = self.classes.get(class_id, "Desconocido")
            return label, f"{confidence * 100:.2f}%"

        except Exception as e:
            print(f"Error en predicción real: {e}")
            return "Error de Procesamiento", "0%"