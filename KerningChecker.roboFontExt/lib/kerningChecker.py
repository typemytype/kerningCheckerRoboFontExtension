import os

import vanilla

from mojo.events import addObserver

# taken from https://github.com/adobe-type-tools/kern-dump
from getKerningPairsFromOTF import ReadKerning
from getKerningPairsFromUFO import UFOkernReader


class KerningChecker(object):

    def __init__(self):
        addObserver(self, "fontDidGenerate", "fontDidGenerate")

    def dict_diff(self, dict_a, dict_b):
        return dict([
            (key, dict_b.get(key, dict_a.get(key)))
            for key in set(dict_a.keys()+dict_b.keys())
            if (
                (key in dict_a and (not key in dict_b or dict_a[key] != dict_b[key])) or
                (key in dict_b and (not key in dict_a or dict_a[key] != dict_b[key]))
            )
        ])

    def fontDidGenerate(self, notification):
        font = notification["font"]
        path = notification["path"]
        format = notification["format"]
        if format not in ("otf", "ttf"):
            return
        if not os.path.exists(path):
            return

        binaryKerning = ReadKerning(path)
        ufoKerning = UFOkernReader(font)

        ufoPairs = ufoKerning.allKerningPairs
        binaryPairs = binaryKerning.kerningPairs

        if ufoKerning.allKerningPairs != binaryKerning.kerningPairs:
            #creates a diff of binary pairs vs UFO pairs
            diff = self.dict_diff(ufoPairs, binaryPairs)
            
            output = 'Hey, you have ' + str(len(diff)) ' missing kerning pairs:\n' + str(diff)
            #prints to output window
            print output
            #displays in dialog. Should this be limited somehow if it is really long? 
            vanilla.dialogs.message(output)

            #vanilla.dialogs.message("Kerning Checker", "Hey, you have kerning within your OT features. The output might not be what you expect!")

KerningChecker()
