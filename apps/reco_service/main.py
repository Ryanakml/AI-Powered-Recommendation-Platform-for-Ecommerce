from fastapi import FastAPI, HTTPException
from feast import FeatureStore
import lightgbm as lgb
import mlflow

app = FastAPI()

# Inisialisasi Feature Store
fs = FeatureStore(repo_path="/path/to/feature_repo")

# Muat model Ranker dari MLflow Registry
logged_model_uri = "models:/LGBMRanker/Production"
ranker = mlflow.lightgbm.load_model(logged_model_uri)

@app.get("/recommendations/v1/{user_id}")
def get_recommendations(user_id: str, k: int = 10):
    # 1. Dapatkan kandidat dari berbagai generator (ALS, ItemCF, dll.)
    #... (logika candidate generation)
    candidates = ["item_101", "item_205", "item_300",...]

    # 2. Ambil fitur online untuk pengguna dan kandidat dari Feast
    feature_vector = fs.get_online_features(
        features=[
            "user_aggregate_features:total_purchases_7d",
            "item_features:price",
            "item_features:category",
        ],
        entity_rows=[{"user_id": user_id, "item_id": item_id} for item_id in candidates],
    ).to_dict()

    # 3. Siapkan data untuk ranker
    #... (logika persiapan fitur)

    # 4. Beri skor kandidat dengan model Ranker
    scores = ranker.predict(ranker_features)
    
    # 5. Urutkan kandidat berdasarkan skor
    #...
    
    # 6. Terapkan logika re-ranking (diversifikasi, filter)
    #...

    # 7. Kembalikan top-k rekomendasi
    return {"user_id": user_id, "recommendations": final_recommendations[:k]}