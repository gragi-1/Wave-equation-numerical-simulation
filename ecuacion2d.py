import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
from scipy.sparse import diags
from scipy.linalg import lu_factor, lu_solve

# Parámetros físicos y numéricos
L = 1.0                   # Longitud del dominio
N = 32                    # Puntos en cada dimensión
dx = L / (N - 1)
x = np.linspace(0, L, N)
y = np.linspace(0, L, N)

dt = 1e-4                 # Paso temporal
T = 1                     # Tiempo total de simulación
num_steps = int(T / dt)

hbar = 1.0
m = 1.0

# Potencial: caja infinita 2D (bordes muy altos)
V = np.zeros((N, N))
V[0, :] = V[-1, :] = 1e12
V[:, 0] = V[:, -1] = 1e12
V_flat = V.flatten()

# Función de onda inicial: paquete gaussiano 2D
x0, y0 = L/2, L/2
sigma = 0.05
k0x = 200 * np.pi
k0y = 200 * np.pi

X, Y = np.meshgrid(x, y, indexing='ij')
psi0 = np.exp(-((X - x0)**2 + (Y - y0)**2) / (2*sigma**2)) * np.exp(1j*(k0x*X + k0y*Y))
psi0 = psi0.flatten()
# Normalización
norm = np.sqrt(np.sum(np.abs(psi0)**2)*(dx**2))
psi0 = psi0 / norm

# Construir el Laplaciano 1D y luego 2D (Kronecker)
diagonals = [-2*np.ones(N), np.ones(N-1), np.ones(N-1)]
lap1d = diags(diagonals, [0, -1, 1]).toarray()
I_N = np.eye(N)
lap2d = np.kron(lap1d, I_N) + np.kron(I_N, lap1d)

# Hamiltoniano y método Crank–Nicolson
H = -(hbar**2 / (2*m)) * (lap2d / (dx**2)) + np.diag(V_flat)
I_mat = np.eye(N*N)
A = I_mat + 1j * dt / (2 * hbar) * H
B = I_mat - 1j * dt / (2 * hbar) * H
lu_factors = lu_factor(A)

# Estado inicial
psi = psi0.copy()

# Variables globales de control
paused = False
reset_requested = False
t_idx = 0

# Configuración de la visualización
fig, ax = plt.subplots()
im = ax.imshow(np.abs(psi.reshape((N, N)))**2, extent=[0, L, 0, L],
               origin='lower', cmap='viridis')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title("Evolución 2D: t = 0.0000")
plt.colorbar(im, ax=ax)

# Funciones de callback
def pause_sim(event):
    global paused
    paused = True

def resume_sim(event):
    global paused
    paused = False

def reset_sim(event):
    global reset_requested, paused, psi, t_idx
    reset_requested = True
    paused = True

# Añadir botones
axpause = plt.axes([0.7, 0.02, 0.1, 0.04])
axresume = plt.axes([0.81, 0.02, 0.1, 0.04])
axreset = plt.axes([0.59, 0.02, 0.1, 0.04])
Button(axpause, 'Pausar').on_clicked(pause_sim)
Button(axresume, 'Continuar').on_clicked(resume_sim)
Button(axreset, 'Resetear').on_clicked(reset_sim)

# Función de actualización para FuncAnimation (sin blit)
def update(frame):
    global psi, t_idx, reset_requested
    if reset_requested:
        psi = psi0.copy()
        t_idx = 0
        reset_requested = False
        ax.set_title("Simulación reseteada y en pausa")
    else:
        if not paused:
            b = B.dot(psi)
            psi = lu_solve(lu_factors, b)
            # Condiciones de contorno de Dirichlet
            psi_2d = psi.reshape((N, N))
            psi_2d[0, :] = 0.0
            psi_2d[-1, :] = 0.0
            psi_2d[:, 0] = 0.0
            psi_2d[:, -1] = 0.0
            psi = psi_2d.flatten()
            t_idx += 1
            if t_idx % 100 == 0:
                ax.set_title(f"Evolución 2D: t = {t_idx*dt:.4f}")
    im.set_data(np.abs(psi.reshape((N, N)))**2)
    return [im]

ani = FuncAnimation(fig, update, interval=1, blit=False, cache_frame_data=False)

plt.show()