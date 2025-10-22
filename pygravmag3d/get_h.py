
import numpy as np
from tri_angle import tri_angle
from get_pqr import get_pqr

G = 6.6732e-11  # gravitational constant used in original MATLAB code

def get_H(Face, cor, Un, M, density):
    """
    Magnetic and gravity anomaly at the origin due to a polyhedral body
    of homogeneous magnetization and density.

    Parameters
    ----------
    Face : (nf, 3) int array
        Triangle indices (1-based in MATLAB; provide 0-based here).
    cor : (nc, 3) float array
        Vertex coordinates (meters).
    Un : (nf, 3) float array
        Unit normals of the triangular faces (outward).
    M : (3,) float array
        Magnetization vector (A/m).
    density : float
        Mass density (kg/m^3).

    Returns
    -------
    Bx, By, Bz, gx, gy, gz : floats
        Magnetic flux density components Bx, By, Bz (in T) and gravitational acceleration
        components gx, gy, gz (in m/s^2) at the origin.
    """
    Face = np.asarray(Face, dtype=int)
    cor = np.asarray(cor, dtype=float)
    Un = np.asarray(Un, dtype=float)
    M = 1e-7 * np.asarray(M, dtype=float).reshape(3)

    Hx = Hy = Hz = 0.0
    gx = gy = gz = 0.0

    # Scale for gravity
    rhof = density * G

    # If Face appears to be 1-based (MATLAB), convert to 0-based
    if Face.min() == 1:
        Face = Face - 1

    nf = Face.shape[0]

    for i in range(nf):
        # Triangle vertices (columns), observation at origin
        idx = Face[i]
        V = cor[idx, :].T  # shape (3,3), columns are P,Q,R

        # Solid angle of the face
        Omega = tri_angle(V[:, 2], V[:, 1], V[:, 0])
        N = Un[i, :]
        # Adjust sign depending on orientation
        di = np.dot(V[:, 0], N)
        if di < 0:
            Omega = -np.sign(di) * Omega

        # Edge integral vector for the triangle
        PQR = get_pqr(V)  # (p, q, r)

        # Face unit normal
        N = Un[i, :].astype(float)
        l, m, n = N

        p, q, r = PQR

        # Field-shape combinations
        hx = l * Omega + n * q - m * r
        hy = m * Omega + l * r - n * p
        hz = n * Omega + m * p - l * q

        # Magnetic contribution (Pd = N · M)
        Pd = float(np.dot(N, M))
        Hx += Pd * hx
        Hy += Pd * hy
        Hz += Pd * hz

        # Gravity contribution: multiply shape by G * density
        di = rhof * di
        gx -= di * hx
        gy -= di * hy
        gz -= di * hz

    return Hx, Hy, Hz, gx, gy, gz
