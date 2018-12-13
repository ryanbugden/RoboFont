# menuTitle: Rotate 180 - All Layers
# shortCut: shift+command+r

'''
A script that rotates your glyph and all of its layers. 
It does its best to rotate it in a helpful way, not 
necessarily just around the body of the contours themselves.
Use your preferred shortcut in line 2.

Last updated: 2018/12/13
'''

font = CurrentFont()
glyph = CurrentGlyph()

# list of layers in the font
layers = font._get_layerOrder()


# function that rotates all layers 180 around a given center point
def rotate180AllLayers(centerX, centerY):
    for layer in range(len(layers)):
        l = glyph.getLayer(layers[layer])
        l.rotateBy(180, 
        (centerX,centerY)
        )
        l.image.rotateBy(180, 
        (centerX,centerY)
        )

# finding a midpoint for the glyph
midpointX = glyph.bounds[0] + (glyph.bounds[2] - glyph.bounds[0]) / 2
midpointY = glyph.bounds[1] + (glyph.bounds[3] - glyph.bounds[1]) / 2

glyph.prepareUndo("Rotate")

# uncommon glyphs rotate around their physical midpoint
if glyph.unicode == None:
    if "." in glyph.name:
        glyph_parent_name = glyph.name.split(".")[0]
        character = chr(font[glyph_parent_name].unicode)

        if character == character.upper():
            rotate180AllLayers(glyph.width/2, font.info.capHeight/2)
    
        elif character == character.lower():
            rotate180AllLayers(glyph.width/2, font.info.xHeight/2)
    
    # a catch-all        
    else:
        rotate180AllLayers(midpointX, midpointY)

# common glyphs rotate around the midpoint of the font's metrics
# this is beneficial, for example, if you want to rotate a /b around its bowl, not its full height
else:    
    character = chr(glyph.unicode)

    if character == character.upper():
        rotate180AllLayers(glyph.width/2, font.info.capHeight/2)
    
    elif character == character.lower():
        rotate180AllLayers(glyph.width/2, font.info.xHeight/2)

glyph.performUndo()
glyph.update()
