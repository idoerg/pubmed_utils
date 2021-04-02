# paperchaser
A script that accepts a file of author names and prints out the collective papers of these authors. No duplicaitons, i.e. of two or more authors collaborated on a paper, that paper will appear only once. The script uses Biopython's Entrez utilities to get the papers from the PubMed database. Other manuscript repositories are not supported currently.

## Prerequisites
* Python >3.6
* Biopython  https://biopython.org

## Installation
Download paperchaser

## Running
Example. Note that this example will not run unless you replace the ```--email``` argument with a valid email address. 
```
python paperchaser -n "Iddo Friedberg" --email="your_email_here" --years 2015 2021 --outfile="my_refs.txt" --affil="Iowa State University"
```

## Arguments
* ```-n, --names``` list of authors, comma delimieted, blank separated. Example: -n "Joe Smith" "Jane Doe"
* ``` -i, --infile``` if more than one author, it is preferable to read them in from a file.
* ``` -m, --email ``` user email. Required by NCBI and therefore required. The author of this software couldn't care less about your email address.
* ```-y,  --years```  year range. E.g. ```--years 2007 2020``` will filter by papers published only between 2007 and 2020, inclusive. Default: 1930 until one year after the current year.
* ```-o,  --outfile``` output file. Optional. Default: screen output.
* ```-s, --datesort {f,F,r,R,forward,reverse}``` sort by date, [f]orward or [r]everse. Default: forward
* ```-a,  --affil``` Institutional affiliation. Optional, but highly recommended if this script is used to generate publication lists for departmental reviews.
*  ```-e, --exclude``` input filename. A file that contains titles of journals to exclude, one per line
*  ```-c, --conflicts``` output filename. Print the co-authors of all authors entered in -i or -n into this file
*  ```-h, --help``` prints help screen and exits

## Author file format
```Firstname\<tab\>LastName\<tab\>Initial```


