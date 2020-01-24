# menuTitle: Rotate 180 - All Layers
# shortCut: shift+command+r

'''
A script that rotates your glyph and all of its layers. 
It does its best to rotate it in a helpful way, not 
necessarily just around the body of the contours themselves.
Use your preferred shortcut in line 2.

Ryan Bugden
2020.01.24
2018.12.13
2018.11.12
'''

f = CurrentFont()
g = CurrentGlyph()

# list of layers in the font
layers = f._get_layerOrder()


# function that rotates all layers 180 around a given center point
def rotate180AllLayers(centerX, centerY):
	
	# If you're on the foreground, rotate all layers.
	if CurrentLayer().name == 'foreground':
		for layer in range(len(layers)):
			l = g.getLayer(layers[layer])
			l.rotateBy(180, 
			(centerX,centerY)
			)
			l.image.rotateBy(180, 
			(centerX,centerY)
			)
	# If you're not on the foreground, rotate all layers behind foreground.
	else:
		for layer in range(len(layers)):
			l = g.getLayer(layers[layer])
			if l.layer.name != 'foreground':
				l = g.getLayer(layers[layer])
				l.rotateBy(180, 
				(centerX,centerY)
				)
				l.image.rotateBy(180, 
				(centerX,centerY)
				)

# finding a midpoint for the glyph
midpointX = g.bounds[0] + (g.bounds[2] - g.bounds[0]) / 2
midpointY = g.bounds[1] + (g.bounds[3] - g.bounds[1]) / 2

with g.undo("Rotate All Layers"):
	# uncommon glyphs rotate around their physical midpoint
	if g.unicode == None:
		if "." in g.name:
			g_parent_name = g.name.split(".")[0]
			if f[g_parent_name].unicode != None:
				character = chr(f[g_parent_name].unicode)

				if character == character.upper():
					rotate180AllLayers(g.width/2, f.info.capHeight/2)
		
				elif character == character.lower():
					rotate180AllLayers(g.width/2, f.info.xHeight/2)
			else:
				rotate180AllLayers(midpointX, midpointY)
			
		# If the foreground has a unicode, reference that.
		elif g.getLayer('foreground').unicode != None:
			character = chr(g.getLayer('foreground').unicode)
			if character == character.upper():
				rotate180AllLayers(g.width/2, f.info.capHeight/2)
	
			elif character == character.lower():
				rotate180AllLayers(g.width/2, f.info.xHeight/2)
		# a catch-all        
		else:
			rotate180AllLayers(midpointX, midpointY)

	# common glyphs rotate around the midpoint of the font's metrics
	# this is beneficial, for example, if you want to rotate a /b around its bowl, not its full height
	else:    
		character = chr(g.unicode)

		if character == character.upper():
			rotate180AllLayers(g.width/2, f.info.capHeight/2)
	
		elif character == character.lower():
			rotate180AllLayers(g.width/2, f.info.xHeight/2)

	g.changed()
