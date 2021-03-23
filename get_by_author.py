
from Bio import Entrez, Medline
import csv
import sys
from datetime import datetime

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

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

def in_year(paper_rec,year_range):
    retval = False
    pub_year = int(paper_rec['DP'][:4])
    if pub_year in year_range:
        retval = True
    return retval



def main(author_file, email="idoerg@iastate.edu", 
         years_back=4, affiliation="Iowa State University"):
    Entrez.email = email

    thisyear = int(datetime.now().year)
    year_range = range(thisyear-years_back, thisyear+1)
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
        if in_year(paper, year_range):
            papers_in_year.append(paper)
    printlist = prep_bibliography(papers_in_year)
    for i in printlist:
        print(i)

if __name__ == '__main__':
    main(sys.argv[1])




