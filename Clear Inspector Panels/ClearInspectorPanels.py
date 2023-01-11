# menuTitle : Clear Inspector Panels

from mojo.subscriber import Subscriber, registerRoboFontSubscriber


'''
Choose which Inspector panels you'd like to hide.
Customize below and add as a start-up script.

Ryan Bugden
2019.03.30
2022.02.01
2023.01.11 Rewritten with Subscribers
'''

# Set visibility of each panel
panels = {
    'Glyph'      :  True,
    'Preview'    :  False,
    'Layers'     :  True,
    'Transform'  :  True,
    'Points'     :  True, # Note: setting this to False may cause slowness.
    'Components' :  True,
    'Anchors'    :  True,
    'Note'       :  False,
    'Guidelines' :  False
    }
    
    
# ================================================
    

class ClearInspectorPanels(Subscriber):
    
    def build(self):
        pass

    def roboFontWantsInspectorViews(self, info):
        
        # print('\nYou’re now opening Inspector along with a script that clears some of its panels:')
        # print('********************')
        
        descs = info['viewDescriptions']
        
        false_keys = []
        for key in panels.keys():
            if panels[key] == False:
                false_keys.append(key)
                
        for i in reversed(range(len(descs))):
            if descs[i]['label'] in false_keys:
                false_title = descs[i]['label']
                del descs[i]
                # print('Cleared %s from the Inspector panel' % false_title)
    
    
registerRoboFontSubscriber(ClearInspectorPanels)