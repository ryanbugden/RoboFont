# menuTitle: Align Points
# shortCut: shift+command+f

'''
This script aligns selected points intelligently. 
It will look at the x-coordinate offset and 
the y-coordinate offset and align according to 
whichever one is smaller.

Ryan Bugden
2019.03.09
with thanks to Frank Griesshammer for the idea
'''

def findRange(l):
    # Find the width of the selection and height of the selection independently
    return max(l) - min(l)

def avgList(l):
    # Average the x and y lists independently
    return int(sum(l) / len(l))

def _adjacentPointsThatAreOffCurve(point_index):
    adjacents = [point_index-1, point_index+1]
    l = []
    for pt_i in adjacents:
        if p.contour.points[pt_i].type == 'offcurve':
            l.append(pt_i)
    return l
     
g = CurrentGlyph()

# Only works if there is a point selection
if g.selection:
    with g.undo("Align Points"):
        x_ind = []
        y_ind = []
        # Parse out the x and y values of the selected glyphs
        for p in g.selection:
            x_ind.append(p.x)
            y_ind.append(p.y)
        # If the points are closer together horizontally, align x.
        if findRange(x_ind) < findRange(y_ind):
            for p in g.selection:
                p_i = p._get_index()
                p.x = avgList(x_ind)
                # Don't forget off-curves
                for ocp_i in _adjacentPointsThatAreOffCurve(p_i):
                    p.contour.points[ocp_i].x = avgList(x_ind)
        # If the points are closer together vertically, align y.
        else:
            for p in g.selection:
                p_i = p._get_index()
                p.y = avgList(y_ind)
                for ocp_i in _adjacentPointsThatAreOffCurve(p_i):
                    p.contour.points[ocp_i].y = avgList(y_ind)
        # Immediately reflect the changes in glyph view.
        g.update()
    