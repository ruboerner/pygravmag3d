# pygravmag3d

3D gravity and magnetic modelling

## Installation

Clone the repository and install in editable mode:

```bash
pip install -e .
```

## Usage

```python
import numpy as np
import pygravmag3d as gm

pts = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]) + [2.0, 2.0, 10.0]

faces, cor, un, v = gm.get_triangulation(pts)

rho = 2670.0                         # kg/m^3, density
T = np.array([15000.0, 0.0, 45000.0]) # magnetic main field in nT
mu0 = 4e-7 * np.pi
kappa = 0.126 # magnetic susceptibility in SI units

M = kappa / mu0 * T # magnetization of body
Bx, By, Bz, gx, gy, gz = gm.get_H(faces, cor, un, M, rho)

print("At origin:")
print("Magnetic field (nT):", Bx, By, Bz)
print("Gravity (m/s^2):    ", gx, gy, gz)
```

For a more complete, runnable demonstration (including triangulation, plotting and comparisons with analytical solutions) see the Jupyter notebook `example_01.ipynb` included in this repository.

