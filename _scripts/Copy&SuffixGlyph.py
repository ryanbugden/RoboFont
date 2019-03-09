# menuTitle: Copy & Suffix Selected Glyphs
# shortCut: shift+command+k

'''
A script that copies selected glyphs and adds your desired suffix to their glyph name.

Ryan Bugden
2019.03.04
'''

import mojo.UI

f = CurrentFont()

# This is the suffix value that the UI suggests for you every time. 
# Feel free to change this to your liking:
suggestion = "ss01"

desired_suffix = mojo.UI.AskString("Desired suffix?", value=suggestion, title="Copied Glyph Suffix Renamer")

for glyph_name in f.selection:
    if "." in glyph_name:
        base_name = glyph_name.split(".")[0]
    else:
        base_name = glyph_name
    newGlyph = f[base_name].copy()
    f.insertGlyph(f[base_name], base_name + "." + desired_suffix)
    # Making sure there are no unicode values
    f[base_name + "." + desired_suffix].unicode = None
    
f.update()
