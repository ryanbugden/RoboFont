# menuTitle: Rotate 180 - All Layers
# shortCut: shift + command + r

'''
A script that rotates your glyph and all of its layers. 
It does its best to rotate it in a helpful way, not 
necessarily just around the body of the contours themselves.
Use your preferred shortcut in line 2.

Ryan Bugden
2023.08.01
2020.01.24
2018.12.13
2018.11.12
'''

import math

f = CurrentFont()
g = CurrentGlyph()

# function that rotates all layers 180 around a given center point
def rotate_all_layers_180(center_x, center_y):
    layers = f.layerOrder
    # If you're on the foreground, rotate all layers.
    if CurrentLayer() == f.defaultLayer:
        for layer in range(len(layers)):
            l = g.getLayer(layers[layer])
            l.rotateBy(180, 
                    (center_x,center_y)
                )
            l.image.rotateBy(180, 
                    (center_x,center_y)
                )
    # If you're not on the foreground, rotate all layers behind foreground.
    else:
        for layer in range(len(layers)):
            l = g.getLayer(layers[layer])
            if l.layer.name != 'foreground':
                l = g.getLayer(layers[layer])
                l.rotateBy(180, 
                        (center_x,center_y)
                    )
                l.image.rotateBy(180, 
                        (center_x,center_y)
                    )

# Account for italics
def get_x_offset(h):
    try:
        italic_offset = f.lib['com.typemytype.robofont.italicSlantOffset']
    except:
        italic_offset = 0

    iv = f.info.italicAngle
    if iv == None: iv = 0

    # Convert degrees to radians in the process
    adjust = math.tan(-iv * math.pi/180) * h
    adjust += italic_offset
    
    return adjust


upper_x_offset = get_x_offset(f.info.capHeight / 2)
lower_x_offset = get_x_offset(f.info.xHeight / 2)
    

# Find a simple midpoint for the glyph. save for later
mid_x = g.bounds[0] + (g.bounds[2] - g.bounds[0]) / 2
mid_y = g.bounds[1] + (g.bounds[3] - g.bounds[1]) / 2

with g.undo("Rotate all layers 180 degrees"):
    # Uncommon glyphs rotate around their physical midpoint
    if not g.unicode:
        if "." in g.name:
            g_parent_name = g.name.split(".")[0]
            if f[g_parent_name].unicode != None:
                character = chr(f[g_parent_name].unicode)

                if character == character.upper():
                    rotate_all_layers_180(g.width/2 + upper_x_offset, f.info.capHeight/2)
        
                elif character == character.lower():
                    rotate_all_layers_180(g.width/2 + lower_x_offset, f.info.xHeight/2)
            else:
                rotate_all_layers_180(mid_x, mid_y)
            
        # If the foreground has a unicode, reference that.
        elif g.getLayer('foreground').unicode:
            character = chr(g.getLayer('foreground').unicode)
            if character == character.upper():
                rotate_all_layers_180(g.width/2 + upper_x_offset, f.info.capHeight/2)
    
            elif character == character.lower():
                rotate_all_layers_180(g.width/2 + lower_x_offset, f.info.xHeight/2)
        # A catch-all        
        else:
            rotate_all_layers_180(mid_x, mid_y)

    # Common glyphs rotate around the midpoint of the font's metrics.
    # This is beneficial, for example, if you want to rotate a "b"" around its bowl, not its full height.
    else:    
        character = chr(g.unicode)

        if character == character.upper():
            rotate_all_layers_180(g.width/2  + upper_x_offset, f.info.capHeight/2)
    
        elif character == character.lower():
            rotate_all_layers_180(g.width/2  + lower_x_offset, f.info.xHeight/2)

    g.changed()
