from mojo.events import installTool, EditingTool
from lib.tools.defaults import getDefault, getDefaultColor
from drawBot import linearGradient
from mojo.drawingTools import *
from AppKit import NSImage
from os import path

'''
Allows you to select the margins as if you would any point or segment. 
Click on the sidebearing and move it with the mouse or arrows!

Ryan Bugden
with thanks to Erik van Blokland and Frederik Berlaen

v0.1.1:   2019.04.10
v0.1.0:   2019.03.07
'''

dirname = path.dirname(__file__)
toolbarIcon = NSImage.alloc().initByReferencingFile_(path.join(dirname, "MarginSelectionToolIcon.pdf"))

class MarginSelectionTool(EditingTool):
    
    def setup(self):
        print('setting up Margin Selection')
        col = getDefaultColor("glyphViewSelectionColor")
        self.sel_color = (col.redComponent(), col.greenComponent(), col.blueComponent(), col.alphaComponent())
        self.RSBselected = False
        self.LSBselected = False
        self.font = CurrentFont()
        self.glyph = CurrentGlyph()
        self.position = None
        self.sensitivity = 6
        self.stroke_width = 1
        self.increment = 1
        self.shift_inc = getDefault("glyphViewShiftIncrement")
        self.shift_command_inc = getDefault("glyphViewCommandShiftIncrement")
        
        # print('Getting those observers ready.')
        # # Get ready for some observers
        # addObserver(self, 'mouseDragged', 'mouseDragged')
        # addObserver(self, 'mouseUp', 'mouseUp')
        # addObserver(self, 'mouseDown', 'mouseDown')
        # addObserver(self, 'keyDown', 'keyDown')
        # addObserver(self, 'draw', 'draw')
        # print('Observers ready.')
    
    def getToolbarIcon(self):
        return(toolbarIcon)
        
    def getToolbarTip(self):
        return "Margin Selection"

    def mouseDragged(self, point, delta):
        print("Mouse dragged.")
        self.position = point
        self.deltaX = delta.x
        self.newDeltaX = delta.x - self.deltaX
        if self.RSBselected == True:
            print(self.deltaX)
            self.glyph.rightMargin += self.newDeltaX
            self.glyph.update()
        if self.LSBselected == True:
            print(self.deltaX)
            self.glyph.leftMargin -= self.newDeltaX
            self.glyph.update()
            
    def mouseUp(self, point):
        print("Mouse up.")
        self.position = None

    def mouseDown(self, point, clickCount):
        #should i make an invisible bezier path around the point, and do a pointinside, to compensate for the 10 uncertainty?
        self.sel_points = []
        
        print("Mouse Down.")
        self.position = point
        self.position_tup = (int(point.x), int(point.y))
        print(self.position_tup)
        
        
        if self.glyph.width - self.sensitivity < self.position[0] < self.glyph.width + self.sensitivity:
            print(self.position[0], "Drawing right line")
            print("RSB is selected") 
            self.RSBselected = True
            self.LSBselected = False
            print("RSB selected reading as...", self.RSBselected)
        
        elif 0 - self.sensitivity < self.position[0] < 0 + self.sensitivity:
            print(self.position[0], "Drawing left line")
            print(True) 
            self.LSBselected = True
            self.RSBselected = False
            
        elif self.position_tup in self.sel_points:
            pass
            
        elif self.shiftDown == True or self.commandDown == True:
            pass
            
        # elif self.alsoGrabbedPoints()[0], self.alsoGrabbedPoints()[1] - 2 >self.position.x, self.position.y < self.alsoGrabbedPoints()[0], self.alsoGrabbedPoints()[1] + 2:
        #     print("also grabbed points")
        #     self.LSBselected = self.LSBselected
        #     self.RSBselected = self.RSBselected
            
        # elif self.position == (self.glyph.point.x, self.glyph.points.y):
        #     pass
            
        else:
            self.LSBselected = False
            self.RSBselected = False
            
        
        for point in self.glyph.selectedPoints:
            self.sel_points.append((point.x , point.y))
        print(self.sel_points)
        # for (x, y) in self.sel_points:
        #     print(y)
        # selection_threshold = 10

    def currentGlyphChanged(self):
        self.font = CurrentFont()
        self.glyph = CurrentGlyph()

    
    def keyDown(self, event):
        print("Keys Down.")
        print(self.arrowKeysDown)
        print("KEY RSB selected reading as...", self.RSBselected) 
        
        if self.RSBselected == True:
            if self.arrowKeysDown['left'] == True:
                if self.shiftDown == self.commandDown == True:
                    self.glyph.rightMargin -= self.shift_command_inc
                elif self.shiftDown == True:
                    self.glyph.rightMargin -= self.shift_inc
                else:
                    self.glyph.rightMargin -= self.increment
            if self.arrowKeysDown['right'] == True:
                if self.shiftDown == self.commandDown == True:
                    self.glyph.rightMargin += self.shift_command_inc
                elif self.shiftDown == True:
                    self.glyph.rightMargin += self.shift_inc
                else:
                    self.glyph.rightMargin += self.increment
                    
        if self.LSBselected == True:
            if self.arrowKeysDown['left'] == True:
                if self.shiftDown == self.commandDown == True:
                    self.glyph.leftMargin += self.shift_command_inc
                elif self.shiftDown == True:
                    self.glyph.leftMargin += self.shift_inc
                else:
                    self.glyph.leftMargin += self.increment
            if self.arrowKeysDown['right'] == True:
                if self.shiftDown == self.commandDown == True:
                    self.glyph.leftMargin -= self.shift_command_inc
                elif self.shiftDown == True:
                    self.glyph.leftMargin -= self.shift_inc
                else:
                    self.glyph.leftMargin -= self.increment
                    
    def draw(self, scale):
        strokeWidth(self.stroke_width)
        stroke(*self.sel_color)
        if self.RSBselected == True:   
            line((self.glyph.width, self.font.info.descender - 500),(self.glyph.width, self.font.info.ascender - self.font.info.descender + 500))
        elif self.LSBselected == True:
            line((0,self.font.info.descender - 500),(0,self.font.info.ascender - self.font.info.descender + 500))
            # why does the line still stay there when the LSB is dragged?
        else:
            pass

    def alsoGrabbedPoints(self):
        self.glyph = CurrentGlyph()

        for c in self.glyph:
            for s in c:
                for p in s:
                    if p.selected:
                        return p.x, p.y
            
        
        
installTool(MarginSelectionTool())

