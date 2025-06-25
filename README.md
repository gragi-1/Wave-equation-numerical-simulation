# 🚀 Schrödinger Equation Simulator in 1D and 2D

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

An interactive simulator for solving the time-dependent Schrödinger equation in confined quantum systems, using advanced numerical methods and real-time visualization.

## 🌟 Key Features

- **1D and 2D Simulations**:
  - **1D**: Temporal evolution of a wave packet in an infinite box.
  - **2D**: Visualization as a heatmap (2D) or 3D surface.
- **Numerical Method**:
  - **Crank-Nicolson** algorithm for stable time integration.
  - Efficient handling with LU factorization of sparse matrices.
- **Interactivity**:
  - Buttons to pause, resume, and reset simulations.
  - Intuitive color-supported selection menu.
- **Customization**:
  - Adjustable physical parameters (length, mass, potential).
  - Configuration of initial conditions (Gaussian packet width, initial momentum).

## 📦 Prerequisites

- **Python 3.8+**
- Required libraries:
  ```bash
  pip install numpy matplotlib scipy colorama
  ```

## 🛠️ Installation and Execution

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/schrodinger-simulator.git
   cd schrodinger-simulator
   ```

2. **Run the selector**:
   ```bash
   python selector.py
   ```

## 🖥️ Simulator Usage

### Main Menu

Select an option:
- **1**: 1D simulation (probability density plot).
- **2**: 2D simulation (2D heatmap visualization).
- **3**: 2D simulation (interactive 3D surface).
- **q**: Exit the program.

### Simulation Controls
- **Pause/Resume**: Freeze or resume temporal evolution.
- **Reset**: Restore the wave function to its initial state.
- **3D Visualization**: Interactive graph rotation (drag with mouse).

## 📂 Project Structure

```
schrodinger-simulator/
├── ecuacion1D.py          # 1D simulation with interactive buttons
├── ecuacion2d.py          # 2D simulation (heatmap)
├── ecuacion2d_3d.py       # 2D simulation (3D surface)
├── selector.py            # Interactive selection menu
└── README.md
```

## ⚙️ Adjustable Parameters

In the `.py` files:
- `L`: Length of the quantum box.
- `N`: Number of points in the spatial grid.
- `dt`: Time step (adjust for numerical stability).
- `sigma`: Initial Gaussian packet width.
- `k0`: Initial momentum of the wave packet.

## 📸 Demonstration Screenshots

| 1D Simulation | 2D Simulation (2D) | 2D Simulation (3D) |
|---------------|--------------------|--------------------|
| ![1D](https://github.com/gragi-1/Wave-equation-numerical-simulation/blob/main/1D.png) | ![2D](https://github.com/gragi-1/Wave-equation-numerical-simulation/blob/main/2D.png) | ![3D](https://github.com/gragi-1/Wave-equation-numerical-simulation/blob/main/3D.png) |

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
