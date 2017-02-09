from bdflib import reader
from numpy import array, arange, zeros
import sys, os

fonts, font_dir = {}, "/usr/share/fonts"
for bdf in os.listdir(font_dir):
    fonts[os.path.splitext(bdf)[0]] = reader.read_bdf(open(os.path.join(font_dir, bdf)))

# Decorator to replace a string by the font with that name
font_argument = lambda func: (lambda f,*a,**k: func(fonts.get(f,f),*a,**k))

@font_argument
def get_glyph(font, char):
    g = font.glyphs_by_codepoint[ord(char)]
    pixels = (array(g.data)[::-1,None] & (1 << arange(g.bbW-1,-1,-1))).astype('bool')
    return pixels

@font_argument
def get_row(font, string):
    glyphs = [get_glyph(font, char) for char in string]
    heights, widths = zip(*[glyph.shape for glyph in glyphs])
    pixels = zeros((max(heights), sum(widths) + len(string) - 1), 'bool')
    for i, (glyph, h, w) in enumerate(zip(glyphs, heights, widths)):
        y, x = 0, sum(widths[:i])
        pixels[y:y+h, x+i:x+i+w] = glyph
    return pixels

def display(pixels):
    for row in pixels:
        for pixel in row:
            sys.stdout.write('@' if pixel else ' ')
        sys.stdout.write('\n')
