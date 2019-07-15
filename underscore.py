import os
import sys
import warnings
import datetime
import codecs
import re

from optparse import OptionParser



def convertir(options):
    WIN32 = True if (sys.platform == 'win32') else False
    if (options.exprtoremove):
        p = re.compile(options.exprtoremove)
    #conversion
    fHandleI = open(options.ifname, 'r')
    fEnum = enumerate(fHandleI)
    fHandleO = open(options.ofname, 'w')
    listMnemo = []

    if(options.prefix == None):
        prefix="_"
    else:
        prefix=options.prefix
    for line in fEnum :
        liste = line[1].split(';')
        if(options.exprtoremove):
            if(not p.match(liste[0])) :
                liste[0]+=prefix
                liste[1]+=prefix
                listMnemo.append(liste)
        else :
            liste[0]+=prefix
            liste[1]+=prefix
            listMnemo.append(liste)
    listMnemo.sort(lambda a,b : cmp(len(b[0]),len(a[0])))
    for Mnemo in listMnemo :
        fHandleO.write(";".join(Mnemo))
    
    fHandleO.close()
    fHandleI.close()
def main():
    if(sys.version_info[0] > 2):
        print("Found Python interpreter : %s\n"%sys.version)
        print("This script works only with Python version up to 2 *but* not with an above version")
        sys.exit(1)
    else:
        parser = OptionParser(usage="%prog -i <IFNAME> -o <OFNAME> -r <REGEXP> -p <PREFIX>", version="%prog 0.1")
        parser.add_option("-i", "--input", dest="ifname",
                            help="input dci en csv")
        parser.add_option("-o", "--output", dest="ofname",
                            help="output Dci en csv avec mnemos courts")
        parser.add_option("-r", "--remove", dest="exprtoremove",
                            help="Suppresion des mnemoniques inutile")
        parser.add_option("-p", "--prefix", dest="prefix",
                            help="sans ajout underscore")
        (options, args) = parser.parse_args()
        if( (not options.ifname) or (not options.ofname)):
            parser.error("options -i and -o are mandatory")

        convertir(options)

if __name__ == "__main__":
    main()