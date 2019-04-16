from treeTkinter import *

Stree = createTree(0,10)
height = Stree.height()
# number of leaves in a full binary tree
nnode = 2 ** height
height += 1

dx = 4 * radius + space
nnode *= dx
p1 = WorldPoint(0.0, 0.0)
p2 = WorldPoint(nnode, nnode)

vdsp = 3 * dx
hdsp = dx

# root position.
getCenter.ct.position = (p2.x * 0.5, p1.y + dx)

xmin = getXmin(Stree.root(), getCenter(), height, hdsp)
xmax = getXmax(Stree.root(), getCenter(), height, hdsp)

p1.position = (xmin - dx, p2.y - vdsp * height)
p2.position = (xmax + dx, p2.y)

mapwv = mapper((0, 0, 1, 1), (0, 0, CANVAS_WIDTH, CANVAS_HEIGHT))
