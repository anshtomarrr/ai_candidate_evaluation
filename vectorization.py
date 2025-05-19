from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def vectorize_texts(texts):
    """
    Perform TF-IDF vectorization on a list of preprocessed texts.
    """
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))  # Unigrams and bigrams
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix


def calculate_similarity(tfidf_matrix):
    """
    Calculate cosine similarity between the first document (job description) and the second document (resume).
    """
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return similarity 