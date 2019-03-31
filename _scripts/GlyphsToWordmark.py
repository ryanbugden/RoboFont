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

try: 
    f[new_g_name]
    f.removeGlyph(new_g_name)
except ValueError:
    pass
    
f.newGlyph(new_g_name)
g = f[new_g_name]
cursor = 0

for letter in new_g_name:
    if letter == ' ':
        cursor += f['space'].width
    else:
        g.appendComponent(letter, offset=(cursor, 0))
        cursor += f[letter].width
    
g.rightMargin = f[new_g_name[-1]].rightMargin
g.update()
