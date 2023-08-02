# menuTitle : Glyph Beams

from vanilla import FloatingWindow, PopUpButton
from mojo.UI import CurrentGlyphWindow, getDefault
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber

'''
Start-up script that adds a little menu under your Glyph View,
which will place a measuring beam inside your Glyph View, the 
vertical position of which is determined by your Font's dimensions. 
Toggle the guides on and off.

Ryan Bugden
2023.08.01
2022.02.23
2019.04.02
'''

EXTENSION_KEY = "com.ryanbugden.glyphBeams"
ID_LIB_KEY    = EXTENSION_KEY + ".beamIdentifiers"
PREF_LIB_KEY  = EXTENSION_KEY + ".preferences"
OOB_DISTANCE  = 100


class GlyphBeams(Subscriber):


    def build(self):
        self.g = None
        self.f = CurrentFont()
        self.beam_color = tuple(getDefault("spaceCenterBeamStrokeColor"))
        self.title = 'Glyph Beams'

        try: 
            # Forcing the order of this dictionary
            self.prefs = {'Uppercase': self.f.lib[PREF_LIB_KEY]['Uppercase'], 'Lowercase': self.f.lib[PREF_LIB_KEY]['Lowercase'], 'Plumb': self.f.lib[PREF_LIB_KEY]['Plumb']}
        except KeyError:
            self.prefs = {'Uppercase': False, 'Lowercase': False, 'Plumb': False} # starting point of the settings
            self.store_prefs()

        self.width = 82  # Width of the button
        
        # Store these IDs in the extension, so they can be deleted on restart.
        try: 
            self.ids = self.f.lib[ID_LIB_KEY]
        except KeyError:
            self.ids = {'Uppercase': [], 'Lowercase': [], 'Plumb': []}
            self.store_ids()

            
    @property
    def window(self):
        return CurrentGlyphWindow()


    @property
    def bar(self):
        if not self.window:
            return
        return self.window.getGlyphStatusBar()


    def store_ids(self):
        self.f.lib[ID_LIB_KEY] = self.ids


    def store_prefs(self):
        self.f.lib[PREF_LIB_KEY] = self.prefs


    def glyphEditorDidOpen(self, info):
        # print("test_2 ", self.prefs)
        
        if not self.bar:
            return

        if hasattr(self.bar, "menuButton"):
            del self.bar.menuButton

        menuItems = list(self.prefs.keys())
        # print("menuItems", menuItems)
        menuItems.insert(0, self.title)
        self.bar.menuButton = PopUpButton((124, 0, self.width, 16), menuItems, sizeStyle="small", callback=self.callback)
        self.bar.menuButton.getNSPopUpButton().setPullsDown_(True)
        self.bar.menuButton.getNSPopUpButton().setBordered_(False)

        for i, menuItem in enumerate(self.bar.menuButton.getNSPopUpButton().itemArray()[1:]):
            value = list(self.prefs.values())[i]
            menuItem.setState_(value)
            # print("put menu items", i, menuItem, value)

        self.add_guides()
        
            
    def glyphEditorGlyphDidChangeMetrics(self, info):
        # update vertical guide position
        self.g = info['glyph']
        self.update_plumb()

                
    def glyphEditorDidSetGlyph(self, info):
        # update vertical guide position
        self.g = info['glyph']
        self.update_plumb()


    def glyphEditorFontInfoDidChange(self, info):
        self.update_horizontals()
        self.update_plumb()


    def update_plumb(self):
        '''Updates the x-position and angle of the plumb guideline'''
        if self.g:
            f = self.g.font
            for guideline in f.guidelines:
                if guideline.identifier in self.ids['Plumb']:
                    offset = 0
                    if 'com.typemytype.robofont.italicSlantOffset' in f.lib.keys():
                        offset = f.lib['com.typemytype.robofont.italicSlantOffset']
                    guideline.x = self.g.width/2 + offset
                    guideline.y = f.info.descender - OOB_DISTANCE
                    if f.info.italicAngle:
                        guideline.angle = 90 + f.info.italicAngle
            self.g.changed()


    def update_horizontals(self):
        '''Updates the y-position of the uppercase and lowercase guidelines'''
        if self.g:
            f = self.g.font
            for guideline in f.guidelines:
                if guideline.identifier in self.ids['Uppercase']:
                    guideline.y = f.info.capHeight / 2
                if guideline.identifier in self.ids['Lowercase']:
                    guideline.y = f.info.xHeight / 2
            self.g.changed()

        
    def callback(self, sender):
        # print("test_3 ", self.prefs)

        item = sender.getNSPopUpButton().selectedItem()
        item.setState_(not item.state())
        selection = []
        for i, menuItem in enumerate(self.bar.menuButton.getNSPopUpButton().itemArray()[1:]):
            if menuItem.state():
                selection.append(i)
        # print("selection", selection)

        # print("test_4 ", self.prefs)

        self.prefs = {'Uppercase': False, 'Lowercase': False, 'Plumb': False}
        # order gets messed up !
        if 0 in selection:
            self.prefs.update({'Uppercase' : True})
        if 1 in selection:
            self.prefs.update({'Lowercase' : True})
        if 2 in selection:
            self.prefs.update({'Plumb' : True})

        # print("test_5 ", self.prefs)

        self.store_prefs()
        self.add_guides()


    def clear_guides(self, font):
        for guideline in font.guidelines:
            for key in self.ids.keys():
                if guideline.identifier in self.ids[key]:
                    # remove cache of ids
                    self.ids[key].remove(guideline.identifier)
                    font.removeGuideline(guideline)

                    self.store_ids()


    def add_guides(self):    
        f = CurrentFont()
        self.clear_guides(f)
        
        if self.prefs["Uppercase"] == True:
            self.guide_cap = f.appendGuideline(name="Uppercase", position=(-OOB_DISTANCE, int((f.info.capHeight)/2)), angle=0, color=self.beam_color)
            self.guide_cap.showMeasurements = True
            self.guide_cap.locked = True
            self.ids['Uppercase'].append(self.guide_cap.identifier)

        if self.prefs["Lowercase"] == True:
            self.guide_x = f.appendGuideline(name="Lowercase", position=(-OOB_DISTANCE, int((f.info.xHeight)/2)), angle=0, color=self.beam_color)
            self.guide_x.showMeasurements = True
            self.guide_x.locked = True
            self.ids['Lowercase'].append(self.guide_x.identifier)

        if self.prefs["Plumb"] == True:
            self.guide_vert = f.appendGuideline(name="Plumb", position=(CurrentGlyph().width/2, f.info.descender - OOB_DISTANCE), angle=90, color=self.beam_color)
            self.guide_vert.showMeasurements = True
            self.guide_vert.locked = True
            self.ids['Plumb'].append(self.guide_vert.identifier)
            self.update_plumb()

        # print("test_6 ", self.prefs)
            
        try:
            CurrentGlyph().changed()
        except:
            pass
        self.store_ids()
        
    
registerGlyphEditorSubscriber(GlyphBeams)
