import argparse, pandas as pd

def return_query(df, key):

    # Sort the data frame by years
    df = df.sort_values('year')

    print(f'\nThis are the papers on {key}:\n')
    for idx in df.index:

        # Check it is not a DOI
        DOI = False
        tmp = df.paper[idx].split('/')
        if len(tmp) > 2: DOI = True

        if not DOI: line = f'https://arxiv.org/abs/{df.paper[idx]}\t{df.author[idx]} ({df.year[idx]})'
        else:       line = f'DOI: {df.paper[idx]}\t{df.author[idx]} ({df.year[idx]})'
        print(line)
    print('')

    return 0

def return_inspire_links(df, key):

    print(f'\nThis are the inspire links on {key}:\n')
    for idx in df.index:
        line = f'https://inspirehep.net/literature?sort=mostrecent&size=25&page=1&q={df.paper[idx]}\t{df.author[idx]} ({df.year[idx]})'
        print(line)
    print('')

    return 0

def print_possible_tags(df):

    print(f'\nThis are the available options for query:\n')
    for tag in df.tag.unique():
        print(tag)
    print('')

    return 0

def check_tag_query(df, key):

    if key not in df.tag.unique():
        raise ValueError('The requested tag is not currently available. Please, use "-o 1" to see the currently available options.')

def print_help():

    row_1 = '\nTo add a new paper to the bibliography.txt file:\npython oven.py -ar 1 -x 1970.1234 -a chandrasekhar -y 1970 -t black-holes perturbations\n\n'
    row_2 = 'To list the archived papers on "black-holes":\npython oven.py -q black-holes\n\n'
    row_3 = 'To see the available tags:\npython oven.py -o 1\n'

    txt = row_1 + row_2 + row_3
    print(txt)
    exit()

def add_reference(args):

    if (args.arxiv == None or args.author == None or args.year == None or args.tag == False) and args.doi == None:
        raise ValueError('If you want to add a new reference, you need to pass ArXiv ID, author, year, and at least one tag.')
    
    DOI = False
    if   not args.arxiv == None and args.doi == None: pass
    elif args.arxiv == None and not args.doi == None:
        args.arxiv = args.doi
        DOI = True
    else: raise ValueError('You cannot pass both an ArXiv and a DOI.')

    with open('bibliography.txt', 'r+') as f:
        lines = f.readlines()
        print('')
        for tag in args.tag:
            newline = f'{args.arxiv}\t{args.author}\t{args.year}\t{tag}'
            if newline+'\n' in lines:
                print(f'The proposed paper {args.arxiv} is already present in the bibliography, at least with the tag {tag}\n')
            else:
                f.write('\n'+newline)
                print(f'The following paper has been correctly added to the bibliography with the tag {tag}')
                if   not DOI: line = f'https://arxiv.org/abs/{args.arxiv}\t{args.author} ({args.year})\n'
                else:         line = f'DOI: {args.doi}\t{args.author} ({args.year})\n'
                print(line)
        f.close

    return 0
    
if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(add_help = False)
    parser.add_argument('-h',  '--help',    type = int, metavar = 'help',    default = False)

    parser.add_argument('-p',  '--paper',   type = str, metavar = 'paper',   default = None)
    parser.add_argument('-q',  '--query',   type = str, metavar = 'query',   default = None)
    parser.add_argument('-i',  '--inspire', type = int, metavar = 'inspire', default = False)
    parser.add_argument('-o',  '--options', type = int, metavar = 'options', default = False)

    parser.add_argument('-ar', '--add-ref', type = int, metavar = 'add_ref', default = False)
    parser.add_argument('-x',  '--arxiv',   type = str, metavar = 'arxiv',   default = None)
    parser.add_argument('-a',  '--author',  type = str, metavar = 'author',  default = None)
    parser.add_argument('-y',  '--year',    type = str, metavar = 'year',    default = None)
    parser.add_argument(       '--doi',     type = str, metavar = 'doi',     default = None)
    parser.add_argument('-t',  '--tag',     nargs='+',  help='<Required> Set flag', required = False)

    args = parser.parse_args()

    if args.help: print_help()

    # Add reference if passed
    if args.add_ref: add_reference(args)
    else:
        # Read the bibliography from file
        df = pd.read_csv('bibliography.txt', sep = '\t', header = None, names = ['paper', 'author', 'year', 'tag'])
        key = args.query

        # Show all the available options for query
        if args.options: print_possible_tags(df)
        else:
            check_tag_query(df, key)
            # Print the inspire links for latex citations
            if args.inspire: return_inspire_links(df[df['tag'] == key], key)
            else:
                # Return the query
                return_query(df[df['tag'] == key], key)