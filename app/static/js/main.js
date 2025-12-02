document.addEventListener('DOMContentLoaded', function() {
    
    // Elementos del DOM
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const previewImg = document.getElementById('previewImg');
    const uploadContent = document.getElementById('upload-content');
    const uploadForm = document.getElementById('upload-form');
    const predictBtn = document.getElementById('predictBtn');
    const loader = document.getElementById('loader');

    // Solo ejecutar si estamos en la página de subida (no en resultados)
    if (dropArea) {
        
        // --- EVENTOS DRAG & DROP (Visuales) ---
        
        // Prevenir comportamiento por defecto
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Añadir clase 'highlight' al arrastrar dentro
        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
        });

        // Quitar clase 'highlight' al salir o soltar
        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
        });

        // Manejar soltar archivo (Drop)
        dropArea.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                fileInput.files = files; // Asignar archivo al input invisible
                handleFiles(files[0]);
            }
        }

        // --- MANEJO DE SELECCIÓN DE ARCHIVO ---
        
        // Cuando se selecciona mediante clic
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                handleFiles(this.files[0]);
            }
        });

        function handleFiles(file) {
            // Validar que sea imagen
            if (!file.type.startsWith('image/')) {
                alert('Por favor, sube solo imágenes.');
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                previewImg.src = e.target.result;
                uploadContent.style.display = 'none'; // Ocultar texto
                previewContainer.style.display = 'block'; // Mostrar imagen
                
                // Animación suave de entrada
                previewContainer.style.opacity = 0;
                setTimeout(() => {
                    previewContainer.style.opacity = 1;
                    previewContainer.style.transition = 'opacity 0.5s ease';
                }, 10);
            };
            reader.readAsDataURL(file);
        }

        // --- ANIMACIÓN DE CARGA AL ENVIAR ---
        
        if (uploadForm) {
            uploadForm.addEventListener('submit', function() {
                if (fileInput.files.length > 0) {
                    predictBtn.style.display = 'none'; // Ocultar botón
                    loader.style.display = 'block';    // Mostrar spinner
                }
            });
        }
    }
});