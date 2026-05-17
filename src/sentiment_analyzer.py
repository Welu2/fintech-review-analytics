import pandas as pd
from transformers import pipeline

_CLASSIFIER_PIPELINE = None


# ------------------------------------------------------------
# LOAD DISTILBERT PIPELINE
# ------------------------------------------------------------

def get_sentiment_pipeline():
    """
    Loads and caches Hugging Face DistilBERT sentiment pipeline.
    """

    global _CLASSIFIER_PIPELINE

    if _CLASSIFIER_PIPELINE is None:

        _CLASSIFIER_PIPELINE = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            truncation=True,
            max_length=512,
            device=-1
        )

    return _CLASSIFIER_PIPELINE


# ------------------------------------------------------------
# BATCH SENTIMENT INFERENCE
# ------------------------------------------------------------

def compute_sentiment_batch(text_series, batch_size=64):
    """
    Runs batched sentiment inference.

    Adds custom Neutral class using confidence thresholding.
    """

    nlp = get_sentiment_pipeline()

    cleaned_inputs = [

        str(text)
        if (pd.notna(text) and str(text).strip() != "")
        else ""

        for text in text_series
    ]

    labels = []
    scores = []

    results = nlp(
        cleaned_inputs,
        batch_size=batch_size
    )

    for i, res in enumerate(results):

        # Empty review handling
        if cleaned_inputs[i] == "":

            labels.append("Neutral")
            scores.append(0.0)

        else:

            score = round(res['score'], 4)

            # Add Neutral threshold
            if score < 0.60:
                label = "Neutral"

            else:
                label = res['label'].title()

            labels.append(label)
            scores.append(score)

    return labels, scores