# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 00:20:48 2016

@author: patrizio
"""

import glob 
from os.path import basename

from WiktionaryDownloadResources import WiktionaryDownloadResources, EXT_FILE_WIKTIONARY
from WiktionaryExtractor import WiktionaryExtractor

class WiktionaryWords:
    def __init__ (self, workingFolder, csv=None):
        self.workingFolder = workingFolder
        self.csv = csv or 'Trad.csv'
        
        #WiktionaryDownloadResources().DownloadResources()

        for resource in glob.iglob (self.workingFolder+'*' +'wiktionary'):
            print (resource)
            lang = basename(resource)
            lang = lang[:lang.index('.')]
            print ("processing:", resource, "lang:", lang)
            WiktionaryExtractor(lang, resource, self.csv).Extraction()
        print ("process completed")
    
if __name__ == '__main__':
    a=WiktionaryWords('/home/patrizio/Documenti/CiMEC/Multilingual_Vectors/wiktionary/')
    