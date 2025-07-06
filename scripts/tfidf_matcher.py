from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def rank_resumes(resumes, job_description, filenames):

  docs = [job_description] + resumes

  vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
  tfidf_matrix = vectorizer.fit_transform(docs)

  similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

  
  ranked = sorted(zip(filenames, similarities), key=lambda x: x[1], reverse=True)

  return ranked

