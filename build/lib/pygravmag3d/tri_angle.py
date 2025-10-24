
import numpy as np

def tri_angle(A, B, C):
    """
    Compute the solid angle spanned by triangle (A,B,C) in R^3
    as seen from the origin.

    Parameters
    ----------
    A, B, C : array_like, shape (3,)
        Triangle vertices ordered counterclockwise.

    Returns
    -------
    ang : float
        Solid angle in radians.
    """
    A = np.asarray(A, dtype=float).reshape(3)
    B = np.asarray(B, dtype=float).reshape(3)
    C = np.asarray(C, dtype=float).reshape(3)

    An = np.linalg.norm(A)
    Bn = np.linalg.norm(B)
    Cn = np.linalg.norm(C)
    crsBC = np.cross(B, C)
    deter = A[0] * crsBC[0] + A[1] * crsBC[1] + A[2] * crsBC[2]
    dotab = A[0] * B[0] + A[1] * B[1] + A[2] * B[2]
    dotac = A[0] * C[0] + A[1] * C[1] + A[2] * C[2]
    dotbc = B[0] * C[0] + B[1] * C[1] + B[2] * C[2]
    tan2ang = deter / (An * Bn * Cn + dotab * Cn + dotac * Bn + dotbc * An)
    ang = 2.0 * np.arctan(tan2ang)
    return float(ang)
