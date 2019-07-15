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
    CompteurFichier=0
    CompteurLigne = 0
    ListeFichierSortie = options.ofname.split('.')
    NomFichier = "%s_%d.%s" %(ListeFichierSortie[0], CompteurFichier, ListeFichierSortie[1])
    fHandleO = open(NomFichier, 'w')
    for line in fHandleI :
        CompteurLigne=CompteurLigne+1
        fHandleO.write(line)
        if( CompteurLigne > int(options.length)) :
           fHandleO.close()
           CompteurLigne = 0
           CompteurFichier=CompteurFichier+1
           NomFichier = "%s_%d.%s" %(ListeFichierSortie[0], CompteurFichier, ListeFichierSortie[1])
           fHandleO = open(NomFichier, 'w')
  
    fHandleO.close()
    fHandleI.close()


def main():

    if(sys.version_info[0] > 2):
        print("Found Python interpreter : %s\n"%sys.version)
        print("This script works only with Python version up to 2 *but* not with an above version")
        sys.exit(1)
    else:
        parser = OptionParser(usage="%prog -i <IFNAME> -o <OFNAME> -l <LONGUEUR>", version="%prog 0.1")
        parser.add_option("-i", "--input", dest="ifname",
                            help="fichier entree")
        parser.add_option("-o", "--output", dest="ofname",
                            help="prefix fichier sortie")
        parser.add_option("-l", "--length", dest="length",
                            help="Nombre de lignes par fichier")
        (options, args) = parser.parse_args()
        if( (not options.ifname) or (not options.ofname) or (not options.length)):
            parser.error("options -i and -o and -l are mandatory")
        convertir(options)

if __name__ == "__main__":
    main()