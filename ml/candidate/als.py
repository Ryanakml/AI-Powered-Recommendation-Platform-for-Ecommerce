# ml/candidate/als.py
import implicit
from scipy.sparse import coo_matrix

def train_als(interactions_df):
    # Siapkan data untuk sparse matrix
    user_cat = interactions_df['user_id'].astype('category').cat
    item_cat = interactions_df['item_id'].astype('category').cat
    
    # Buat sparse matrix
    interaction_matrix = coo_matrix(
        (interactions_df['interaction_strength'].astype(float),
         (user_cat.codes, item_cat.codes)),
        shape=(len(user_cat.categories), len(item_cat.categories))
    ).tocsr()

    # Inisialisasi dan latih model ALS
    model = implicit.als.AlternatingLeastSquares(factors=50, regularization=0.01, iterations=20)
    model.fit(interaction_matrix)
    
    # Simpan model dan pemetaan kategori
    #...
    return model, user_cat, item_cat