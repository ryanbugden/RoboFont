# menuTitle: CJ - UFO Setup - Quick

'''
Open an empty UFO and run this script to begin setting up a basic font with Chinese and Japanese ideographs in Robofont.
To add more glyphs to what will be generated, change the "new_glyphs" list.
This script also alters your preferences: New glyphs added will always have the same set width as what you set here.
If the glyphs don't show up in your glyph palette, try saving the UFO, closing, and reopening.

Ryan Bugden
2019.10.12
Thanks to TienMin Liao for the idea.
'''

import mojo.drawingTools
from lib.tools.defaults import setDefault

# Set colors of boxes
big_box_color    = (1, 0, 0, 0.5)
small_box_color  = (0, 0, 1, 0.5)

# Set size of your box
set_width        = 1000
set_height       = 1000 # Maybe don't change this...
small_box_height = 850
y_offset         = -50

# Set x, cap, asc to all the same value
vert_metric      = 900


# ====vvv==== SHOULDN’T NEED TO CHANGE BELOW ====vvv==== #

box_margin = (set_height - small_box_height) / 2

# Combine them
new_glyphs = ["uni56FD", "uni570B", "uni611B", "uni7231", "uni6C38", "uni888B", "uni970A", "uni9748", "uni7075", "uni916C", "uni4ECA", "uni529B", "uni9DF9", "uni9E70", "uni4E09", "uni9B31", "uni90C1"]

# Define our font, the frontmost open one
f = CurrentFont()
    
# Setting vertical metrics to something simpler and non-Latin
f.info.capHeight = f.info.xHeight = f.info.ascender = vert_metric
f.info.descender = 0

# Making background layers that will have the boxes
f.newLayer("big_box",   color=big_box_color)
f.newLayer("small_box", color=small_box_color)

def drawBox(x, y, width, height, glyph):
    pen = glyph.getPen()
    pen.moveTo((x, y))
    pen.lineTo((width + x, y))
    pen.lineTo((width + x, height + y))
    pen.lineTo((x, height + y))
    pen.closePath()

# Set how you want it to display    
def setBoxDisplay(layer):
    layer.setDisplayOption('Fill', False) 
    layer.setDisplayOption('Stroke', True)
    layer.setDisplayOption('Points', False)
    layer.setDisplayOption('Coordinates', False)
    
# Make a template to be used as a component
small = f.getLayer("small_box")
small.newGlyph("box_templates", clear=True)
s_t = small["box_templates"]
s_t.clear()
drawBox(box_margin, box_margin + y_offset, set_width - box_margin*2, set_height - box_margin*2, s_t)
s_t.width = set_width

big = f.getLayer("big_box")
big.newGlyph("box_templates", clear=True)
b_t = big["box_templates"]
b_t.clear()
drawBox(0, y_offset, set_width, set_height, b_t)
b_t.width = set_width
    
    
# Run through all the glyphs in the list ^
for g_name in new_glyphs:
    
    # Run through all the layers in the font
    for layer in f.layers:
        
        # Make each glyph
        if not g_name in layer:
            layer.newGlyph(g_name, clear=True)
            
        l_g = layer[g_name]
        l_g.width = set_width
        
        # For the big box layer, draw a big box
        if layer.name == "big_box":
            
            # Clear the old box, if you're rerunning this script with different measurements
            l_g.clear()
            l_g.appendComponent("box_templates")
            
            setBoxDisplay(layer)
            l_g.changed()
            
        # For the small box layer, draw/redraw a small box
        elif layer.name == "small_box":
            
            # Clear the old box, if you're rerunning this script with different measurements
            l_g.clear()
            l_g.appendComponent("box_templates")
            
            setBoxDisplay(layer)
            l_g.changed()
            
    # Removing foreground blanks, to reveal glyph templates
    fore = f.getLayer("foreground")
    if g_name in fore:
        g = fore[g_name]
        if g.components == () and g.contours == ():
            fore.removeGlyph(g_name)

# Set your preferences such that each time you add a glyph, its width is correct
setDefault("newGlyphWidth", set_width)
