# menuTitle: Rotate 180 All Layers
# shortCut: shift+command+r

# Rotate all layers 180 degrees, within current glyph.
# Use your preferred shortcut in line 2.
# 2018/11/12

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

glyph.prepareUndo()

# uncommon glyphs rotate around their physical midpoint
if glyph.unicode == None:
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
