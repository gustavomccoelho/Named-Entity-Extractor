# Portuguese Named Entity Extractor
This repository describes a Named Entity Extractor, a proposed implementation of the Named Entity Recognition (NER) task for a given portuguese written file (or a set of files) in PDF format. The model used for this task is based on the **BERTimbau project** [[1]](#1), where the word embeddings ([BERT](https://github.com/google-research/bert)) are combined with a CRF layer and trained on a portuguese corpus. The base code is taken from the [original project](https://github.com/neuralmind-ai/portuguese-bert).  

The entities classes are set as below:

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
The list of the required python packages is found on utils/requirements.txt. For quick instalation under the selected environment, simply run:

```
pip install -r requirements.txt
```

The pre-trained models can be downloaded from [this link](https://neuralmind-ai.s3.us-east-2.amazonaws.com/nlp/bert-large-portuguese-cased/bert-large-portuguese-cased_tensorflow_checkpoint.zip). The default location is: data/input/model_checkpoint/.

The test environment was configured as following:

- Operational System: Ubuntu 18.04
- Python version: 3.6
- Java version: 8

Note: Java is required for handling PDF files by the tika package.

# Implementation
To implement the program at the default arguments, simply place the PDF document(s) into the input folder (default is data/input/raw/) and run: 

```
python main.py
```

The default output folders are set as below:

- data/output/wordcloud/ (for wordclouds)
- data/output/entities/ (for list of entities)

# List of implementation parameters

```
python main.py
    --verbose 1 {0 for silent run}
    --input_path data/input/raw/
    --predictions_file data/input/temp/predictions.txt
    --entities_path data/output/entities/
    --wordcloud_path data/output/wordcloud/
    --labels_file data/input/labels/classes.txt
    --bert_model data/input/model_checkpoint/
    
```

# References

<a id="1">[1]</a> SOUZA, Fábio; NOGUEIRA, Rodrigo; LOTUFO, Roberto. Portuguese named entity recognition using BERT-CRF. arXiv preprint arXiv:1909.10649, 2019.
