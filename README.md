# paper_chaser
A script that accepts a file of author names and prints out the collective papers of these authors. non-redundant. I.e. of two or more authors collaborated on a paper, that paper will appear only once. The script uses Biopython's Entrez until to get the papers from the PubMed database. Other manuscript repositories are currently not supported.

## Prerequisites
* Python >3.6
* Biopython  https://biopython.org

## Installation
Download get_by_author.py

## Running
Example
```
python paper_chaser.py -n "Iddo Friedberg" --email="your_email_here" --years 2015 2021 --outfile="my_refs.txt" --affil="Iowa State University"
```

## Arguments
* ```-n, --names``` list of names
* ``` -i, --infile``` if more than one author, it is preferable to read in from a file.
* ``` -m, --email ``` user email. Required by NCBI and therefore required. The author of this software couldn't care less about your email address.
* ```-y,  --years```  year range. E.g. ```--years 2007 2020``` will filter by papers published in those years only. Default: 1930 until the current year.
* ```-o,  --outfile``` output file. Optional. Default: screen output.
* ```-s, --datesort {f,F,r,R,forward,reverse}``` sort by date, [f]orward or [r]everse. Default: forward
* ```-a,  --affil``` Institutional affiliation. Optional, but highly recommended if this script is used to generate publication lists for departmental reviews.
*  ```-e, --exclude``` a file that contains titles of journals to exclude, one per line
*  ```-h, --help``` prints help screen and exits

## Author file format
Firstname\<tab\>LastName\<tab\>Initial


