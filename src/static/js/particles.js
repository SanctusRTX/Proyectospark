/**
 * Spark Particles Animation
 * Script para añadir partículas animadas a cualquier contenedor
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar partículas en elementos con la clase 'particles-container'
    const containers = document.querySelectorAll('.particles-container');
    containers.forEach(container => {
        createParticles(container);
    });
});

/**
 * Crea partículas flotantes dentro del contenedor especificado
 * @param {HTMLElement} container - El elemento contenedor donde se crearán las partículas
 * @param {Object} options - Opciones de configuración (opcional)
 */
function createParticles(container, options = {}) {
    // Opciones por defecto
    const defaults = {
        count: 20,                // Número de partículas
        minSize: 5,               // Tamaño mínimo
        maxSize: 15,              // Tamaño máximo
        minDuration: 8,           // Duración mínima de la animación
        maxDuration: 20,          // Duración máxima de la animación
        hueMin: 200,              // Tono mínimo (azul)
        hueMax: 230,              // Tono máximo (azul claro)
        satMin: 70,               // Saturación mínima
        satMax: 100,              // Saturación máxima
        lightMin: 50,             // Luminosidad mínima
        lightMax: 70,             // Luminosidad máxima
        opacityMin: 0.3,          // Opacidad mínima
        opacityMax: 0.6           // Opacidad máxima
    };

    // Combinar opciones por defecto con las proporcionadas
    const settings = {...defaults, ...options};
    
    // Asegurar que el contenedor tenga posición relativa para las partículas absolutas
    if (getComputedStyle(container).position === 'static') {
        container.style.position = 'relative';
    }
    
    // Asegurar que el contenedor tenga overflow hidden
    container.style.overflow = 'hidden';
    
    // Crear partículas
    for (let i = 0; i < settings.count; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        // Posición aleatoria
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        
        // Tamaño aleatorio
        const size = Math.random() * (settings.maxSize - settings.minSize) + settings.minSize;
        
        // Duración aleatoria
        const duration = Math.random() * (settings.maxDuration - settings.minDuration) + settings.minDuration;
        
        // Retraso aleatorio
        const delay = Math.random() * 5;
        
        // Color aleatorio entre azul y celeste
        const hue = Math.floor(Math.random() * (settings.hueMax - settings.hueMin)) + settings.hueMin;
        const saturation = Math.floor(Math.random() * (settings.satMax - settings.satMin)) + settings.satMin;
        const lightness = Math.floor(Math.random() * (settings.lightMax - settings.lightMin)) + settings.lightMin;
        const opacity = Math.random() * (settings.opacityMax - settings.opacityMin) + settings.opacityMin;
        
        // Aplicar estilos
        particle.style.cssText = `
            position: absolute;
            left: ${posX}%;
            top: ${posY}%;
            width: ${size}px;
            height: ${size}px;
            background: hsla(${hue}, ${saturation}%, ${lightness}%, ${opacity});
            box-shadow: 0 0 ${size/2}px hsla(${hue}, ${saturation}%, ${lightness}%, 0.5);
            border-radius: 50%;
            pointer-events: none;
            opacity: 0;
            animation: floatParticle ${duration}s ease-in-out ${delay}s infinite;
            z-index: 1;
        `;
        
        container.appendChild(particle);
    }
}

// Añadir el estilo de animación si no existe
if (!document.getElementById('particles-style')) {
    const styleEl = document.createElement('style');
    styleEl.id = 'particles-style';
    styleEl.textContent = `
        @keyframes floatParticle {
            0% {
                transform: translateY(0) translateX(0) rotate(0);
                opacity: 0;
            }
            20% {
                opacity: 0.8;
            }
            50% {
                transform: translateY(-50px) translateX(30px) rotate(180deg);
                opacity: 0.9;
            }
            80% {
                opacity: 0.8;
            }
            100% {
                transform: translateY(-150px) translateX(40px) rotate(360deg);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(styleEl);
} 