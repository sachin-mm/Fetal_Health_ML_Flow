import os
from random import random
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn import utils
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

# mlflow server \
 #   --backend-store-uri sqlite:///mlflow.db \
 #   --default-artifact-root ./artifacts \
 #   --host 0.0.0.0

# mlflow.set_tracking_uri("http://localhost:5000")
# request_uri="http://127.0.0.1:5000/invocations"

def eval_metrics(actual, pred):
    precision = precision_score(actual, pred, average="weighted")
    recall = recall_score(actual, pred, average="weighted")
    f1 = f1_score(actual, pred, average="micro")
    accuracy = accuracy_score(actual, pred)
    return precision,recall,f1,accuracy

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)
    mlflow.set_tracking_uri("http://localhost:8000")


    try:
        data = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fetal_health.csv"))
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s", e
        )

    X=data.drop(["fetal_health"],axis=1)
    y=data["fetal_health"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 10, test_size = 0.2)
    
    ne= int(sys.argv[1])
    md=int(sys.argv[2])
    with mlflow.start_run(run_name='fetal_health'):
        rf_classifier=RandomForestClassifier(n_estimators=ne, max_depth=md)
        rf_classification = rf_classifier.fit(X_train, y_train)
        y_pred=rf_classification.predict(X_test)

        (precision,recall,f1,accuracy) = eval_metrics(y_test,y_pred)

        
        print("  precision: %s" % precision)
        print("  recall: %s" % recall)
        print("  f1: %s" % f1)
        print(" accuracy:%s"% accuracy)

        mlflow.log_param("n_estimators", ne)
        mlflow.log_param("max_depth", md)

        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("accuracy", accuracy)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Model registry does not work with file store
        if tracking_url_type_store != "file":

            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(rf_classification, "model", registered_model_name='rf_classification')
        else:
            mlflow.sklearn.log_model(rf_classification, "model")
