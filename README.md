# get_by_author
A script that accepts a file of author names and prints out the collective papers of these authors. non-redundant. I.e. of two or more authors collaborated on a paper, that paper will appear only once.

## Prerequisites
* Python >3.6
* Biopython  https://biopython.org

## Installation
Download get_by_author.py

## Running
```
python get_by_author.py 
```

## Arguments

* ```-y/--years```  year range. E.g. ```--years 2007 2020``` will filter by papers publisehd in those years only. Default: 1930 until the current yeat
* 
