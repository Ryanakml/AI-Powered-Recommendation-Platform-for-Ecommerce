# ml/candidate/item_item_cf.py
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

def train_item_item_cf(interactions_df):
    # Buat user-item matrix
    user_item_matrix = interactions_df.pivot_table(
        index='user_id', columns='item_id', values='interaction_strength'
    ).fillna(0)
    
    # Buat sparse matrix
    user_item_sparse = csr_matrix(user_item_matrix.values)
    
    # Hitung cosine similarity antar item
    item_similarity = cosine_similarity(user_item_sparse.T)
    
    # Simpan matriks similaritas
    #...
    return item_similarity