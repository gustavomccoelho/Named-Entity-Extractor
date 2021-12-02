# Portuguese Named Entity Extractor
This repository describes a Named Entity Extractor, a proposed implementation of the Named Entity Recognition (NER) task for a given portuguese written file (or a set of files) in PDF format. The model used for this task is based on the **BERTimbau project** [[1]](#1), where the word embeddings ([BERT](https://github.com/google-research/bert)) are combined with a CRF layer and trained on a portuguese corpus. The base code is taken from the [original project](https://github.com/neuralmind-ai/portuguese-bert).  

The entities classes are as following:

- Place ("Local")
- Name ("Nome")
- Organization ("Organização")
- Time ("Tempo")
- Value ("Valor")

The final output is composed of:

- A list of all named entities extracted and its frequencies for each class
- A corresponding wordcloud for each named entity class, as below (for class Time)

<img src="https://github.com/gustavomccoelho/Named-Entity-Extractor/blob/main/data/output/wordcloud/wordcloud_tempo.jpg" width="500">

# Requirements


# Environment
The test environment was configured as following:

- Operational System: Ubuntu 18.04
- Python version: 3.6
- Java version: 8

# Implementation
To implement the program, simply place the PDF document(s) into the folder data/input/raw/ and run: 

```
python main.py
```

The outputs are store under:

- data/output/wordcloud/ (for wordclouds)
- data/output/entities/ (for list of entities)

# References

<a id="1">[1]</a> SOUZA, Fábio; NOGUEIRA, Rodrigo; LOTUFO, Roberto. Portuguese named entity recognition using BERT-CRF. arXiv preprint arXiv:1909.10649, 2019.
