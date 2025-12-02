from app import create_app

# Crea la aplicación usando la fábrica que definimos en app/__init__.py
app = create_app()

if __name__ == '__main__':
    print("--- 🚦 INICIANDO SERVIDOR TRAFFIC AI ---")
    print(" > Abre tu navegador en: http://127.0.0.1:5000")
    print(" > Presiona CTRL+C en esta terminal para detenerlo.")
    
    # Iniciamos el servidor
    app.run(debug=True, port=5000)