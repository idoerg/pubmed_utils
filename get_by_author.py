#!/usr/bin/env python

from Bio import Entrez, Medline
from datetime import datetime
import csv
import sys
import argparse
import re

def get_by_author(name, affiliation):
    handle = Entrez.esearch(db="pubmed", 
            term=f"{name}[AU] AND {affiliation}[AD]",retmax=100)
    record = Entrez.read(handle)
    handle.close()
    id_set = set(record['IdList'])
    return id_set

def get_all_pubmed_ids(author_list, affiliation):
    full_id_set = set()
    for author in author_list:
        id_set = get_by_author(author, affiliation)
        full_id_set = full_id_set.union(id_set)
        
    return full_id_set

def get_papers_by_ids(id_set):
    handle = Entrez.efetch(db="pubmed", id=list(id_set), rettype="medline",
                           retmode="text")
    paper_list = list(Medline.parse(handle))
    return paper_list

def prep_bibliography(paper_list):
    au_string = ''
    printlist = []
    for paper_rec in paper_list:
        au_string = ''
        for author in paper_rec['AU']:
            au_string += f"{author}, "
        # remove last comma and space from author list 
        au_string = au_string[:-2]
        title = paper_rec['TI']
        journal = paper_rec['JT']
        journal_abbr = paper_rec['TA']
        # date = paper_rec['DP']
        source = paper_rec['SO']
        printrec = f"{au_string}\n{title}\n{source}\n//\n"
        printlist.append(printrec)
    return(printlist)

def in_year_range(paper_rec,year_range):
    retval = False
    pub_year = int(paper_rec['DP'][:4])
    if pub_year in year_range:
        retval = True
    return retval



def main(author_file, email, years, 
         affiliation="Iowa State University",outfile=None):
    Entrez.email = email
    if years:
        year_range = range(years[0], years[1]+1)
    else:
        year_range = range(1930, int(datetime.now().year))
    author_list = []
    with open(author_file) as in_authors:
        author_reader = csv.reader(in_authors,delimiter='\t')
        for inline in author_reader:
            author = f"{inline[0]} {inline[1]}"
            author_list.append(author)
    pubmed_ids = get_all_pubmed_ids(author_list, affiliation)
    paper_list = get_papers_by_ids(pubmed_ids)
    papers_in_year = []
    for paper in paper_list:
        if in_year_range(paper, year_range):
            papers_in_year.append(paper)
    printlist = prep_bibliography(papers_in_year)
    if outfile:
        with open(outfile,'w') as f:
            for i in printlist:
                print(i,f)
        f.close()
    else:
        for i in printlist:
            print(i)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('-o','--outfile')
    parser.add_argument('-m','--email',required=True)
    parser.add_argument('-a','--affil',default="Iowa State University")
    parser.add_argument('-y','--years',nargs=2,type=int)
    args = parser.parse_args()
    if args.years:
        args.years.sort()
        if args.years[0] < 1930 or args.years[1] > int(datetime.now().year):
            raise ValueError(f'Bad year range {args.years[0]}, {args.years[1]}')
    if not re.match('^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,}$',args.email):
        raise ValueError(f'Invalid email address {args.email}')
    main(args.infile, args.email, args.years, args.affil,args.outfile)


