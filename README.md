# PrivateAllele
A script to identify private alleles between populations/groups

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#requirements">Requirements</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- requirements -->
## Requirements

This script has been tested with python 3.
The script requires the following files:

&nbsp;&nbsp;&nbsp;VCF file that you wish to identify private alleles from<br />
&nbsp;&nbsp;&nbsp;A population file with each line having the format: individual population<br />

<!-- usage -->
## Usage

1) Output the list of private alleles (format: Chromosome, position, population, private allele count in population):<br /><br />
&nbsp;&nbsp;&nbsp;python PrivateAlleleIdentifier.v1.0.py -vcf file.vcf.gz -pop population.txt > PrivateAlleles.txt<br /><br />
&nbsp;&nbsp;&nbsp;help (and further explanations): python PrivateAlleleIdentifier.v1.0.py -h

<!-- license -->
## License 

Distributed under the MIT License.
