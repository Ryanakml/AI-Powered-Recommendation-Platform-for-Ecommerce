# ml/ranker/train_ranker.py
import lightgbm as lgb
import shap

def train_ranker(training_data):
    # training_data adalah DataFrame dengan kolom:
    # 'user_id', 'item_id', 'relevance_score', 'query_id', dan fitur-fitur lainnya
    
    X_train = training_data.drop(columns=['user_id', 'item_id', 'relevance_score', 'query_id'])
    y_train = training_data['relevance_score']
    
    # Group mendefinisikan jumlah item per kueri (user)
    group_train = training_data.groupby('query_id').size().to_list()

    ranker = lgb.LGBMRanker(
        objective="lambdarank",
        metric="ndcg",
        n_estimators=1000,
        learning_rate=0.05,
    )
    
    ranker.fit(
        X_train,
        y_train,
        group=group_train,
        eval_set=[(X_train, y_train)],
        eval_group=[group_train],
        eval_at=,
    )
    
    # Menghasilkan penjelasan SHAP
    explainer = shap.TreeExplainer(ranker)
    shap_values = explainer.shap_values(X_train)
    
    # Plot dan simpan summary plot
    shap.summary_plot(shap_values, X_train, show=False)
    
    return ranker