import time
import datetime
import numpy as np

import vanilla
from mojo.events import addObserver, removeObserver


'''
Thanks to Tal Leming for pointing me to some MM UI infrastructure.

Ryan Bugden
22.07.28
'''

twenty_four = False # whether or not you would like to display the time in 24-hr or 12-hr time

def get_average_diff(l):
    a = np.array(l)
    all_diffs = np.diff(a)
    if len(all_diffs) > 0:
        avg = sum(all_diffs) / len(all_diffs)
    else:
        avg = 0
    
    return avg
    

class KerningETA:
    
    dataset_size = 20 # how many recent pairs you'll allow in your dataset, from which you will surmise the ETA
    sep = " "
    
    def __init__(self):

        self.f = CurrentFont()
        self.pair = ()
        self.pairs = []
        self.mm_open = False
        self.vanilla_initiated = False
        self.tool_group = None
        
        addObserver(self, "mmClose", "MetricsMachine.ControllerWillClose")
        addObserver(self, "pairChanged", "MetricsMachine.currentPairChanged") 
        

    def mmClose(self, sender):

        self.mm_open = False
        

    def pairChanged(self, sender):

        # try getting the window
        try:
            from mm4.mmScripting import _getMainWindowControllerForFont, MetricsMachineScriptingError
            import metricsMachine

            # Tal's code for grabbing the UI
            self.controller = _getMainWindowControllerForFont(self.f)
            self.edit_view = self.controller.editView
            self.tool_group = self.edit_view.toolGroup
            self.prog_ind = self.tool_group.progressIndicator
        
            self.mm_open = True

        # if MM isn't open yet
        except (MetricsMachineScriptingError, ModuleNotFoundError) as se:
            # print("MetricsMachineScriptingError", se)
            self.mm_open = False
            return
            
        # if the window’s open...
        if self.mm_open == True:
            
            # change the left pos of the text box depending on whether the progress indicator is present or not
            x, y, w, h = self.prog_ind.getPosSize()
            text_x = x + w + 10
            if self.prog_ind.isVisible() == False:
                text_x = x + 10
            
            # ... and you haven't made the textbox yet
            if self.vanilla_initiated == False:
                
                self.tool_group.message_box = vanilla.TextBox(
                    (text_x, y, -10, 20), 
                    "",
                    alignment='right'
                    )
                    
                self.vanilla_initiated = True

            # if you have made the text box, just change the position
            else:
                self.tool_group.message_box.setPosSize((text_x, y, -10, 20))
            
        # get the current pair
        current_pair = sender["pair"]
        if current_pair == self.pair:
            return
        self.pair = current_pair
        
        # get where we are in the pair-list
        self.pl = metricsMachine.GetPairList()
        p_i = self.pl.index(self.pair)
        self.pairs_left = len(self.pl) - p_i
        
        self.updatePairlist()
    
        # calculate time
        time_per_pair = get_average_diff([b for a, b in self.pairs])
        time_left = self.pairs_left * time_per_pair
        ETA = time.time() + time_left
        if twenty_four == True:
            ETA = datetime.datetime.fromtimestamp(ETA).strftime('%H:%M')
        else:
            ETA = datetime.datetime.fromtimestamp(ETA).strftime('%-I:%M %p')
        
        # if you took a break, start the dataset from scratch
        if time_per_pair > 60:
            self.pairs = []
            self.updatePairlist()
        
        # set the appropriate info
        self.tool_group.message_box.set(f"Remaining: {self.pairs_left} {self.sep} Δ: {round(time_per_pair, 1)} sec. {self.sep} ETA: {ETA}")
        
        
    def updatePairlist(self):

        # store recent pairs & set message if not enough pairs in the dataset
        if not self.pair in [a for a, b in self.pairs]:
            self.pairs.append((self.pair, time.time()))
            
            # account for short pair-lists
            if len(self.pl) < self.dataset_size / 2:
                self.dataset_size = len(self.pl) / 2
                
            if len(self.pairs) > self.dataset_size:
                self.pairs.pop(0)
            else:
                self.tool_group.message_box.set(f"Remaining: {self.pairs_left} {self.sep} Kern {self.dataset_size - len(self.pairs)} more pairs to get an ETA")
                return
        


KerningETA()