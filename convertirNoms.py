# -*- coding:utf-8 -*-

import os
import sys
import warnings
import datetime
import codecs

from optparse import OptionParser


def convertir(options):
    WIN32 = True if (sys.platform == 'win32') else False
    if(options.verbose):
        pass

    if(options.lineend not in ["CRLF","LF"]):
        options.lineend = "LF"

    if(options.lineend == "LF"):
        NIX = True
    else:
        NIX = False

    # initialiser le dico avec le fichier de règles
    listRules = []
    fHandle = open(options.rules, 'r')
    fEnum = enumerate(fHandle)
    for line in fEnum :
        listRules.append( line[1].split(';')[:2] )
    #print(listRules)
    fHandle.close()

    #conversion
    fHandleI = open(options.ifname, 'r')
    fHandleO = open(options.ofname, 'w')

    fEnum = enumerate(fHandleI)
    for line in fEnum :
        liste = line[1].split(';')
        if(len(liste)>30):
            addr = liste[30]
            addr = addr.replace("172.","10.")
            liste[30]=addr
        mnemo = liste[0]
        for rule in listRules:
            #print("Applying rule : '%s' -> '%s'"%(rule[0],rule[1]))
            #print("... before %s"%mnemo)
			if (mnemo == rule[0]) :
				mnemo = mnemo.replace(rule[0],rule[1])
            #print("... after %s\n"%mnemo)
        liste[0]=mnemo
        #liste.insert(0,mnemo)
        fHandleO.write(";".join(liste))
    fHandleO.close()
    fHandleI.close()

def main():
    if(sys.version_info[0] > 2):
        print("Found Python interpreter : %s\n"%sys.version)
        print("This script works only with Python version up to 2 *but* not with an above version")
        sys.exit(1)
    else:
        parser = OptionParser(usage="%prog -i <IFNAME> -o <OFNAME>", version="%prog 0.1")
        parser.add_option("-i", "--input", dest="ifname",
                            help="input dci en csv")
        parser.add_option("-o", "--output", dest="ofname",
                            help="output Dci en csv avec mnemos courts")
        parser.add_option("-r", "--rules", dest="rules",
                            help="Nom du fichier de regles")
        parser.add_option("--lineend", dest="lineend", default="LF",
                            help="character for line ending : CRLF (windows) or LF (unix) default")
        parser.add_option("-q", "--quiet",
                          action="store_false", dest="verbose", default=True,
                          help="don't print status messages to stdout")

        (options, args) = parser.parse_args()

        if( (not options.ifname) or (not options.ofname) or(not options.rules)):
            parser.error("options -i and -o and -r are mandatory")

        convertir(options)

if __name__ == "__main__":
    main()

