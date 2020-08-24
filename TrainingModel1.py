from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


# training data
TRAIN_DATA = [
    ("Who is Shaka Khan?", {"entities": [(7, 17, "PERSON")]}),
    ("I like London and Berlin.", {"entities": [(7, 13, "LOC"), (18, 24, "LOC")]}),
    ("Satnam invested in Europe", {"entities": [(0, 6, "PERSON"), (19, 24, "LOC")]}),
    ("Republic of Estonia ", {"entities": [(0, 19, "LOC")]}),
    ("Ministry of Defense ", {"entities": [(0, 19, "ORG")]}),
    ("Ministry of Economic Affairs and Communication ", {"entities": [(0, 46, "ORG")]}),
    ("Aorta Limited ", {"entities": [(0, 13, "ORG")]}),
    ("Ämari Airport ", {"entities": [(0, 13, "LOC")]}),
    ("Logistic Park ", {"entities": [(0, 13, "LOC")]}),
    ("Ämari Air Base ", {"entities": [(0, 13, "ORG")]}),
    ("Aorta ", {"entities": [(0, 5, "ORG")]}),
    ("Ämari Logistics Group ", {"entities": [(0, 21, "ORG")]}),
    ("Ämari Logistics Park ", {"entities": [(0, 20, "ORG")]}),
    ("Ämari Freight Services ", {"entities": [(0, 22, "ORG")]}),
    ("National Defense ", {"entities": [(0, 16, "ORG")]}),
    ("Aorta ", {"entities": [(0, 5, "ORG")]}),
    ("Harjumaa ", {"entities": [(0, 8, "LOC")]}),
    ("Steve Ampleford ", {"entities": [(0, 15, "PERSON")]}),
    ("Berkley Square ", {"entities": [(0, 14, "LOC")]}),
    ("London ", {"entities": [(0, 6, "LOC")]}),
    ("United Kingdom ", {"entities": [(0, 15, "LOC")]}),
    ("Estonia ", {"entities": [(0, 6, "LOC")]}),
    ("Hoonestusõigus ", {"entities": [(0, 13, "LAW")]}),

]


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.load("en_core_web_sm")  # create blank Language class
        print("Created blank 'en_core_web_sm' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if model is None:
            nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # save model to output directory

    #output_dir = "D:\\Crymzee\\Steve\Model\\attomusmodel"
    output_dir = "/home/sanam/CuriousHenryBeta/attomusmodel"
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])


if __name__ == "__main__":
    plac.call(main)

    # Expected output:
    # Entities [('Shaka Khan', 'PERSON')]
    # Tokens [('Who', '', 2), ('is', '', 2), ('Shaka', 'PERSON', 3),
    # ('Khan', 'PERSON', 1), ('?', '', 2)]
    # Entities [('London', 'LOC'), ('Berlin', 'LOC')]
    # Tokens [('I', '', 2), ('like', '', 2), ('London', 'LOC', 3),
    # ('and', '', 2), ('Berlin', 'LOC', 3), ('.', '', 2)]