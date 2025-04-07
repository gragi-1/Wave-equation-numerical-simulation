# 🚀 Simulador de la Ecuación de Schrödinger en 1D y 2D

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)

Un simulador interactivo para resolver la ecuación de Schrödinger dependiente del tiempo en sistemas cuánticos confinados, utilizando métodos numéricos avanzados y visualización en tiempo real.

## 🌟 Características Principales

- **Simulaciones en 1D y 2D**:
  - **1D**: Evolución temporal de un paquete de onda en una caja infinita.
  - **2D**: Visualización en mapa de calor (2D) o superficie 3D.
- **Método Numérico**:
  - Algoritmo **Crank-Nicolson** para integración temporal estable.
  - Manejo eficiente con factorización LU de matrices dispersas.
- **Interactividad**:
  - Botones para pausar, reanudar y reiniciar simulaciones.
  - Menú de selección intuitivo con soporte de color.
- **Personalización**:
  - Ajuste de parámetros físicos (longitud, masa, potencial).
  - Configuración de condiciones iniciales (ancho del paquete gaussiano, momento inicial).

## 📦 Requisitos Previos

- **Python 3.8+**
- Bibliotecas necesarias:
  ```bash
  pip install numpy matplotlib scipy colorama
  ```

## 🛠️ Instalación y Ejecución

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/schrodinger-simulator.git
   cd schrodinger-simulator
   ```

2. **Ejecutar el selector**:
   ```bash
   python selector.py
   ```

## 🖥️ Uso del Simulador

### Menú Principal
![Menú Principal](https://via.placeholder.com/600x200.png?text=Selector+Interactivo+del+Simulador)

Seleccione una opción:
- **1**: Simulación 1D (gráfico de densidad de probabilidad).
- **2**: Simulación 2D (visualización en 2D con mapa de calor).
- **3**: Simulación 2D (visualización en 3D con superficie interactiva).
- **q**: Salir del programa.

### Controles en Simulación
- **Pausar/Continuar**: Congela o reanuda la evolución temporal.
- **Resetear**: Reinicia la función de onda a su estado inicial.
- **Visualización en 3D**: Rotación interactiva del gráfico (arrastre con mouse).

## 📂 Estructura del Proyecto

```
schrodinger-simulator/
├── ecuacion1D.py          # Simulación 1D con botones interactivos
├── ecuacion2d.py          # Simulación 2D (mapa de calor)
├── ecuacion2d_3d.py       # Simulación 2D (superficie 3D)
├── selector.py            # Menú de selección interactivo
└── README.md
```

## ⚙️ Parámetros Ajustables

En los archivos `.py`:
- `L`: Longitud de la caja cuántica.
- `N`: Número de puntos en la malla espacial.
- `dt`: Paso temporal (ajustar para estabilidad numérica).
- `sigma`: Ancho del paquete gaussiano inicial.
- `k0`: Momento inicial del paquete de onda.

## 📸 Capturas de Demostración

| Simulación 1D | Simulación 2D (2D) | Simulación 2D (3D) |
|---------------|--------------------|--------------------|
| ![1D](https://via.placeholder.com/300x200.png?text=Evolución+1D) | ![2D](https://via.placeholder.com/300x200.png?text=Mapa+de+Calor+2D) | ![3D](https://via.placeholder.com/300x200.png?text=Superficie+3D) |

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulte el archivo [LICENSE](LICENSE) para más detalles.

---

Desarrollado con ❤️ por [Tu Nombre] - ¡Explora el mundo cuántico! 🎇
```

---

### Notas Adicionales:
1. Reemplace `https://github.com/tu-usuario/schrodinger-simulator` con su enlace real al repositorio.
2. Añada capturas reales de las simulaciones en la sección de demostración.
3. Personalice la sección de licencia según sus necesidades.
4. Incluya un archivo `LICENSE` en el repositorio si es necesario.
