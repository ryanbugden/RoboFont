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
    x_ind = []
    y_ind = []
    # Parse out the x and y values of the selected glyphs
    for p in g.selection:
        x_ind.append(p.x)
        y_ind.append(p.y)
    # Find the width of the selection and height of the selection
    x_diff = max(x_ind) - min(x_ind)
    y_diff = max(y_ind) - min(y_ind)
    # Average each of the lists
    av_x_ind = int(sum(x_ind) / len(x_ind))
    av_y_ind = int(sum(y_ind) / len(y_ind))
    # If the points are closer together horizontally, align x.
    if x_diff < y_diff:
        for p in g.selection:
            p_i = p._get_index()
            p.x = av_x_ind
            # Don't forget off-curves
            for ocp_i in _adjacentPointsThatAreOffCurve(p_i):
                p.contour.points[ocp_i].x = av_x_ind
    # If the points are closer together vertically, align y.
    else:
        for p in g.selection:
            p_i = p._get_index()
            p.y = av_y_ind
            for ocp_i in _adjacentPointsThatAreOffCurve(p_i):
                p.contour.points[ocp_i].y = av_y_ind
    # Immediately reflect the changes in glyph view.
    g.update()
    