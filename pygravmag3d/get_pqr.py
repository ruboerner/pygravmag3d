
import numpy as np

def get_pqr(vertices):
    """
    Compute the contribution of the three edges of triangle PQR
    to the surface integral vector PQR.

    Parameters
    ----------
    vertices : array_like, shape (3, 3)
        Columns are the vertex coordinates of the triangle (P,Q,R),
        oriented counterclockwise with respect to the outward normal.

    Returns
    -------
    pqr : ndarray, shape (3,)
        The vector contribution summed over edges.
    """
    V = np.asarray(vertices, dtype=float).reshape(3, 3)
    pqr = np.zeros(3, dtype=float)
    edge_index = [0, 1, 2, 0]  # MATLAB 1:3:1 -> Python 0,1,2,0
    eps = np.finfo(float).eps

    for t in range(3):
        p1 = V[:, edge_index[t]]
        p2 = V[:, edge_index[t + 1]]
        v = p2 - p1
        L = np.linalg.norm(v)
        b = 2.0 * np.dot(p1, v)
        r1 = np.linalg.norm(p1)
        denom = r1 + b / 2.0 / L
        if abs(denom) < eps:
            I = (1.0 / L) * np.log(abs(L - r1) / r1)
        else:
            I = (1.0 / L) * np.log((np.sqrt(L**2 + b + r1**2) + L + b / 2.0 / L) / denom)
        pqr = pqr + I * v
    return pqr
