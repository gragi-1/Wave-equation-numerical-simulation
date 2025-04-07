import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # Importación necesaria para gráficos 3D
from scipy.sparse import diags
from scipy.linalg import lu_factor, lu_solve

# Parámetros espaciales y temporales
L = 1.0                   # Longitud del dominio
N = 35                    # Número de puntos en cada dimensión
dx = L / (N - 1)
x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
X, Y = np.meshgrid(x, y, indexing='ij')

dt = 1e-3                 # Paso temporal
T = 2                     # Tiempo total de simulación
num_steps = int(T / dt)

hbar = 1.0
m = 1.0

# Potencial: caja infinita 2D (bordes con valor muy alto)
V = np.zeros((N, N))
V[0, :] = V[-1, :] = 1e12
V[:, 0] = V[:, -1] = 1e12
V_flat = V.flatten()

# Función de onda inicial: paquete gaussiano 2D en el centro
x0, y0 = L/2, L/2
sigma = 0.05
k0x = 200 * np.pi
k0y = 200 * np.pi

psi0 = np.exp(-((X - x0)**2 + (Y - y0)**2)/(2*sigma**2)) \
       * np.exp(1j*(k0x*X + k0y*Y))
psi0 = psi0.flatten()
# Normalización
norm = np.sqrt(np.sum(np.abs(psi0)**2) * (dx**2))
psi0 /= norm

# Construir el Laplaciano 1D y a partir de él el 2D (producto de Kronecker)
diagonals = [-2*np.ones(N), np.ones(N-1), np.ones(N-1)]
lap1d = diags(diagonals, [0, -1, 1]).toarray()
I_N = np.eye(N)
lap2d = np.kron(lap1d, I_N) + np.kron(I_N, lap1d)

# Hamiltoniano y matrices para Crank–Nicolson
H = -(hbar**2 / (2*m)) * (lap2d / (dx**2)) + np.diag(V_flat)
I_mat = np.eye(N*N)
A = I_mat + 1j * dt / (2 * hbar) * H
B = I_mat - 1j * dt / (2 * hbar) * H
lu_factors = lu_factor(A)

# Estado inicial
psi = psi0.copy()
t_idx = 0

# Configuración del gráfico 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Z = np.abs(psi.reshape((N, N)))**2
surf = ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_zlim(0, np.max(psi0.reshape((N, N)))**2 * 1.2)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel(r'$|\psi|^2$')
ax.set_title("Evolución 2D: t = 0.0000")

# Función de actualización para la animación
def update(frame):
    global psi, t_idx
    # Realizar un paso temporal usando Crank–Nicolson
    b = B.dot(psi)
    psi = lu_solve(lu_factors, b)

    # Aplicar condiciones de contorno (Dirichlet: psi=0 en los bordes)
    psi_2d = psi.reshape((N, N))
    psi_2d[0, :] = psi_2d[-1, :] = 0.0
    psi_2d[:, 0] = psi_2d[:, -1] = 0.0
    psi = psi_2d.flatten()

    t_idx += 1
    tiempo = t_idx * dt

    # Actualizar la visualización: se borra y vuelve a dibujar la superficie
    ax.clear()
    Z = np.abs(psi.reshape((N, N)))**2
    surf = ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_zlim(0, np.max(psi0.reshape((N, N)))**2 * 1.2)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel(r'$|\psi|^2$')
    ax.set_title(f"Evolución 2D: t = {tiempo:.4f}")
    return surf,

ani = FuncAnimation(fig, update, interval=1, blit=False, cache_frame_data=False)
plt.show()