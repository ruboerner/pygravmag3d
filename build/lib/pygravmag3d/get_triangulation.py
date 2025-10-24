import numpy as np
from scipy.spatial import ConvexHull


def get_triangulation(pts):
    """
    Compute the outward-oriented triangular surface mesh of the convex hull of `pts`.

    Parameters
    ----------
    pts : ndarray of shape (n_points, 3)
        Cartesian coordinates of the points defining the body.
    
    Returns
    -------
    faces_oriented : ndarray of shape (n_faces, 3)
        Indices of the hull vertices, oriented so their winding follows the outward normal.
    cor : ndarray of shape (n_points, 3)
        Coordinates of the hull vertices ordered consistently with `faces_oriented`.
    Un : ndarray of shape (n_faces, 3)
        Unit outward normal vector for each triangular face.
    v : float
        Volume enclosed by the convex hull.
    """
    hull = ConvexHull(pts)
    Face = hull.simplices  # shape (F,3), 0-based indexing
    cor = hull.points
    v = hull.volume
    equations = hull.equations  # each row: [a,b,c,d] outward plane

    faces_oriented = Face.copy()
    Un = np.zeros((Face.shape[0], 3))

    for i, tri in enumerate(Face):
        A, B, C = pts[tri]
        n_geom = np.cross(B - A, C - A)
        n_geom /= np.linalg.norm(n_geom)

        # Outward normal from Qhull’s plane
        n_out = equations[i, :3]
        n_out /= np.linalg.norm(n_out)

        # If they point in opposite directions, flip triangle winding
        if np.dot(n_geom, n_out) < 0:
            faces_oriented[i, [1, 2]] = faces_oriented[i, [2, 1]]
            n_geom = -n_geom

        Un[i] = n_geom   # consistent outward unit normal

    return faces_oriented, cor, Un, v