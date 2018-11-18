# menuTitle: Copied Glyph Suffix Renamer
# shortCut: shift+command+k

import re
import mojo.UI

font = CurrentFont()
existing_suffix = "copy_"

copies = []
for glyph in font.keys():
        if re.search(r".*\.%s[1-9]" %existing_suffix, glyph) != None:
            copies.append("copy")
    
if "copy" in copies:
    desired_suffix = mojo.UI.AskString("Desired suffix?", value="ss01", title="Copied Glyph Suffix Renamer")
    for glyph in font:
        print(glyph.name)
        glyph.name = re.sub(r"\.%s([1-9])" %existing_suffix, r".%s" %desired_suffix,  glyph.name)
        print(glyph.name)
        glyph.update()

else:
    mojo.UI.dontShowAgainMessage(messageText='Nothing done.', 
    informativeText='There were no \"copy_\" suffixes to replace.', 
    alertStyle=1, 
    parentWindow=None, 
    resultCallback=None, 
    dontShowAgainKey='Yes')
    
font.update()
