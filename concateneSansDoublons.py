# -*- coding:utf-8 -*-

import os
import sys
import glob
from optparse import OptionParser

def concatene(options):

    os.chdir(options.workDir)

    #dico
    lDico = {}
    #fichier de sortie
    fHandleO = open(options.ofname, "w")
    lFileDoublons = "doublond"+options.ofname
    fHandleDoublons = open(lFileDoublons,"w")

    # liste des fichiers à concatener    
    listeFiles = glob.glob(options.pattern)
    listeMnemoGlobale = []
    for lFile in listeFiles:
        fHandle = open(lFile, "r")
        fEnum = enumerate(fHandle)
        for lLine in fEnum:
            liste = lLine[1].split(';')
            key = liste[0]
            listeMnemoGlobale.append(key)

            #la clé existe t-elle ?
            if(key not in lDico):
                #ecrire dans le fichier output
                fHandleO.write(lLine[1])
                lDico[key] = ["%s -> %d"%(lFile,lLine[0]+1)]
            else:
                #stockage des doublons
                lDico[key].append("%s -> %d"%(lFile,lLine[0]+1))

        fHandle.close()
    fHandleO.close()

    # verification (a priori inutile ...)
    s1 = set(listeMnemoGlobale) #suppression des doublons par construction de l'objet
    s2 = set(lDico.keys()) #clefs dico sont uniques => passage list -> set
    sdiff = s1.difference(s2)
    if(len(sdiff)>0):
        print(sdiff)
        raise ValueError
    
    for key in lDico:
        if(len(lDico[key])>1):
            fHandleDoublons.write("%s : found %d\n"%(key,len(lDico[key])))
            for item in lDico[key]:
                fHandleDoublons.write("... %s\n"%(item))
    fHandleDoublons.close()
        

def main():
    if(sys.version_info[0] > 2):
        print("Found Python interpreter : %s\n"%sys.version)
        print("This script works only with Python version up to 2 *but* not with an above version")
        sys.exit(1)
    else:
        parser = OptionParser(usage="%prog -w <WorkingDir> -p <Pattern> -o <OFNAME>", version="%prog 0.1")
        parser.add_option("-w", "--WorkingDir", dest="workDir",
                            help="chemin des fichiers à concaténer")
        parser.add_option("-o", "--output", dest="ofname",
                            help="nom de fichier à générer")
        parser.add_option("-p", "--Pattern", dest="pattern",
                            help="pattern des fichiers à concaténer")

        (options, args) = parser.parse_args()

        if( (not options.workDir) or (not options.ofname) or(not options.pattern)):
            parser.error("options -w and -p and -o are mandatory")

        concatene(options)

if __name__ == "__main__":
    main()

