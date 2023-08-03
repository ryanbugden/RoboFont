# menuTitle : Copy Glyph Names Menu

from mojo.subscriber import Subscriber, registerFontOverviewSubscriber
from AppKit import NSPasteboardTypeString, NSPasteboard


class copyGlyphsAs(Subscriber):
    
    '''
    A contextual menu in the Font View. Right click selected glyphs 
    to copy glyphs names to your clipboard in any provided format.
    This is a cobbling-together of Erik van Blokland’s copyNamesToClipboard.py 
    and Robofont’s example code for contextual menus. Implement as a 
    startup script or extension.
    
    2019.11.06
    Ryan Bugden
    '''
    
    max_title_length = 20


    def build(self):
        pass
        
    def fontOverviewWantsContextualMenuItems(self, info):
        # print(info)
        self.font = CurrentFont()
        if self.font is None:
            self.names = []
        else:
            self.names = self.get_selection()
        
        my_menu_items = [
            ("Copy names as...", [
                (self._as_title(self._as_spaced_names(self.names)), self.spaced_names_callback),
                (self._as_title(self.as_list_names(self.names)), self.list_names_callback),
                (self._as_title(self._as_feature_group(self.names)), self.feature_group_callback),
                (self._as_title(self._as_slashed_names(self.names)), self.slashed_names_callback),
                (self._as_title(self._as_unicode_text(self.names)), self.unicode_text_callback)
                ]
            )
        ]
        # print(info['itemDescriptions'])
        if "Copy names as..." in info['itemDescriptions']:
            print("Copy names menu is here.")
        
        info['itemDescriptions'].extend(my_menu_items)
        
#===================

    def spaced_names_callback(self, sender):
        self.to_pasteboard(self._as_spaced_names(self.names))
        # print("spaced_names_callback selected")

    def list_names_callback(self, sender):
        self.to_pasteboard(self.as_list_names(self.names))
        # print("list_names_callback selected")
        
    def feature_group_callback(self, sender):
        self.to_pasteboard(self._as_feature_group(self.names))
        # print("feature_group_callback selected")

    def slashed_names_callback(self, sender):
        self.to_pasteboard(self._as_slashed_names(self.names))
        # print("slashed_names_callback selected")
        
    def unicode_text_callback(self, sender):
        self.to_pasteboard(self._as_unicode_text(self.names))
        # print("unicode_text_callback selected")
        
#===================
        
    def _as_spaced_names(self, names):
        return " ".join(names)

    def as_list_names(self, names):
        return "[" + ", ".join(["\"%s\""%s for s in names]) + "]"
        
    def _as_feature_group(self, names):
        return "[%s]"%" ".join(names)

    def _as_slashed_names(self, names):
        return "/"+"/".join(names)
        
    def _as_unicode_text(self, names):
        return "/"+"/".join(names)

    def _as_title(self, text):
        if len(text)<self.max_title_length:
            return text
        return text[:self.max_title_length]+u" …"
        
    def _as_unicode_text(self, names):
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
        
    def get_selection(self):
        ordered = []
        missing = []
        sel = list(set(self.font.templateSelectedGlyphNames) | set(self.font.selectedGlyphNames))
        for n in self.font.lib['public.glyphOrder']:
            if n in sel:
                ordered.append(n)
        return ordered
        
    def to_pasteboard(self, text):
        pb = NSPasteboard.generalPasteboard()
        pb.clearContents()
        pb.declareTypes_owner_([
            NSPasteboardTypeString,
        ], None)
        pb.setString_forType_(text, NSPasteboardTypeString)
        
#===================
        
if __name__ == "__main__":    
    registerFontOverviewSubscriber(copyGlyphsAs)
