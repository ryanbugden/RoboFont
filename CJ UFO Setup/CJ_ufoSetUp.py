# menuTitle: CJ - UFO Setup - 600

'''
Open an empty UFO and run this script to begin setting up a basic font with Chinese and Japanese ideographs in Robofont.
To add more glyphs to what will be generated, change the "hanzi" and "kanji" lists.
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

# List of ~300 Hanzi glyphs
hanzi = ["uni4E00", "uni4E03", "uni4E07", "uni4E09", "uni4E0A", "uni4E0B", "uni4E0D", "uni4E1A", "uni4E1C", "uni4E24", "uni4E2A", "uni4E2D", "uni4E3A", "uni4E3B", "uni4E50", "uni4E5D", "uni4E5F", "uni4E60", "uni4E66", "uni4E86", "uni4E8C", "uni4E91", "uni4E94", "uni4E9B", "uni4EA4", "uni4EAC", "uni4EAE", "uni4EBA", "uni4EC0", "uni4ECA", "uni4ECE", "uni4ED6", "uni4EE5", "uni4EEC", "uni4F1A", "uni4F46", "uni4F4F", "uni4F5C", "uni4F60", "uni505A", "uni513F", "uni5143", "uni5148", "uni5149", "uni5168", "uni516B", "uni516C", "uni516D", "uni5171", "uni5173", "uni5174", "uni518C", "uni518D", "uni519B", "uni519C", "uni51AC", "uni51E0", "uni51FA", "uni5200", "uni5206", "uni522B", "uni5230", "uni524D", "uni529B", "uni529E", "uni52A0", "uni52A8", "uni5305", "uni5317", "uni533B", "uni5341", "uni5343", "uni5348", "uni534A", "uni536B", "uni5382", "uni53BB", "uni53C8", "uni53CC", "uni53CD", "uni53D1", "uni53E3", "uni53EA", "uni53EB", "uni53EF", "uni53F0", "uni53F6", "uni5403", "uni5408", "uni540C", "uni540E", "uni5411", "uni542C", "uni5435", "uni548C", "uni54E5", "uni54ED", "uni56DB", "uni56DE", "uni56E0", "uni56FD", "uni571F", "uni5728", "uni5730", "uni5750", "uni58F0", "uni5916", "uni591A", "uni5927", "uni5929", "uni592A", "uni5934", "uni5947", "uni5973", "uni5976", "uni5979", "uni597D", "uni5988", "uni59B9", "uni59D0", "uni5B50", "uni5B57", "uni5B66", "uni5B69", "uni5BB6", "uni5BF9", "uni5C0F", "uni5C11", "uni5C31", "uni5C3A", "uni5C71", "uni5C81", "uni5DE5", "uni5DF1", "uni5DFE", "uni5E02", "uni5E08", "uni5E72", "uni5E73", "uni5E74", "uni5E7F", "uni5E8A", "uni5F00", "uni5F53", "uni5F88", "uni5FC3", "uni5FEB", "uni6210", "uni6211", "uni624B", "uni624D", "uni6253", "uni627E", "uni628A", "uni653E", "uni6587", "uni65B9", "uni65E5", "uni65E9", "uni65F6", "uni660E", "uni661F", "uni6625", "uni662F", "uni665A", "uni66F4", "uni6708", "uni6709", "uni670B", "uni6728", "uni672C", "uni673A", "uni6761", "uni6765", "uni6797", "uni679C", "uni6811", "uni6821", "uni6837", "uni684C", "uni6B21", "uni6B63", "uni6BCF", "uni6BD4", "uni6BDB", "uni6C11", "uni6C14", "uni6C34", "uni6C5F", "uni6CA1", "uni6CB3", "uni6D17", "uni6D77", "uni706B", "uni706F", "uni70B9", "uni7136", "uni7237", "uni7238", "uni7247", "uni7259", "uni725B", "uni72D7", "uni732B", "uni738B", "uni73A9", "uni73B0", "uni73ED", "uni74DC", "uni751F", "uni7528", "uni7530", "uni7535", "uni753B", "uni767D", "uni767E", "uni7684", "uni76AE", "uni76EE", "uni76F4", "uni770B", "uni771F", "uni7740", "uni77E5", "uni77F3", "uni7968", "uni79CB", "uni7A7F", "uni7A97", "uni7ACB", "uni7AD9", "uni7AF9", "uni7B11", "uni7C73", "uni7EA2", "uni7ECF", "uni7ED9", "uni7F51", "uni7F8A", "uni7F8E", "uni7FBD", "uni8001", "uni8033", "uni80D6", "uni8138", "uni81EA", "uni820C", "uni8239", "uni82B1", "uni8349", "uni866B", "uni884C", "uni8863", "uni88AB", "uni897F", "uni8981", "uni89C1", "uni8BA9", "uni8BDD", "uni8BED", "uni8BF4", "uni8BFE", "uni8C01", "uni8C46", "uni8D1D", "uni8D70", "uni8D77", "uni8DD1", "uni8DF3", "uni8EAB", "uni8F66", "uni8FB9", "uni8FC7", "uni8FD8", "uni8FD9", "uni8FDB", "uni9053", "uni90A3", "uni90FD", "uni91CC", "uni91D1", "uni957F", "uni95E8", "uni95EE", "uni9633", "uni9634", "uni96E8", "uni96EA", "uni9752", "uni9762", "uni97F3", "uni9875", "uni98CE", "uni98DE", "uni996D", "uni9971", "uni9A6C", "uni9AD8", "uni9C7C", "uni9E1F"]

# List of ~300 Kanji glyphs
kanji = ["u20B9F", "uni4E01", "uni4E08", "uni4E0E", "uni4E14", "uni4E16", "uni4E18", "uni4E19", "uni4E21", "uni4E26", "uni4E32", "uni4E38", "uni4E39", "uni4E3C", "uni4E45", "uni4E4F", "uni4E57", "uni4E59", "uni4E5E", "uni4E71", "uni4E73", "uni4E7E", "uni4E80", "uni4E88", "uni4E89", "uni4E8B", "uni4E92", "uni4E95", "uni4E9C", "uni4EA1", "uni4EAB", "uni4EAD", "uni4EC1", "uni4ECB", "uni4ECF", "uni4ED5", "uni4ED8", "uni4ED9", "uni4EE3", "uni4EE4", "uni4EEE", "uni4EF0", "uni4EF2", "uni4EF6", "uni4EFB", "uni4F01", "uni4F0E", "uni4F0F", "uni4F10", "uni4F11", "uni4F1D", "uni4F2F", "uni4F34", "uni4F38", "uni4F3A", "uni4F3C", "uni4F4D", "uni4F4E", "uni4F50", "uni4F53", "uni4F55", "uni4F59", "uni4F73", "uni4F75", "uni4F7F", "uni4F8B", "uni4F8D", "uni4F9B", "uni4F9D", "uni4FA1", "uni4FAE", "uni4FAF", "uni4FB5", "uni4FB6", "uni4FBF", "uni4FC2", "uni4FC3", "uni4FCA", "uni4FD7", "uni4FDD", "uni4FE1", "uni4FEE", "uni4FF3", "uni4FF5", "uni4FF8", "uni4FFA", "uni5009", "uni500B", "uni500D", "uni5012", "uni5019", "uni501F", "uni5023", "uni5024", "uni502B", "uni5039", "uni5049", "uni504F", "uni505C", "uni5065", "uni5074", "uni5075", "uni5076", "uni507D", "uni508D", "uni5091", "uni5098", "uni5099", "uni50AC", "uni50B2", "uni50B5", "uni50B7", "uni50BE", "uni50C5", "uni50CD", "uni50CF", "uni50D5", "uni50DA", "uni50E7", "uni5100", "uni5104", "uni5112", "uni511F", "uni512A", "uni5144", "uni5145", "uni5146", "uni514B", "uni514D", "uni5150", "uni515A", "uni5165", "uni5175", "uni5177", "uni5178", "uni517C", "uni5185", "uni5186", "uni518A", "uni5192", "uni5197", "uni5199", "uni51A0", "uni51A5", "uni51B6", "uni51B7", "uni51C4", "uni51C6", "uni51CD", "uni51DD", "uni51E1", "uni51E6", "uni51F6", "uni51F8", "uni51F9", "uni5203", "uni5207", "uni5208", "uni520A", "uni5211", "uni5217", "uni521D", "uni5224", "uni5225", "uni5229", "uni5236", "uni5237", "uni5238", "uni5239", "uni523A", "uni523B", "uni5247", "uni524A", "uni5256", "uni525B", "uni525D", "uni5263", "uni5264", "uni526F", "uni5270", "uni5272", "uni5275", "uni5287", "uni529F", "uni52A3", "uni52A9", "uni52AA", "uni52B1", "uni52B4", "uni52B9", "uni52BE", "uni52C3", "uni52C5", "uni52C7", "uni52C9", "uni52D5", "uni52D8", "uni52D9", "uni52DD", "uni52DF", "uni52E2", "uni52E4", "uni52E7", "uni52F2", "uni52FE", "uni5302", "uni5316", "uni5320", "uni5339", "uni533A", "uni533F", "uni5347", "uni5351", "uni5352", "uni5353", "uni5354", "uni5357", "uni5358", "uni535A", "uni5360", "uni5370", "uni5371", "uni5373", "uni5374", "uni5375", "uni5378", "uni5384", "uni5398", "uni539A", "uni539F", "uni53B3", "uni53C2", "uni53CA", "uni53CB", "uni53CE", "uni53D4", "uni53D6", "uni53D7", "uni53D9", "uni53E4", "uni53E5", "uni53EC", "uni53F2", "uni53F3", "uni53F7", "uni53F8", "uni5404", "uni5409", "uni540D", "uni540F", "uni5410", "uni541B", "uni541F", "uni5426", "uni542B", "uni5438", "uni5439", "uni5442", "uni5448", "uni5449", "uni544A", "uni5468", "uni546A", "uni5473", "uni547C", "uni547D", "uni54B2", "uni54BD", "uni54C0", "uni54C1", "uni54E1", "uni54F2", "uni54FA", "uni5504", "uni5506", "uni5507", "uni5510", "uni552F", "uni5531", "uni553E", "uni5546", "uni554F", "uni5553", "uni5584", "uni5589", "uni559A", "uni559C", "uni559D", "uni55A9", "uni55AA", "uni55AB", "uni55B6", "uni55C5", "uni55E3", "uni5606", "uni5631", "uni5632", "uni5668", "uni5674", "uni5687"]

# Combine them
new_glyphs = hanzi + kanji

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
