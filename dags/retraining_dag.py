# dags/retraining_dag.py
from airflow.decorators import dag, task
from airflow.operators.python import BranchPythonOperator
import pendulum

@dag(dag_id="weekly_model_retraining", schedule="@weekly", start_date=pendulum.now())
def retraining_dag():
    @task
    def get_training_data():...

    @task
    def train_new_model(): 
        # Menggunakan MLflow untuk melacak run
       ...
        return new_model_metrics

    @task
    def get_production_model_metrics():...

    @task.branch
    def compare_models(new_metrics, prod_metrics):
        if new_metrics['ndcg@10'] > prod_metrics['ndcg@10'] * 1.01:
            return "promote_model_task"
        else:
            return "skip_promotion_task"

    @task
    def promote_model(): 
        # Menggunakan MLflow client untuk mempromosikan model ke 'Production'
       ...

    @task
    def skip_promotion():...

    data = get_training_data()
    new_metrics = train_new_model(data)
    prod_metrics = get_production_model_metrics()
    comparison = compare_models(new_metrics, prod_metrics)
    comparison >> [promote_model(), skip_promotion()]

retraining_dag()