import os
import sys
import warnings
import datetime
import codecs
import re

from optparse import OptionParser



def convertir(options):
    WIN32 = True if (sys.platform == 'win32') else False
    fHandleI = open(options.ifname, 'r')
    fEnum = enumerate(fHandleI)
    fHandleO = open(options.ofname, 'w')
    fHandleO2 = open(options.nfname, 'w')
    listMnemo = []

    for line in fEnum :
        liste = line[1].split(';')
        liste[0]+="_"
        out = "OBJETS;" + liste[0] + ";\n"
        fHandleO.write(out)
        out = "Valeur;Valeur;\n"
        fHandleO.write(out)
        out = "OBJETS;" + liste[0] + ";\n"        
        fHandleO2.write(out)
        out = "Valeur;ValeurForcee;\n"
        fHandleO2.write(out)
        out = "OBJETS;" + liste[0] + ";\n"        
        fHandleO2.write(out)
        out = "Valeur;Forcage;\n"
        fHandleO2.write(out)
        if liste[2] != "BOOL" :
            out = "OBJETS;" + liste[0] + ";\n"        
            fHandleO2.write(out)
            out = "Valeur;Derive;\n"
            fHandleO2.write(out)     
    fHandleO.close()
    fHandleO2.close()
    fHandleI.close()
def main():
    if(sys.version_info[0] > 2):
        print("Found Python interpreter : %s\n"%sys.version)
        print("This script works only with Python version up to 2 *but* not with an above version")
        sys.exit(1)
    else:
        parser = OptionParser(usage="%prog -i <IFNAME> -o <OFNAME> -n <OFNAME2>", version="%prog 0.1")
        parser.add_option("-i", "--input", dest="ifname",
                            help="fichier cs2")
        parser.add_option("-o", "--output", dest="ofname",
                            help="fichier de liens 1")
        parser.add_option("-n", "--noutput", dest="nfname",
                            help="fichier de liens 2")
        (options, args) = parser.parse_args()
        if( (not options.ifname) or (not options.ofname) or (not options.nfname)):
            parser.error("options -i and -o and -n are mandatory")

        convertir(options)

if __name__ == "__main__":
    main()
