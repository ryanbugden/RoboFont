from mojo.events import addObserver
from AppKit import NSPasteboardTypeString, NSPasteboard

class copyNamesAs(object):
    
    '''
    A contextual menu in the Font View. Right click selected glyphs 
    to copy glyphs names to your clipboard in any provided format.
    This is a cobbling-together of Erik van Blokland’s copyNamesToClipboard.py 
    and Robofont’s example code for contextual menus. Implement as a 
    startup script or extension.
    
    2019.11.06
    Ryan Bugden, Erik van Blokland, Frederik Berlaen, Gustavo Ferreira
    '''
    
    maxTitleLength = 20

    def __init__(self):
        addObserver(self, "fontOverviewAdditionContextualMenuItems", "fontOverviewAdditionContextualMenuItems")
        
    def fontOverviewAdditionContextualMenuItems(self, notification):
        self.font = CurrentFont()
        if self.font is None:
            self.names = []
        else:
            self.names = self.getSelection()
        
        myMenuItems = [
            ("Copy names as...", [
                (self._asTitle(self._asSpacedNames(self.names)), self.spacedNamesCallback),
                (self._asTitle(self._asListNames(self.names)), self.listNamesCallback),
                (self._asTitle(self._asFeatureGroup(self.names)), self.featureGroupCallback),
                (self._asTitle(self._asSlashedNames(self.names)), self.slashedNamesCallback),
                (self._asTitle(self._asUnicodeText(self.names)), self.unicodeTextCallback)
                ]
            )
        ]
        notification["additionContextualMenuItems"].extend(myMenuItems)
        
#===================

    def spacedNamesCallback(self, sender):
        self._toPasteBoard(self._asSpacedNames(self.names))
        print("spacedNamesCallback selected")

    def listNamesCallback(self, sender):
        self._toPasteBoard(self._asListNames(self.names))
        print("listNamesCallback selected")
        
    def featureGroupCallback(self, sender):
        self._toPasteBoard(self._asFeatureGroup(self.names))
        print("featureGroupCallback selected")

    def slashedNamesCallback(self, sender):
        self._toPasteBoard(self._asSlashedNames(self.names))
        print("slashedNamesCallback selected")
        
    def unicodeTextCallback(self, sender):
        self._toPasteBoard(self._asUnicodeText(self.names))
        print("unicodeTextCallback selected")
        
#===================
        
    def _asSpacedNames(self, names):
        return " ".join(names)

    def _asListNames(self, names):
        return "[" + ", ".join(["\"%s\""%s for s in names]) + "]"
        
    def _asFeatureGroup(self, names):
        return "[%s]"%" ".join(names)

    def _asSlashedNames(self, names):
        return "/"+"/".join(names)
        
    def _asUnicodeText(self, names):
        return "/"+"/".join(names)

    def _asTitle(self, text):
        if len(text)<self.maxTitleLength:
            return text
        return text[:self.maxTitleLength]+u" …"
        
    def _asUnicodeText(self, names):
        text = ""
        for n in names:
            if self.font[n].unicode is not None:
                try:
                    text += unichr(self.font[n].unicode)
                except NameError: # python 3
                    text += chr(self.font[n].unicode)
        if not text:
            return "[no unicodes]"
        return text
        
    def getSelection(self):
        ordered = []
        missing = []
        sel = list(set(self.font.templateSelection) | set(self.font.selection))
        for n in self.font.lib['public.glyphOrder']:
            if n in sel:
                ordered.append(n)
        return ordered
        
    def _toPasteBoard(self, text):
        pb = NSPasteboard.generalPasteboard()
        pb.clearContents()
        pb.declareTypes_owner_([
            NSPasteboardTypeString,
        ], None)
        pb.setString_forType_(text, NSPasteboardTypeString)
        
#===================
        
if __name__ == "__main__":    
    copyNamesAs()
