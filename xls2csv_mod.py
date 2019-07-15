# -*- coding:utf-8 -*-

# Stéphane JEANNENOT
# Date : 22 septembre 2009
# Special >MOD< for FREMM

import sys
import os
import codecs
import warnings
from optparse import OptionParser

# External module for Excel conversion
import xlrd
# External module for legacy conversion
import xls2csv

def convert2csv_mod(options):
    if(options.sheetNamePattern != None):
        # Converting sheets whose name follow a name pattern
        wstr = """\n
        Trying to find sheets matching the given pattern "%s"
        Same options for all sheets (removing rows + colums,
        converting colums to integers, etc .... !!)
        Use at your own risks !!
        """%options.sheetNamePattern
        warnings.warn(wstr)

        options = xls2csv.manageOptions(options)
        WIN32 = True if (sys.platform == 'win32') else False
        if(options.lineend == "LF"):
            NIX = True
        else:
            NIX = False

        # Open input file
        if(options.inputEncoding):
            book = xlrd.open_workbook(filename=options.ifname, encoding_override=options.inputEncoding)
        else:
            book = xlrd.open_workbook(filename=options.ifname)

        # Open output file
        outfile = codecs.open(options.ofname, 'w', encoding=options.outputEncoding)

        #options.colasint = set()

        # Statistics
        nSheets = book.nsheets
        if(options.stats):
            print("\nStatistics of input Excel file :")
            print("... sheets found = %d" % nSheets)
            print("... encoding = %s" % book.encoding)

        if(options.numsheet >= nSheets or options.numsheet < 0):
            raise ValueError

        # Local copy
        remrows_local = list(options.remrows)
        remcols_local = list(options.remcols)
        filename = os.path.basename(options.ifname)
        for name in book.sheet_names():
            if( name.find(options.sheetNamePattern)!=-1 ):
                print("-> Converting %s"%name)
                wSheet = book.sheet_by_name(name)

                # --DEBUG -- Remove this !
                #outfile.write("\n\n---------- SHEET '%s' ----------\n\n"%name)

                # Handle negative indexes for removing rows and colums
                options.remrows = set([i if i>=0 else (wSheet.nrows+i) for i in remrows_local])
                options.remcols = set([i if i>=0 else (wSheet.ncols+i) for i in remcols_local])
                # Doing the conversion
                for data in xls2csv.convertFactory(options,wSheet):
                    chaine = ((options.separator).join(data)).rstrip(options.separator)
                    chaine = chaine.replace("\n", "")
                    chaine = chaine.replace(" ", "")

                    # fin des traitements pour fichiers xls de FREMM !!
                    # (commentaires après la ligne END -> remrows insuffisant)
                    # => sortie de la boucle de conversion
                    if(chaine[:3].upper()=="END"):
                        break
                    if(chaine[:1]==""):
                        continue

                    if(filename[:filename.find("_")] in options.red):
                        chaine = "R" + chaine

                    chaine = "%s%s%s%s%s"%(chaine[:chaine.find(";")],options.separator,chaine,options.separator,name)

                    #chaine = "%s%s%s"%(chaine[:chaine.find(";")],options.separator,chaine)




                    outfile.write(chaine)
                    if(NIX):
                        outfile.write("\n")
                    else:
                        outfile.write("\r\n")
        outfile.close()
    else:
        # legacy conversion, as usual
        xls2csv.convert2csv(options)


def main():
    if(sys.version_info[0] > 2):
        print("Found Python interpreter : %s\n"%sys.version)
        print("This script works only with Python version up to 2.x *but* not with an above version (xlrd module limitation)")
        sys.exit(1)
    else:
        parser = OptionParser(usage="%prog -i <IFNAME> -o <OFNAME>", version="%prog <MOD for DCNS>")
        parser.add_option("-i", "--input", dest="ifname",
                            help="input Excel filename")
        parser.add_option("-o", "--output", dest="ofname",
                            help="output CSV filename")
        parser.add_option("-s", "--sheet", dest="numsheet", type="int", default=0,
                            help="sheet number to convert (1st sheet is numbered '0', so it's 0 by default)")
        parser.add_option("--sheet-name-pattern", dest="sheetNamePattern", default=None,
                            help="(EXPERIMENTAL) convert sheets where the given substring matches their names \
                            WARNING : overwrite option --sheet option")
        parser.add_option("-p", "--sep", dest="separator", default=";",
                            help="separator used in the csv file (';' as Excel default conversion character)")
        parser.add_option("--input-encoding", dest="inputEncoding",
                            help="override the input file encoding (useful for excel 95 and earlier versions)")
        parser.add_option("--output-encoding", dest="outputEncoding", default="utf-8",
                            help="set the output file encoding (utf-8 by default)")
        parser.add_option("--col-as-int", dest="colasint",
                            help="give column numbers as a list with ':' as separator, like 1:25:41 or 'all' for converting all colums \
                            For these columns, if the cell contains a number, it will be considered as an integer")
        parser.add_option("--red", dest="red", default="",
                            help="name of Bigramme as a list with ':' as separator")
        parser.add_option("--remove-rows", dest="remrows",
                            help="give row numbers to remove as a list with ':' as separator, like 2:3:56")
        parser.add_option("--remove-cols", dest="remcols",
                            help="give column numbers to remove as a list with ':' as separator, like 6:89:7")
        parser.add_option("--lineend", dest="lineend", default="LF",
                            help="character for line ending : CRLF (windows) or LF (unix) default")
        parser.add_option("--stats", action="store_true", dest="stats", default=False,
                            help="print statistics about the Excel file")
        parser.add_option("-q", "--quiet",
                          action="store_false", dest="verbose", default=True,
                          help="don't print status messages to stdout")

        (options, args) = parser.parse_args()

        if( (not options.ifname) or (not options.ofname) ):
            parser.error("options -i and -o are mandatory")

        convert2csv_mod(options)

if __name__ == "__main__":
    main()
