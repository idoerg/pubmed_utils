#!/usr/bin/env python

# Copyright (C) 2021 Iddo Friedberg
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from Bio import Entrez, Medline
from datetime import datetime
import csv
import sys
import argparse
import re

YEAR = re.compile("(19|20)[0-9][0-9]") 

def get_by_author(name, affiliation):
    """
    
    Accepts an author name and (optional) institutional affiliation.  Returns
    all the papers for which they are a co-author, maximum 300. 

    The pubmed IDs are returned as a set. This is to avoid duplicatoins with
    other oauthors: if a paper was authored by 2 authors, it will only count
    once

    """

    if not affiliation:
        handle = Entrez.esearch(db="pubmed", 
            term=f"{name}[AU]",retmax=300)
    else:
        handle = Entrez.esearch(db="pubmed", 
                term=f"{name}[AU] AND {affiliation}[AD]",retmax=300)
    record = Entrez.read(handle)
    handle.close()
    id_set = set(record['IdList'])
    return id_set

def get_all_pubmed_ids(author_list, affiliation):
    """
    Get all the pubmed IDs of all authors. The pubmed IDs are collected as
    a set to avoid duplications: if 2 authors authored the same paper, it
    will only be counted once.

    """

    full_id_set = set()
    for author in author_list:
        id_set = get_by_author(author, affiliation)
        full_id_set = full_id_set.union(id_set)
        
    return full_id_set

def get_papers_by_ids(id_set):
    """
    Receives a set of pubmed IDs, returns a list of paper records in
    Medline format.
    """

    handle = Entrez.efetch(db="pubmed", id=list(id_set), rettype="medline",
                           retmode="text")
    paper_list = list(Medline.parse(handle))
    return paper_list

def include_this_paper(paper_rec,exclude_list):
    
    """
    If the user supplied a list of journals to exclude, this function is
    called. A simple string match between the source field in the paper and
    the list of excluded journals.

    """

    for i in exclude_list:
        if i.lower() in paper_rec['SO'].lower():
            return False
    return True

def prep_bibliography(paper_list,exclude_list):
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
        # year = int(paper_rec['DP'][:4])
        year = get_paper_year(paper_rec)
        source = paper_rec['SO']
        if include_this_paper(paper_rec,exclude_list):
            printrec = f"{au_string}\n{title}\n{source}\n//\n"
            printlist.append((year,printrec))
    return(printlist)

def in_year_range(paper_rec,year_range):
    retval = False
    pub_year = get_paper_year(paper_rec)
    if pub_year in year_range:
        retval = True
    return retval

def get_paper_year(paper_rec):
    pub_year = 0
    pyear_found = YEAR.search(paper_rec['DP'])
    if not pyear_found:
        sys.stdout.write(
        f"Could not find publication year for {paper_rec['TI']}\n{paper_rec['SO']}\n{paper_rec['DP']}\n")
    else:
        pub_year = int(pyear_found.group())
    return pub_year


def main(author_list, email, years, 
         affiliation,exclude_file,datesort="F",outfile=None):
    Entrez.email = email
    year_range = range(years[0],years[1]+1)
    exclude_list = []
    print(author_list)
    pubmed_ids = get_all_pubmed_ids(author_list, affiliation)
    print(pubmed_ids)
    paper_list = get_papers_by_ids(pubmed_ids)
    papers_in_year = []
    for paper in paper_list:
        if in_year_range(paper, year_range):
            papers_in_year.append(paper)
    if exclude_file:
        exclude_list = [i.strip() for i in exclude_file.readlines()]
    print(f"excluding: {exclude_list}")
    printlist = prep_bibliography(papers_in_year,exclude_list)
    printlist.sort()
    if datesort[0].upper() == 'R':
        printlist.reverse()
    for i in printlist:
        print(i[1],file=outfile)


def author_file_to_list(author_file):
    author_list = []
    author_reader = csv.reader(author_file,delimiter='\t')
    for inline in author_reader:
        author = f"{inline[1]} {inline[0][0]}{inline[2]}"
        author_list.append(author)
    return author_list

if __name__ == '__main__':

    print("""
    paperchaser  Copyright (C) 2021  Iddo Friedberg 
    This program comes with ABSOLUTELY NO WARRANTY. 
    This is free software, and you are welcome to redistribute it
    under certain conditions. See the GNU General Public License 
    for more details:
    <https://www.gnu.org/licenses/gpl-3.0.txt>
    """)
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n','--names',nargs='+',default=None)
    group.add_argument('-i','--infile',nargs='?',type=argparse.FileType('r'),
                       help="""file with author names. Format:
                       firstname<tab>lastname<tab>initial""",
                        default=None)

    parser.add_argument('-o','--outfile',nargs='?',type=argparse.FileType('w'),
                        default=sys.stdout)
    parser.add_argument('-m','--email',required=True,
                        help="A valid email is required by Entrez")
    parser.add_argument('-a','--affil',
                       help="Institutional affiliation")
    parser.add_argument('-y','--years',nargs=2,type=int,
                        default=[1930, int(datetime.now().year)],
                        help="Two years for publication year range. Earliest is 1930, latest is one year in the future")
    parser.add_argument('-s','--datesort',
                        choices=['[Ff]orward','[Rr]everse'],
                        default='forward',
                        help="Sort by publication year. Default: forward (ascending) publication year.")
    parser.add_argument('-e','--exclude',nargs='?',
                        type=argparse.FileType('r'), default=None,
                        help="Journal titles to exclude")

    args = parser.parse_args()
    # Check year range is good. Nothing before 1930 or after a year in the future.
    args.years.sort()
    if args.years[0] < 1930 or args.years[1] > int(datetime.now().year)+1:
        raise ValueError(f'Bad year range {args.years[0]}, {args.years[1]}')
    # Check validity of email addresss
    if not re.match('^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,}$',args.email):
        raise ValueError(f'Invalid email address {args.email}')
    print(args.infile)
    print(args.names)
    print(args.years)
    if args.infile:
        author_list = author_file_to_list(args.infile)
    else:
        author_list = args.names
    main(author_list, args.email, args.years, args.affil, args.exclude, args.datesort, args.outfile)


