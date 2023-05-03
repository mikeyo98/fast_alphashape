import numpy as np
from rtree import index
from scipy.spatial import Delaunay

def create_rtree_index(triangles):
    idx = index.Index()
    for i, triangle in enumerate(triangles):
        min_x = min(p[0] for p in triangle)
        min_y = min(p[1] for p in triangle)
        max_x = max(p[0] for p in triangle)
        max_y = max(p[1] for p in triangle)
        idx.insert(i, (min_x, min_y, max_x, max_y))
    return idx



class AlphaShape:
    def __init__(self, points, alpha) -> None:
        self.points = points
        self.tris = self.alpha_shape(1/alpha)        
        self.treeIdx = create_rtree_index(self.tris)

    # https://stackoverflow.com/questions/23073170/calculate-bounding-polygon-of-alpha-shape-from-the-delaunay-triangulation
    def alpha_shape(self, alpha):
        """
        Compute the alpha shape (concave hull) of a set of points.
        :param points: np.array of shape (n,2) points.
        :param alpha: alpha value.
        :param only_outer: boolean value to specify if we keep only the outer border
        or also inner edges.
        :return: set of (i,j) pairs representing edges of the alpha-shape. (i,j) are
        the indices in the points array.
        """
        assert self.points.shape[0] > 3, "Need at least four points"

        tri = Delaunay(self.points)
        tris = []
        # Loop over triangles:
        # ia, ib, ic = indices of corner points of the triangle
        for ia, ib, ic in tri.simplices:
            pa = self.points[ia]
            pb = self.points[ib]
            pc = self.points[ic]
            # Computing radius of triangle circumcircle
            # www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
            a = np.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
            b = np.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
            c = np.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)
            s = (a + b + c) / 2.0
            area = np.sqrt(s * (s - a) * (s - b) * (s - c))
            circum_r = a * b * c / (4.0 * area)
            if circum_r < alpha:                
                tris.append([pa, pb, pc])
        return tris

    def point_in_shape(self, point):
        def point_in_triangle(p, triangle):
            A, B, C = triangle
            v0 = C - A
            v1 = B - A
            v2 = p - A

            dot00 = v0.dot(v0)
            dot01 = v0.dot(v1)
            dot02 = v0.dot(v2)
            dot11 = v1.dot(v1)
            dot12 = v1.dot(v2)

            inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
            u = (dot11 * dot02 - dot01 * dot12) * inv_denom
            v = (dot00 * dot12 - dot01 * dot02) * inv_denom

            return (u >= 0) and (v >= 0) and (u + v < 1)
        nearby_triangle_indices = list(self.treeIdx.intersection(point))
        for index in nearby_triangle_indices:
            if point_in_triangle(point, self.tris[index]):
                return True
        return False
