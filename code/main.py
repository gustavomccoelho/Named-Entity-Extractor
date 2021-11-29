from tika import parser
from os import listdir
from os.path import isfile, join
from argparse import ArgumentParser
from progress.bar import Bar
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter


def load_pdf(pdf_path):
    """Encodes a PDF text file addressed by pdf_path
    using UTF-8 and returns is as a string."""
    single_text = parser.from_file(pdf_path + file)['content']
    single_text.encode('utf-8')
    return single_text


def pre_process(single_text):
    """Pre-processes the input string (single_text)
    by replacing non-valid characters, removing line breakers
    and replacing uppercase by lowercase letters."""

    single_text = single_text.replace('\n', '')
    single_text = single_text.replace('_', '')
    single_text = single_text.replace('●', '')
    single_text = single_text.replace('▪', '')
    single_text = single_text.replace('•', '')
    single_text = single_text.replace('§', '')
    single_text = single_text.replace('–', '.')
    single_text = single_text.replace('-', '.')
    single_text = single_text.replace('\uf0b7', '')

    while '  ' in single_text or '..' in single_text:
        single_text = single_text.replace('  ', ' ')
        single_text = single_text.replace('..', '.b')

    single_text = single_text.lower()

    return single_text


if __name__ == "__main__":

    argParser = ArgumentParser("NER inference CLI")

    # Setting main arguments
    argParser.add_argument("--verbose",
                           default='1',
                           help="Level of verbose (0 for silent, 1 for full verbose)"
                                "Default is 1")
    argParser.add_argument("--input_path",
                           default="../data/input/",
                           help="Path for pdf input files."
                                "Default is ../data/input/")
    argParser.add_argument("--entities_path",
                           default="../data/output/entities/",
                           help="Path for pdf files."
                                "Default is ../data/output/entities/")
    argParser.add_argument("--wordcloud_path",
                           default="../data/output/wordcloud/",
                           help="Path for txt files."
                                "Default is ../data/output/wordcloud/")

    args = argParser.parse_args()

    # Collecting input file names
    fileList = [f for f in listdir(args.input_path) if isfile(join(args.input_path, f))]
    bar = Bar('Loading PDF files', max=len(fileList))
    text_list = []

    # Loading pdf files
    for file in fileList:
        try:
            text = load_pdf(args.input_path)
            text_list.append(text)
        except AttributeError:
            if args.verbose == '1':
                print("\nThe following file cannot be encoded with UTF-8 and will be skipped: " + file)
            continue
        if args.verbose == '1':
            bar.next()
    bar.finish()

    bar = Bar('Pre-Processing text', max=len(fileList))

    # Pre-processing text
    for i, text in enumerate(text_list):
        text_list[i] = pre_process(text)
        if args.verbose == '1':
            bar.next()
    bar.finish()
