# Numerical method

This project solves the time-dependent Schrödinger equation for a particle in a one- or
two-dimensional infinite potential well:

$$
i\hbar \frac{\partial \psi}{\partial t} = \hat{H}\psi,
\qquad
\hat{H} = -\frac{\hbar^2}{2m}\nabla^2 + V.
$$

The default examples use dimensionless units, with $\hbar = m = 1$, and a zero potential
inside the box. The implementation also accepts a spatially varying, time-independent
potential through the Python API.

## Spatial discretization

The second derivative is approximated with a centered finite difference:

$$
\frac{\partial^2 \psi}{\partial x^2}\bigg|_j
\approx
\frac{\psi_{j-1} - 2\psi_j + \psi_{j+1}}{\Delta x^2}.
$$

In two dimensions, the discrete Laplacian is assembled as a Kronecker sum of the two 1D
operators. The resulting Hamiltonian is sparse: it has three nonzero diagonals in 1D and
five in 2D.

## Boundary conditions

An infinite well requires

$$
\psi(0, t) = \psi(L, t) = 0.
$$

The solver evolves only the interior grid nodes. Boundary values are inserted as exact
zeros for visualization. This is both more accurate and better conditioned than assigning
an arbitrary large number to the potential at the boundary.

## Time integration

Crank–Nicolson averages the Hamiltonian between two consecutive time levels:

$$
\left(I + \frac{i\Delta t}{2\hbar}H\right)\psi^{n+1}
=
\left(I - \frac{i\Delta t}{2\hbar}H\right)\psi^n.
$$

For a time-independent Hermitian Hamiltonian, this update is unitary up to floating-point
roundoff. It is second-order accurate in time and conserves total probability. The left
matrix is factorized once with sparse LU decomposition and reused for every frame.

## Accuracy and resolution

Crank–Nicolson is unconditionally stable, but stability does not guarantee accuracy. A
useful simulation still requires enough grid points to resolve the shortest wavelength:

$$
\lambda = \frac{2\pi}{|k|}.
$$

As a practical rule, use at least 10–15 grid intervals per wavelength and reduce the time
step until the result no longer changes materially. The automated test suite checks norm
conservation and exact boundary values; it does not replace a convergence study for new
physical scenarios.

## Computational complexity

The sparse representation avoids the quadratic memory cost of a dense Hamiltonian. Setup
is dominated by the one-time sparse LU factorization. Each later step performs one sparse
matrix-vector product and two triangular solves. The surface renderer is usually the
bottleneck in the 3D view, not the solver.

