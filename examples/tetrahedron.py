#!/usr/bin/env python
'''
Create irregular mesh on a regular tetrahedron centered at the origin.
'''
import numpy as np
import time

import voropy
# ==============================================================================
def _main():
    args = _parse_options()

    # circumcircle radius
    r = 5.0
    #max_volume = 1.0 / args.n**3
    max_volume = 8.0

    # boundary points
    points = []
    points.append((0.0, 0.0, r))
    # theta = arccos(-1/3) (tetrahedral angle)
    costheta = -1.0 / 3.0
    sintheta = 2.0 / 3.0 * np.sqrt(2.0)
    # phi = 0.0
    sinphi = 0.0
    cosphi = 1.0
    points.append((r * cosphi * sintheta, r * sinphi * sintheta, r * costheta))
    # phi = np.pi * 2.0 / 3.0
    sinphi = np.sqrt(3.0) / 2.0
    cosphi = -0.5
    points.append((r * cosphi * sintheta, r * sinphi * sintheta, r * costheta))
    # phi = - np.pi * 2.0 / 3.0
    sinphi = -np.sqrt(3.0) / 2.0
    cosphi = -0.5
    points.append((r * cosphi * sintheta, r * sinphi * sintheta, r * costheta))

    # boundary faces
    facets = [ [0,1,2],
               [0,2,3],
               [0,3,1],
               [1,2,3] ]

    # create the mesh
    print 'Create mesh...',
    start = time.time()
    import meshpy.tet
    # Set the geometry and build the mesh.
    info = meshpy.tet.MeshInfo()
    info.set_points( points )
    info.set_facets( facets )
    meshpy_mesh = meshpy.tet.build(info, max_volume = 1.0/args.n**3)
    mesh = voropy.mesh3d(meshpy_mesh.points, meshpy_mesh.elements)
    elapsed = time.time() - start
    print 'done. (%gs)' % elapsed

    num_nodes = len(mesh.node_coords)

    # create values
    print 'Create values...',
    start = time.time()
    import random, cmath
    X = np.empty(num_nodes, dtype = complex)
    for k, node in enumerate(mesh.node_coords):
        #X[k] = cmath.rect( random.random(), 2.0 * pi * random.random() )
        X[k] = complex( 1.0, 0.0 )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed

    # Add magnetic vector potential.
    print 'Create mvp...',
    start = time.time()
    A = np.empty(num_nodes, dtype=np.dtype((float,3)))
    height0 = 0.1
    height1 = 1.1
    radius = 2.0
    import magnetic_vector_potentials
    for k, node in enumerate(mesh.node_coords):
        A[k] = magnetic_vector_potentials.mvp_z( node )
        #A[k] = magnetic_vector_potentials.mvp_magnetic_dot( node, radius, height0, height1 )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed

    mesh.write(args.filename, {'psi': X, 'A': A})

    print '\n%d nodes, %d elements' % (num_nodes, len(mesh.cells))

    return
# ==============================================================================
def _parse_options():
    '''Parse input options.'''
    import argparse

    parser = argparse.ArgumentParser( description = 'Construct tetrahedrization of a cube.' )


    parser.add_argument( 'filename',
                         metavar = 'FILE',
                         type    = str,
                         help    = 'file to be written to'
                       )

    parser.add_argument( '--maxvol', '-m',
                         metavar = 'N',
                         dest='n',
                         nargs='?',
                         type=int,
                         const=1,
                         default=1,
                         help    = 'max volume of a tetrahedron is 1.0/N^3'
                       )


    args = parser.parse_args()

    return args
# ==============================================================================
if __name__ == "__main__":
    _main()
# ==============================================================================
