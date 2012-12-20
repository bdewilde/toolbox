# This program parses LexisNexis output
# Example: > python lexis_nexis_parser.py in='inputfile.txt' out='outputfile.txt' print=True

import csv
import re
import sys

# set up run options
inFileName = None
doPrint = False
outFileName = 'lexis_nexis_output.txt'
# overwrite with command line args if given, formatted as key=value
for arg in sys.argv[1:] :
    key, val = arg.split('=')
    if key == 'in' : inFileName = val
    elif key == 'out' : outFileName = val
    elif key == 'print' : doPrint = bool(val)
if inFileName is None :
    sys.exit("ERROR: Must provide input file name on command line, e.g. in=input.txt")
print "\nINFO: RUN OPTIONS"
print "... in =", inFileName
print "... out =", outFileName
print "... print =", doPrint

# input/output files
inFile = open(inFileName, 'r')
outFile = open(outFileName, 'w')
KEYS = ['pub', 'pub_date', 'show', 'anchors', 'guests', 'blog', 'byline',
    'section', 'length', 'load_date', 'language', 'pub_type', 'journal_code',
    'copyright', 'article_text']
csv_writer = csv.DictWriter(outFile, KEYS, delimiter="\t")
csv_writer.writeheader()

# split LexisNexis document on "X of Y DOCUMENTS" lines
docs = re.split(r'\d+ of \d+ DOCUMENTS', inFile.read())

# get cover page search info if available
cover = docs[0]
dwnldreqs = re.search(r'^Download Request: .*', cover, re.MULTILINE)
if dwnldreqs is not None : dwnldreqs = dwnldreqs.group()
terms = re.search(r'^Terms: .*(\n.*){2}', cover, re.MULTILINE)
if terms is not None : terms = terms.group()
sources = re.search(r'^Source: .*', cover, re.MULTILINE)
if sources is not None : sources = sources.group()
if doPrint is True :
    print "\nINFO: COVER PAGE"
    print "...", dwnldreqs
    print "...", terms
    print "...", sources

# iterate over documents
for doc in docs[1:] :
    # clean up white space
    lines = re.split('\r\n|\n\n', doc)
    lines = [line.strip() for line in lines if line != '']
    # create dict of all data with default value 'NA'
    row = {}
    for key in KEYS : row[key] = 'NA'
    # get leading metadata; special care taken with dates to avoid errors
    row['pub'] = lines[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December']
    for month in months :
        if lines[1].startswith(month) :
            row['pub_date'] = lines[1]
            del lines[0:2]
            break
    if row['pub_date'] == 'NA' :
        row['pub'] += ' ' + lines[1]
        row['pub_date'] = lines[2]
        del lines[0:3]

    #row['pub_date'] = lines[1]    # rarely errs
    #del lines[0:2]
    # get remaining metadata, set default to 'NA'
    # by iterating over lines in document
    for line in lines[:] :
        if line.startswith('SHOW: ') :
            row['show'] = line[len('SHOW: '):]
            del lines[lines.index(line)]
        elif line.startswith('ANCHORS: ') :
            row['anchors'] = line[len('ANCHORS: '):]
            del lines[lines.index(line)]
        elif line.startswith('GUESTS: ') :
            row['guests'] = line[len('GUESTS: '):]
            del lines[lines.index(line)]
        elif line.startswith('BLOG: ') :
            row['blog'] = line[len('BLOG: '):]
            del lines[lines.index(line)]
        elif line.startswith('BYLINE: ') :
            row['byline'] = line[len('BYLINE: '):]
            del lines[lines.index(line)]
        elif line.startswith('SECTION: ') :
            row['section'] = line[len('SECTION: '):]
            del lines[lines.index(line)]
        elif line.startswith('LENGTH: ') :
            row['length'] = line[len('LENGTH: '):]
            del lines[lines.index(line)]
        elif line.startswith('LANGUAGE:') :
            row['language'] = line[len('LANGUAGE:'):].lower()
            del lines[lines.index(line)]
        elif line.startswith('LOAD-DATE: ') :
            row['load_date'] = line[len('LOAD-DATE: '):]
            del lines[lines.index(line)]
        elif line.startswith('PUBLICATION-TYPE: ') :
            row['pub_type'] = line[len('PUBLICATION-TYPE: '):].lower()
            del lines[lines.index(line)]
        elif line.startswith('JOURNAL-CODE: ') :
            row['journal_code'] = line[len('JOURNAL-CODE: '):]
            del lines[lines.index(line)]
        elif line.startswith('Copyright ') :
            row['copyright'] = line[len('Copyright '):]
            # also get rid of 'All Rights Reserved'
            del lines[-3:]

    # all remaining lines should be article text
    article_text = ' '.join(lines)
    row['article_text'] = re.sub(r'\s', ' ', article_text)

    # helpful printout
    if doPrint is True :
        print "\nPUBLICATION:", row['pub']
        print "PUB-DATE:", row['pub_date']
        print "ANCHORS:", row['anchors']
        print "GUESTS:", row['guests']
        print "SHOW:", row['show']
        print "BLOG:", row['blog']
        print "BYLINE:", row['byline']
        print "SECTION:", row['section']
        print "LENGTH:", row['length']
        print "LOAD-DATE:", row['load_date']
        print "LANGUAGE:", row['language']
        print "PUB-TYPE:", row['pub_type']
        print "JOURNAL-CODE:", row['journal_code']
        print "COPYRIGHT:", row['copyright']
        print "ARTICLE TEXT:", "\n", row['article_text']

    csv_writer.writerow(row)

print "\nINFO: output saved to", outFileName
outFile.close()