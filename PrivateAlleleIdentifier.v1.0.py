##########################################################
### Import Necessary Modules #############################

import argparse                       #provides options at the command line
import sys                            #take command line arguments and uses it in the script
import gzip                           #allows gzipped files to be read
import re                             #allows regular expressions to be used

##########################################################
### Command-line Arguments ###############################

parser = argparse.ArgumentParser(description="A script to identify SNPs that have alleles private to a population.")
parser.add_argument("-vcf", help = "The location of the vcf file", default=sys.stdin, required=True)
parser.add_argument("-pop", help = "The location of the population file (IndividualName<tab>IndivdualPopulation per line)", default=sys.stdin, required=True)
parser.add_argument("-min", help = "The minimum number of individuals with the private allele in a population, default=1", default=1)
args = parser.parse_args()

#########################################################
###Variables ############################################

class Variables():
   population = {}
   populations = []
   numIndividuals = 0

#########################################################
### Body of script ######################################

class OpenFile():
    def __init__ (self, f, typ, occ):
        """Opens a file (gzipped) accepted"""
        if re.search(".gz$", f):
            self.filename = gzip.open(f, 'rb')
        else:
            self.filename = open(f, 'r') 
        if typ == "vcf":
            sys.stderr.write("\nOpened vcf file: {}\n".format(occ))
            OpenVcf(self.filename,occ)
        elif typ == "pop":
            sys.stderr.write("\nOpened pop file: {}\n".format(occ))
            OpenPop(self.filename,occ)

class OpenVcf():
    def __init__ (self,f,o):
        """Reads a vcf file to identify private alleles"""
        self.numMarkers = 0
        self.privateMarkers = {}
        self.individuals = []   
        for self.line in f:
            ### Allows gzipped files to be read ###
            try:
                self.line = self.line.decode('utf-8')
            except:
                pass          
            if not re.search("^#", self.line):
                self.chr, self.pos, self.id, self.ref, self.alt, self.qual, self.filt, self.info, self.fmt = self.line.split()[0:9]
                self.individualGenotypes = self.line.split()[9:]
                self.numMarkers += 1
                self.privateTest = {}
                self.privateTest["0"] = {}
                self.privateTest["1"] = {}
                for self.position, self.indGeno in enumerate(self.individualGenotypes):
                    self.indName = self.individuals[self.position]
                    try:
                        self.indPop = Variables.population[self.indName]
                    except:
                        continue
                    self.indGeno = self.indGeno.split(":")[0].split("/")
                    if self.indGeno[0] == "." or self.indGeno[1] == ".":
                        continue
                    if int(self.indGeno[0]) == 0 or int(self.indGeno[1]) == 0:
                        if self.indPop in self.privateTest["0"]:
                            self.privateTest["0"][self.indPop] += 1
                        else:
                            self.privateTest["0"][self.indPop] = 1
                    if int(self.indGeno[0]) == 1 or int(self.indGeno[1]) == 1:
                        if self.indPop in self.privateTest["1"]:
                            self.privateTest["1"][self.indPop] += 1
                        else:
                            self.privateTest["1"][self.indPop] = 1
                if len(self.privateTest["0"].keys()) == 1:
                    for self.pop in self.privateTest["0"]:
                        if int(self.privateTest["0"][self.pop]) >= int(args.min):
                            print ("{}\t{}\t{}\t{}".format(self.chr, self.pos, self.pop, self.privateTest["0"][self.pop]))
                elif len(self.privateTest["1"].keys()) == 1:
                    for self.pop in self.privateTest["1"]:
                        if int(self.privateTest["1"][self.pop]) >= int(args.min):
                            print ("{}\t{}\t{}\t{}".format(self.chr, self.pos, self.pop, self.privateTest["1"][self.pop]))                                                                    
            elif re.search("^#CHROM", self.line):
                self.individuals = self.line.split()[9:]
                self.numInds = len(self.individuals)
                if int(self.numInds)  != int(Variables.numIndividuals):
                    sys.stderr.write("Warning, population and vcf files have different number of individuals.\n")
        f.close()
        
class OpenPop():
    def __init__ (self,f,o):
        """Reads a population file to identify which individual goes to which population"""
        self.pops = {}
        for self.line in f:
            ### Allows gzipped files to be read ###
            try:
                self.line = self.line.decode('utf-8')
            except:
                pass          
            if not re.search("^#", self.line):
                self.individual, self.pop = self.line.split()
                if self.individual in Variables.population:
                    sys.stderr.write("\tWarning: {} already defined for population {}, replacing with population {}\n\n".format(self.individual, Variables.population[self.individual], self.pop))
                Variables.population[self.individual] = self.pop
                if self.pop in self.pops:
                    self.pops[self.pop] += 1
                else:
                    self.pops[self.pop] = 1
                Variables.numIndividuals += 1
        for self.pop in sorted(self.pops):
            Variables.populations.append(self.pop)
            sys.stderr.write("\tIdentified population {} with {} samples\n".format(self.pop, self.pops[self.pop]))
        f.close()

### Order of script ####
if __name__ == '__main__':
    Variables()
    open_aln = OpenFile(args.pop, "pop", args.pop)
    open_aln = OpenFile(args.vcf, "vcf", args.vcf)
