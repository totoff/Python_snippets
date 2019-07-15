# -*- coding:utf-8 -*-

import os
import sys
import warnings
import datetime
import codecs
import glob

from optparse import OptionParser


def convertir(options):
    WIN32 = True if (sys.platform == 'win32') else False
    if(options.verbose):
        pass


    mnemoPresents = []
    indMax=0
    longueur_max=17

    if(os.path.exists(options.ofname)):
        fHandleO = open(options.ofname, 'r')
        if(fHandleO):
            fEnum = enumerate(fHandleO)
            for line in fEnum :
                liste = line[1].split(';')
                mnemoPresents.append(liste[0])
                indMax=int(liste[1][liste[1].rfind("_")+1:])
            fHandleO.close()

    fHandleO = open(options.ofname, 'a')
    mnemoListe = []

    fHandleI = open(options.ifname, "r")
    fileName = os.path.basename(options.ifname)
    prefix = fileName[:fileName.rfind("_")]
    fEnum = enumerate(fHandleI)
    if(options.longueur):
        longueur_max = options.longueur
    for line in fEnum :
        liste = line[1].split(';')
        if(len(liste[options.colonne]) > longueur_max ):
            if(liste[options.colonne] not in mnemoPresents and liste[options.colonne] not in mnemoListe):
                mnemoListe.append(liste[options.colonne])
                indMax = indMax+1
                fHandleO.write("%s;%s_%.5d;\n" %(liste[options.colonne], prefix, indMax))
    fHandleI.close()

    #traitement de la mnemoListe
    mnemoListe1 = list(set(mnemoListe))
    nb = len(mnemoListe) - len(mnemoListe1)
    print("---------- Mnemonique en double : %d --------------" %nb)



    fHandleO.close()

def main():
    if(sys.version_info[0] > 2):
        print("Found Python interpreter : %s\n"%sys.version)
        print("This script works only with Python version up to 2 *but* not with an above version")
        sys.exit(1)
    else:
        parser = OptionParser(usage="%prog -i <IFNAME> -o <OFNAME>", version="%prog 0.1")
        parser.add_option("-i", "--input", dest="ifname",
                            help="input cs1 filename")
        parser.add_option("-o", "--output", dest="ofname",
                            help="output conversion mnemos du fichier")
        parser.add_option("-c", "--colonne", dest="colonne", type="int",
                            help="output conversion mnemos du fichier")
        parser.add_option("-q", "--quiet",
                          action="store_false", dest="verbose", default=True,
                          help="don't print status messages to stdout")
        parser.add_option("-l", "--longueur", dest="longueur", type="int",
                            help="longueur d'un mnemonique a remplace")

        (options, args) = parser.parse_args()

        if( (not options.ifname) or (not options.ofname) or (not options.colonne)):
            parser.error("options -i and -o -c are mandatory")

        convertir(options)

if __name__ == "__main__":
    main()

