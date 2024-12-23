# menuTitle: (Start-up) Kerning ETA

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
    all_diffs = np.diff(l)
    if len(all_diffs) > 0:
        avg = np.mean(all_diffs)
    else:
        avg = 0
        
    return avg
    

class KerningETA:
    
    dataset_size = 100 # how many recent pairs you'll allow in your dataset, from which you will surmise the ETA
    sep = " "
    
    def __init__(self):

        self.f = CurrentFont()
        self.pair = ()
        self.pairs = []
        self.pairs_left = 0
        self.mm_open = False
        self.mm_fonts_open = []

        addObserver(self, "mmOpen", "MetricsMachine.ControllerWillOpen")
        addObserver(self, "mmClose", "MetricsMachine.ControllerWillClose")
        addObserver(self, "pairChanged", "MetricsMachine.currentPairChanged") 


    def mmOpen(self, notification):
        pass
            

    def mmClose(self, notification):
        self.mm_open = False

        if self.f in self.mm_fonts_open:
            self.mm_fonts_open.remove(self.f)
        

    def pairChanged(self, sender):

        self.f = CurrentFont()

        
        # Try getting the window
        try:
            from mm4.mmScripting import _getMainWindowControllerForFont, MetricsMachineScriptingError
            import metricsMachine

            controller = _getMainWindowControllerForFont(self.f)
            edit_view = controller.editView
            tool_group = edit_view.toolGroup
            prog_ind = tool_group.progressIndicator
        
            self.mm_open = True

        # If MM isn't open yet
        except (MetricsMachineScriptingError, ModuleNotFoundError) as se:
            # print("MetricsMachineScriptingError", se)
            self.mm_open = False
            return


        # If the window’s open...
        if self.mm_open == True:

            # Change the left pos of the text box depending on whether the progress indicator is present or not
            x, y, w, h = prog_ind.getPosSize()
            text_x = x + w + 10
            if prog_ind.isVisible() == False:
                text_x = x + 10
            
            
            # Add current font to list of fonts open
            if not self.f in self.mm_fonts_open:
                self.mm_fonts_open.append(self.f)

                # You haven't made the textbox yet
                tool_group.message_box = vanilla.TextBox(
                    (text_x, y, -10, 20), 
                    "",
                    alignment='right'
                    )

            else:
                # If it's not the back of the list (changing windows to another mmFont), reset pair count for time estimate
                if not self.f == self.mm_fonts_open[-1]:
                    self.pairs = []
                    self.update_pair_list(tool_group.message_box)

                # Move most recent to the back of the list
                self.mm_fonts_open.remove(self.f)
                self.mm_fonts_open.append(self.f)

                # If you have made the text box, just change the position
                tool_group.message_box.setPosSize((text_x, y, -10, 20))

            
            # Get the current pair
            current_pair = sender["pair"]
            if current_pair == self.pair:
                return
            self.pair = current_pair
            
            # Get where we are in the pair-list
            self.pl = metricsMachine.GetPairList()
            try:
                p_i = self.pl.index(self.pair)
                self.pairs_left = len(self.pl) - p_i - 1
            except ValueError:
                pass
                # print(f"Pair {self.pair} is not in the pairlist. Cannot calculate pairs-left in the pairlist.")
            
            self.update_pair_list(tool_group.message_box)
        
            # Calculate time
            time_per_pair = get_average_diff([b for a, b in self.pairs])
            time_left = self.pairs_left * time_per_pair
            ETA = time.time() + time_left
            if twenty_four == True:
                ETA = datetime.datetime.fromtimestamp(ETA).strftime('%H:%M')
            else:
                ETA = datetime.datetime.fromtimestamp(ETA).strftime('%-I:%M %p')
            
            # If you took a break, start the dataset from scratch
            if time_per_pair > 50:
                self.pairs = []
                self.update_pair_list(tool_group.message_box)
            
            # Set the appropriate info
            message = f"Remaining: {self.pairs_left} {self.sep} Δ: {round(time_per_pair, 1)} sec. {self.sep} ETA: {ETA}"
            if self.pairs_left == 0:
                message = f"You did it! And it’s {ETA}."
            tool_group.message_box.set(message)
        
        
    def update_pair_list(self, message_box):

        # Store recent pairs & set message if not enough pairs in the dataset
        if self.pair not in [a for a, b in self.pairs]:
            self.pairs.append((self.pair, time.time()))
            
            # Account for short pair-lists
            if len(self.pl) < self.dataset_size / 2:
                self.dataset_size = len(self.pl) / 2
                
            if len(self.pairs) > self.dataset_size:
                self.pairs.pop(0)
            else:
                message_box.set(f"Remaining: {self.pairs_left} {self.sep} Kern {self.dataset_size - len(self.pairs)} more pairs to get an ETA")
        


KerningETA()