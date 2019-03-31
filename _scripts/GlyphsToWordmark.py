# menuTitle : Glyphs to Wordmark

'''
Compiles a glyph consisting of components 
of letters in the string you provide.

Ryan Bugden
2019.03.31
'''

from mojo.UI import AskString

f = CurrentFont()

new_g_name = AskString('What word would you like to compose?', value='', title='New wordmark')

# If the glyph exists, it removes it.
try: 
    f[new_g_name]
    f.removeGlyph(new_g_name)
except ValueError:
    pass
    
# Create the glyph
f.newGlyph(new_g_name)
g = f[new_g_name]
cursor = 0

# Add each letter of the string to the glyph as a component
for letter in new_g_name:
    if letter == ' ':
        cursor += f['space'].width
    else:
        g.appendComponent(letter, offset=(cursor, 0))
        cursor += f[letter].width

# Set the right margin to that of the last letter of the string
g.rightMargin = f[new_g_name[-1]].rightMargin
g.update()
