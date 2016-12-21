# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 10:17:33 2016

@author: patrizio
"""

import os
import re


TAG_START_PAGE='<page>'
TAG_END_PAGE='</page>'

TAG_START_TITLE='<title>'
TAG_END_TITLE='</title>'

TAG_START_TRAD = '{{-trad-}}'

TAG_START_LANG = ':*{{'
TAG_END_LANG = '}}:'

PATTERN_TRAD = re.compile ('(\[\[.*\]\])?')

HYPER_FILTER = re.compile ('\]\].*\(')
HYPER_FILTER_FINE = re.compile ('\]\].*\[\[')

SEP_CSV = '\t'

# NOT USED
#TAG_SYLLABLE = '{{-sill-}}'
#TAG_PRONUNCIATION = '{{-pron-}}'
#TAG_ETIMOLOGY = '{{-etim-}}'
#TAG_SINONYM = '{{-sin-}}'
#
#TAG_DER = '{{-der-}}'
#TAG_ALTER = '{{-alter-}}'
#TAG_PROV = '{{-prov-}}'
#TRADUZ_END_TAG='{{-ref-}}'

class WiktionaryExtractor:    
    def __init__ (self, lang=None, corpus=None, csv=None):
        
        self.basepath = '/home/patrizio/Documenti/CiMEC/Multilingual_Vectors/wiktionary'
        self.corpus = corpus or self.basepath + os.sep + 'itwiki'
        self.csv = csv or self.basepath + os.sep + "traduzioni.csv"        
        self.lang = lang or 'it'
        
        self.exclude_Tags = [':', '|', '#', ';']
        
    def Extraction (self):
        """
            This method extract data from a wiktionary corpus
        
        
            return 
            
            
            
              <page>
                  <title>MediaWiki:Category</title>
        """
        with open(self.corpus, 'r') as f:
            line = True
            while line:
                line = f.readline()
                if TAG_START_PAGE in line:
                    line = f.readline()
                    if ':' not in line:
                        #valid page
                        word = line[line.index(TAG_START_TITLE) + len(TAG_START_TITLE):line.index(TAG_END_TITLE)]                         
                        #loop until found start tag
                        while TAG_START_TRAD not in line and TAG_END_PAGE not in line:
                            line = f.readline ()
#                        print (line)
                        if TAG_END_PAGE in line:
                            continue
                        #Now start extracting traductions
                        while line.strip() != '':
                            if line.startswith(TAG_START_LANG) and TAG_END_LANG in line:
                                lang = line[len(TAG_START_LANG):line.index(TAG_END_LANG)]
                                if '|' in lang:
                                    lang = lang[:lang.index('|')]
                                #first hyper filter
                                line = re.sub(HYPER_FILTER,']]',line)
                                #traductions extraction
                                trad = [t[2:-2] for l in line.split(',') for t in re.findall(PATTERN_TRAD, l) if len(t.split()) > 0]
                                #fine filter
                                traductions = []
                                for t in trad:                                
                                    if t.startswith('[['):
                                        t = t[2:]
                                    if ']]' in t:
                                        while ']]' in t and '[[' in t:
                                            traductions.append(t[:t.index(']]')])
                                            t = t[t.index('[[')+2:]
                                        if ']]' in t:
                                            traductions.append(t[:t.index(']]')])
                                        elif '[[' in t:
                                            traductions.append(t[t.index('[[')+2:])
                                        else:
                                            traductions.append(t)
                                    else:
                                        traductions.append(t)         
                                #clear non-traductions
                                for t in traductions:
                                    for exclude in self.exclude_Tags :
                                        if exclude in t:
                                            traductions.remove(t)
                                            break
                                print (word, self.lang, lang, traductions)
                                with open(self.csv, 'a') as csv:
                                    for t in traductions:
                                        if len(t.strip()) > 0:
                                            line = ''.join([self.lang, SEP_CSV, word, SEP_CSV, lang, SEP_CSV, t]) + '\n'
                                            csv.write (line)
                            line = f.readline ()
                        continue

if __name__ == '__main__':
    print ("DEMO MODE")
    a=WiktionaryExtractor()
    a.Extraction()                
                
            