import os

import vanilla

from mojo.events import addObserver

# taken from https://github.com/adobe-type-tools/kern-dump
from getKerningPairsFromOTF import ReadKerning
from getKerningPairsFromUFO import UFOkernReader


class KerningChecker(object):

    def __init__(self):
        addObserver(self, "fontDidGenerate", "fontDidGenerate")

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

        if ufoKerning.allKerningPairs != binaryKerning.kerningPairs:
            vanilla.dialogs.message("Kerning Checker", u"Hey – you have kerning within your OT features. The output might not be what you expect!")

KerningChecker()
