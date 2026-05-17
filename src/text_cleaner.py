import re
import nltk

# Download required NLTK resources safely
for resource in ['stopwords', 'wordnet', 'omw-1.4']:

    try:
        nltk.data.find(f'corpora/{resource}')

    except LookupError:
        nltk.download(resource, quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# ------------------------------------------------------------
# INITIALIZE NLP COMPONENTS
# ------------------------------------------------------------

LEMMATIZER = WordNetLemmatizer()

STOPWORDS = set(stopwords.words('english'))

DOMAIN_STOPWORDS = STOPWORDS.union({

    'bank',
    'app',
    'cbe',
    'dashen',
    'abyssinia',
    'boa',
    'good',
    'nice',
    'bad',
    'worst',
    'please',
    'money',
    'update',
    'fix',
    'working',
    'open',
    'telebirr',
    'awash',
    'amhara',
    'hibret'
})


# ------------------------------------------------------------
# TEXT CLEANING FUNCTION
# ------------------------------------------------------------

def clean_review_text(text):
    """
    Cleans raw review text using:
    - lowercase normalization
    - regex cleanup
    - stopword removal
    - lemmatization
    """

    if not isinstance(text, str):
        return ""

    # Lowercase
    text = text.lower()

    # Remove special characters and digits
    text = re.sub(r'[^a-z\s]', '', text)

    tokens = []

    for word in text.split():

        if word not in DOMAIN_STOPWORDS:

            # Verb lemmatization
            lemma = LEMMATIZER.lemmatize(word, pos='v')

            # Noun lemmatization
            lemma = LEMMATIZER.lemmatize(lemma, pos='n')

            tokens.append(lemma)

    return " ".join(tokens)