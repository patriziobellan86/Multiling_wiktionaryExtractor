# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 14:23:03 2016

@author: patrizio
"""

import os
from os.path import basename
import bz2
import re
import requests
import urllib.request
from urllib.parse import urljoin
from lxml import html

EXT_FILE_WIKTIONARY = '.wiktionary'

class WiktionaryDownloadResources:
    def __init__ (self, folder2save=None):
        self.extFile = '.xml.bz2'
        
        self.tagWiktionary = 'wiktionary'
        self.tagMultistream = '-pages-articles-multistream.xml.bz2'
        self.wikimediaPage = 'https://dumps.wikimedia.org/'        
        self.dumpBackupPage = self.wikimediaPage + 'backup-index.html'
        
        self.folder2save = folder2save or '/home/patrizio/Documenti/CiMEC/Multilingual_Vectors/wiktionary' 

    def DownloadResources (self):
        langs = self.ReadDump ()
        i = 1
        for lang in langs:
            print ("Processing", i, "resource on ", len(langs))
            self.SaveResourcePage(self.ReadLangResourcePage(self.ReadResourcesPage(lang)))
        print ("All the resources are downloaded")
        
        
    def ReadDump (self):
        with urllib.request.urlopen(self.dumpBackupPage) as response:
           dumpPage = response.read()
        dumpPage = html.fromstring(dumpPage)
        hrefs = [a.attrib['href'] for a in dumpPage.cssselect('a')]
        links = [urljoin(self.wikimediaPage, link) for link in hrefs if self.tagWiktionary in link]
        return links
        
    def ReadResourcesPage (self, link):
        lastDump = re.compile ('(\.\./\d/)')
        with urllib.request.urlopen(link) as response:
           dumpPage = response.read()
        dumpPage = html.fromstring(dumpPage)
        links = [a.attrib['href'] for a in dumpPage.cssselect('a')]
        for l in links:
            if l.startswith('../') and l.endswith('/'):
                l = link[:link.rindex('/')+1] + l[3:]
                return l
     
    def ReadLangResourcePage (self, link):
        with urllib.request.urlopen(link) as response:
           dumpPage = response.read()
        dumpPage = html.fromstring(dumpPage)
        links = [a.attrib['href'] for a in dumpPage.cssselect('a')]
        for l in links:         
            if l.endswith (self.tagMultistream):
                l = urljoin(self.wikimediaPage, l)
                print ("resource file", l)                
                return l

    def SaveResourcePage (self, link):
        filename = self.folder2save + os.sep + link [len(self.wikimediaPage):link.index(self.tagWiktionary)] + self.extFile
        print ("the file will be saved as ", filename)
        with open(filename, 'wb') as f:
            print("Downloading", link)
            data = requests.get(link).content
            f.write(data) 
        print ("Downloaded")
        self.DecompressResourceFile(filename)
        
        
    def DecompressResourceFile (self, filename):
        print ("decompressing:", filename)
        lang = basename(filename)
        dst = self.folder2save + os.sep + lang[:lang.index('.')] + EXT_FILE_WIKTIONARY
        print (filename, dst)
        
        with open(filename, 'rb') as source, open(dst, 'wb') as dest:
            dest.write(bz2.decompress(source.read()))  
        os.remove(filename)
        print ("process complete")
   
            
if __name__ == '__main__':
    print ("DEMO MODE")
    a = WiktionaryDownloadResources()

    langs = a.ReadDump ()
    a.SaveResourcePage(a.ReadLangResourcePage(a.ReadResourcesPage(langs[100])))