# get_by_author
A script that accepts a file of author names and prints out the collective papers of these authors. non-redundant. I.e. of two or more authors collaborated on a paper, that paper will appear only once. The script uses Biopython's Entrez until to get the papers from the PubMed database. Other manuscript repositories are currently not supported.

## Prerequisites
* Python >3.6
* Biopython  https://biopython.org

## Installation
Download get_by_author.py

## Running
Example
```
python get_by_author.py --email="idoerg@iastate.edu" --years 2015 2021 --outfile="my_refs.txt", --affil="Iowa State University"
```

## Arguments
* ```-n, --names``` list of names
* ``` -i, --infile``` if more htan one person, they need to be in a file
* ``` -m, --email ``` user email. Required by NCBI and therefore required. The author of this software couldn't care less about your email address.
* ```-y,  --years```  year range. E.g. ```--years 2007 2020``` will filter by papers published in those years only. Default: 1930 until the current year.
* ```-o,  --outfile``` output file. Optional. Default: screen output.
* ```-a,  --affil``` Institutional affiliation. Optional, but highly recpommended if this script is used to generate publication lists for departmental reviews.
*  ```-h, --help``` prints help screen and exits


