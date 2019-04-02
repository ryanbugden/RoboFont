# menuTitle : Clear Inspector Panels

'''
Choose which Inspector panels you'd like to hide.
Customize below and add as a start-up script.

Ryan Bugden
2019.03.30
'''

# Set what you want hidden as False:
panels = {
    'Glyph'      :  True,
    'Preview'    :  False,
    'Layers'     :  True,
    'Transform'  :  True,
    'Points'     :  False,
    'Components' :  True,
    'Anchors'    :  True,
    'Note'       :  False
    }
    
    
# ================================================
    
from mojo.events import addObserver

class ClearInspectorPanels:
    
    def __init__(self):
        addObserver(self, "inspectorWindowWillShowDescriptions", "inspectorWindowWillShowDescriptions")

    def inspectorWindowWillShowDescriptions(self, notification):
        
        print('You’re now opening Inspector along with a script that clears some of its panels:')
        print('********************')
        
        false_keys = []
        for key in panels.keys():
            if panels[key] == False:
                false_keys.append(key)
                
        for i in reversed(range(len(notification["descriptions"]))):
            if notification["descriptions"][i]['label'] in false_keys:
                false_title = notification["descriptions"][i]['label']
                del notification["descriptions"][i]
                print('Cleared %s from the Inspector panel' % false_title)
                print('')
    
    
ClearInspectorPanels()
