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
python get_by_author.py 
```

## Arguments

* ``` -m, --email ``` user email. Required by NCBI. The author of this software couldn't care less about your email.
* ```-y,  --years```  year range. E.g. ```--years 2007 2020``` will filter by papers published in those years only. Default: 1930 until the current year.
* ```-o,  --outfile``` output file. Optional. Default: screen output.
* ```-a,  --affil``` Institutional affiliation. Optional, but highly recpommended if this script is used to generate publicaiton lists for departmental reviews.
*  ```-h, --help``` prints help screen and exits


