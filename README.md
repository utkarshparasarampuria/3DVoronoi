# 3DVoronoi
Computing the Voronoi diagram for a voxel set with arbitrary seed points. Then coloring the diagram with the min graph coloring alogrithm.

Solution:
Create a python dict to store the existence of each neighbours of each voxel. There can be maximum 26 neighbours, so 1 integer is enough to store this information.
Finally start BFS from each seed points, increasing the level of BFS for each seed one by one. If point is in no set till now, then include it, else don't. (Imagine ink drops dropping in a tub of water at the same time)
