import pendulum
from airflow.decorators import dag
from airflow.operators.bash import BashOperator

@dag(
    dag_id="hourly_feature_materialization",
    schedule="@hourly",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["feature-store"],
)
def feature_materialization_dag():
    materialize_features = BashOperator(
        task_id="materialize_incremental_features",
        bash_command=(
            "cd feature_repo && "
            "feast materialize-incremental $(date -u +'%Y-%m-%dT%H:%M:%S')"
        ),
    )

feature_materialization_dag()