# menuTitle: Align Points
# shortCut: shift+command+f

from fontTools.misc.fixedTools import otRound
import math

'''
This script aligns selected points intelligently. 
It will look at the x-coordinate offset and 
the y-coordinate offset and align according to 
whichever one is smaller. It will also make 
an educated guess as to which direction you'd 
like to align it.

Requires Robofont 3.2+

Ryan Bugden
2019.03.09
2023.04.20 - Make it smarter
with thanks to Frank Griesshammer for the idea
'''



def avg_list(l):
    # Average the x and y lists independently
    return int(sum(l) / len(l))
    

g = CurrentGlyph()
f = g.font

if g.selectedPoints:
    x_ind = [p.x for p in g.selectedPoints]
    y_ind = [p.y for p in g.selectedPoints]
            
    max_x = max(x_ind)
    mid_x = avg_list(x_ind)
    min_x = min(x_ind)

    max_y = max(y_ind)
    mid_y = avg_list(y_ind)
    min_y = min(y_ind)
    
    
def get_adj_pts_that_are_offcurve(point_index):
    adjacents = [point_index-1, point_index+1]
    l = []
    for pt_i in adjacents:
        # Will avoid errors with first/last point indexes
        try: 
            p.contour._getPoint(pt_i)
        except IndexError:
            continue
        if p.contour.points[pt_i].type == 'offcurve':
            l.append(pt_i)
    return l
    
    
def get_x_align_vert(x, y):
    italic = 0
    if f.info.italicAngle:
        italic = f.info.italicAngle
        
    y_off = otRound(y - mid_y)  # Vertical offset
    x_off = otRound(math.tan(math.radians(-italic)) * y_off)  # x-offset for if you have an italic angle
    x_align = mid_x + x_off

    return x_align
    

def get_x_align_horiz(x, y):
    italic = 0
    if f.info.italicAngle:
        italic = f.info.italicAngle
        
    y_off = otRound(mid_y - y)  # Vertical offset
    x_off = otRound(math.tan(math.radians(-italic)) * y_off)  # x-offset for if you have an italic angle
    x_align = x + x_off

    return x_align
    
    
def check_which_alignment():
    # Find the width of the selection and height of the selection independently
    
    x_range = max_x - get_x_align_vert(max_x, max_y)
    y_range = max_y - mid_y
    
    if x_range > y_range:
        return 'horizontal'
    else:
        return 'vertical'
    
debug = True

# Only works if there is a point selection
if g.selectedPoints:
    
    with g.undo("Align Points"):
        
        # Threshold to determine whether to move off-curves drastically or not.
        ocp_dist_threshold = 1
            
        
        # If the points are closer together horizontally, align vertically.
        if check_which_alignment() == 'vertical':
            for p in g.selectedPoints: 
                p_i = p._get_index()
                
                x_align = get_x_align_vert(p.x, p.y)
                    
                x_delta = x_align - p.x
                p.x = x_align
                
                if debug == True:
                    print(1)
                    
                # If all of the selection is offcurves, just stop here.
                if list(set([p.type for p in g.selectedPoints])) == ['offcurve']:
                    continue
                
                # Otherwise, don't forget off-curves.
                for ocp_i in get_adj_pts_that_are_offcurve(p_i):
                    compare_p  = p.contour.points[p_i]
                    ocp        = p.contour.points[ocp_i]
                    ocp_dist_x = abs(ocp.x - p.x)
                    ocp_dist_y = abs(ocp.y - p.y)
                    # If the point is close enough, it will snap to the alignment average.
                    if compare_p.x - ocp_dist_threshold < ocp.x < compare_p.x + ocp_dist_threshold:
                        ocp.x = x_align
                        
                        if debug == True:
                            print(2)
                            
                    # If it's a smooth point #### and the handle isn't parallel to the alignment direction, the off-curve will snap to the alignment average.
                    elif p.smooth == True and ocp.y != p.y and ocp_dist_x < ocp_dist_y:  # and ocp.y < p.y - ocp_dist_threshold:
                        ocp.x = get_x_align_vert(ocp.x, ocp.y)

                        print("ocp.index", ocp.index)
                        print("p_i", p_i)
                        
                        if debug == True:
                            print(3)
                            
                    # Otherwise, the off-curve-to-on-curve relationship will be maintained
                    else:
                        ocp.x += x_delta
                        
                        if debug == True:
                            print(4)
                        
        # Same-ish for horizontal
        else:
            for p in g.selectedPoints:
                p_i = p._get_index()
                
                x_align = get_x_align_horiz(p.x, p.y)
                y_align = mid_y
                    
                x_delta, y_delta = x_align - p.x, y_align - p.y
                
                p.x, p.y = x_align, y_align
                
                if debug == True:
                    print(5)
                    
                # If all of the selection is offcurves, just stop here.
                if list(set([p.type for p in g.selectedPoints])) == ['offcurve']:
                    continue
                            
                # Otherwise, don't forget off-curves.
                for ocp_i in get_adj_pts_that_are_offcurve(p_i):
                    compare_p = p.contour.points[p_i]
                    ocp       = p.contour.points[ocp_i]
                    ocp_dist_x = abs(ocp.x - p.x)
                    ocp_dist_y = abs(ocp.y - p.y)
                    if compare_p.y - ocp_dist_threshold < ocp.y < compare_p.y + ocp_dist_threshold:
                        ocp.y = y_align
                        
                        if debug == True:
                            print(6)
                    elif p.smooth == True and ocp.x != p.x and ocp_dist_y < ocp_dist_x:  # Make this capture smooth off-curve more effectively. Currently only skips those that are perfectly, vertically above
                        ocp.x = get_x_align_horiz(ocp.x, ocp.y)
                        ocp.y = y_align
                        
                        if debug == True:
                            print(7)
                    else:
                        ocp.x += x_delta
                        ocp.y += y_delta
                        
                        if debug == True:
                            print(8)
                        
        # Immediately reflect the changes in glyph view.
        g.changed()
        
        
