# simple_alphashape
 Alphashape, but minimal implementation, fast checking if point is inside the shape
 
 Note: 
  - alpha value takes the reciprocal, just to agree with the alphashape lib from pip
  - this api only has 'point_in_shape' method
  - the alphashape may contain a hole inside
 
 Tested on a shape with ~20000 points, ~26000 triangles. Took me less than 1 min to create a 843x1218 mask. (updated)
 
 Reference: 
 https://stackoverflow.com/questions/23073170/calculate-bounding-polygon-of-alpha-shape-from-the-delaunay-triangulation
