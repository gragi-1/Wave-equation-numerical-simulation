import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from scipy.sparse import diags
from scipy.linalg import lu_factor, lu_solve

# Parámetros físicos y numéricos
L = 1.0                   # Longitud de la caja
N = 256                   # Número de puntos en el dominio espacial
dx = L / (N - 1)          # Paso espacial
x = np.linspace(0, L, N)  # Dominio espacial

dt = 1e-4                 # Paso temporal
T = 10                    # Tiempo total de simulación
num_steps = int(T / dt)   # Número de pasos de tiempo

# Constantes (usamos unidades en las que ℏ = 1 y m = 1)
hbar = 1.0
m = 1.0

# Potencial: caja infinita
V = np.zeros(N)
V[0] = V[-1] = 1e12  # Se asigna un valor muy alto en las fronteras

# Función de onda inicial: paquete gaussiano
x0 = L / 2            # Centro del paquete
sigma = 0.05          # Ancho del paquete
k0 = 200 * np.pi      # Número de onda
psi0 = np.exp(-(x - x0)**2 / (2 * sigma**2)) * np.exp(1j * k0 * x)
# Normalización
psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dx)

# Construcción del Hamiltoniano con diferencias finitas
diagonal = np.full(N, -2.0)
off_diagonal = np.full(N - 1, 1.0)
laplaciano = diags([off_diagonal, diagonal, off_diagonal], offsets=[-1, 0, 1]).toarray()
H = -(hbar**2 / (2 * m)) * (laplaciano / dx**2) + np.diag(V)

# Construcción de las matrices del método Crank–Nicolson
I = np.eye(N)
A = I + 1j * dt / (2 * hbar) * H  # Matriz del lado izquierdo
B = I - 1j * dt / (2 * hbar) * H  # Matriz del lado derecho

# Factorización LU de A para resolver de forma eficiente en cada paso
lu, piv = lu_factor(A)

# Estado inicial de la simulación
psi = psi0.copy()

# Configuración de la visualización en tiempo real
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(x, np.abs(psi)**2, label=r'$|\psi(x,t)|^2$')
ax.set_xlabel('x')
ax.set_ylabel(r'$|\psi(x,t)|^2$')
ax.set_title('Evolución temporal de la función de onda')
ax.legend()
ax.set_ylim(0, np.max(np.abs(psi0)**2) * 1.2)

# Variables que controlan la pausa y el reseteo
paused = False
reset_requested = False

# Funciones de callback para los botones
def pause_sim(event):
    global paused
    paused = True

def resume_sim(event):
    global paused
    paused = False

def reset_sim(event):
    global reset_requested, paused
    reset_requested = True
    paused = True

# Añadir botones de Pausar, Continuar y Resetear
axpause = plt.axes([0.7, 0.02, 0.1, 0.04])    # Pausar
axresume = plt.axes([0.81, 0.02, 0.1, 0.04])    # Continuar
axreset = plt.axes([0.59, 0.02, 0.1, 0.04])     # Resetear

btn_pause = Button(axpause, 'Pausar')
btn_pause.on_clicked(pause_sim)
btn_resume = Button(axresume, 'Continuar')
btn_resume.on_clicked(resume_sim)
btn_reset = Button(axreset, 'Resetear')
btn_reset.on_clicked(reset_sim)

# Bucle de simulación usando while para permitir reinicio
t_idx = 0
while t_idx < num_steps:
    # Si se ha solicitado un reset, reestablecemos el estado inicial y el contador.
    if reset_requested:
        psi = psi0.copy()
        t_idx = 0
        line.set_ydata(np.abs(psi)**2)
        ax.set_title('Simulación reseteada y en pausa')
        plt.pause(0.001)
        reset_requested = False

    # Actualizar la simulación solo si no está en pausa
    if not paused:
        b = B.dot(psi)
        psi = lu_solve((lu, piv), b)
        
        # Enforce Dirichlet boundary conditions for the infinite potential well
        psi[0] = 0.0
        psi[-1] = 0.0
        
        t_idx += 1
        
        if t_idx % 100 == 0:
            line.set_ydata(np.abs(psi)**2)
            ax.set_title(f'Evolución: t = {t_idx * dt:.4f}')
            plt.pause(0.001)
    else:
        plt.pause(0.1)

plt.ioff()
plt.show()
