from tika import parser
from os import listdir
from os.path import isfile, join
from argparse import ArgumentParser
from progress.bar import Bar
from run_inference import run_inference
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter


def plot_cloud(entities):
    """"""
    wordcloud = WordCloud(width=3000, height=2000, random_state=1, background_color='salmon', colormap='Pastel1',
                          collocations=False).generate_from_frequencies(Counter(entities))
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud)
    plt.axis("off")


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
        single_text = single_text.replace('..', '.')

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
                           default="../data/input/raw/",
                           help="Path for pdf input files."
                                "Default is ../data/input/raw/")
    argParser.add_argument("--predictions_file",
                           default="../data/input/temp/predictions.txt",
                           help="Predictions file."
                                "Default is ../data/input/temp/predictions.txt")
    argParser.add_argument("--entities_path",
                           default="../data/output/entities/",
                           help="Path for entities frequencies output."
                                "Default is ../data/output/entities/")
    argParser.add_argument("--wordcloud_path",
                           default="../data/output/wordcloud/",
                           help="Path for txt files."
                                "Default is ../data/output/wordcloud/")
    argParser.add_argument('--labels_file',
                           default="../data/input/labels/classes.txt",
                           help="File with all NER classes to be considered, one "
                                "per line.")
    argParser.add_argument('--bert_model',
                           default="../data/input/model_checkpoint/",
                           help="Path to the BERT model"
                                "Default is ../data/input/model_checkpoint/")


    args = argParser.parse_args()

    # Collecting input file names
    fileList = [f for f in listdir(args.input_path) if isfile(join(args.input_path, f))]
    bar = Bar('Loading PDF files', max=len(fileList))
    text_list = []
    invalid_files = []

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

    bar = Bar('Pre-processing text', max=len(text_list))

    # Pre-processing text
    for i, text in enumerate(text_list):
        text_list[i] = pre_process(text)
        if args.verbose == '1':
            bar.next()
    bar.finish()

    inference_args = {
        "labels_file": args.labels_file,
        "tokenizer_model": args.bert_model,
        "bert_model": args.bert_model,
        "input_file": "../data/input/temp/pre_processed.txt",
        "output_file": args.predictions_file,
    }

    bar = Bar('Extracting entities', max=len(text_list))
    entities_list = []

    # Extracting entities from each file
    for i, text in enumerate(text_list):
        try:
            text_file = open(inference_args["input_file"], "w", encoding="utf-8")
            text_file.write(text)
            text_file.close()
            run_inference(inference_args)
            with open(args.predictions_file) as json_file:
                entities_list.append(json.load(json_file))

        except AssertionError:
            if args.verbose == '1':
                print("\nAssertion error on file " + fileList[i])
            pass
        if args.verbose == '1':
            bar.next()
    bar.finish()

    # Splitting entities according to class
    bar = Bar('Splitting entities', max=len(entities_list))
    pessoa = []
    tempo = []
    valor = []
    local = []
    organizacao = []

    for i in range(len(entities_list)):
        for j in range(len(entities_list[i][0]['entities'])):

            if entities_list[i][0]['entities'][j]['class'] == 'PESSOA':
                pessoa.append(entities_list[i][0]['entities'][j]['text'])

            if entities_list[i][0]['entities'][j]['class'] == 'TEMPO':
                tempo.append(entities_list[i][0]['entities'][j]['text'])

            if entities_list[i][0]['entities'][j]['class'] == 'VALOR':
                valor.append(entities_list[i][0]['entities'][j]['text'])

            if entities_list[i][0]['entities'][j]['class'] == 'LOCAL':
                local.append(entities_list[i][0]['entities'][j]['text'])

            if entities_list[i][0]['entities'][j]['class'] == 'ORGANIZACAO':
                organizacao.append(entities_list[i][0]['entities'][j]['text'])
        if args.verbose == '1':
            bar.next()
    bar.finish()

    plot_cloud(pessoa)
    plt.savefig(args.wordcloud_path + 'wordcloud_pessoa.jpg')
    plot_cloud(tempo)
    plt.savefig(args.wordcloud_path + 'wordcloud_tempo.jpg')
    plot_cloud(valor)
    plt.savefig(args.wordcloud_path + 'wordcloud_valor.jpg')
    plot_cloud(local)
    plt.savefig(args.wordcloud_path + 'wordcloud_local.jpg')
    plot_cloud(organizacao)
    plt.savefig(args.wordcloud_path + 'wordcloud_organizacao.jpg')

    print("Wordclouds plotted.")

    with open(args.entities_path + "entities_count_pessoa.txt", "w", encoding='utf-8') as file:
        file.write(str(Counter(pessoa)))
    with open(args.entities_path + "entities_count_tempo.txt", "w", encoding='utf-8') as file:
        file.write(str(Counter(tempo)))
    with open(args.entities_path + "entities_count_local.txt", "w", encoding='utf-8') as file:
        file.write(str(Counter(local)))
    with open(args.entities_path + "entities_count_valor.txt", "w", encoding='utf-8') as file:
        file.write(str(Counter(valor)))
    with open(args.entities_path + "entities_count_organizacao.txt", "w", encoding='utf-8') as file:
        file.write(str(Counter(organizacao)))

    print("Entities count saved.")

