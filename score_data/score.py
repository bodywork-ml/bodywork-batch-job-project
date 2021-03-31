"""
This module defines what will happen in the batch job:

- download dataset from cloud storage (AWS S3);
- load model;
- score dataset; and,
- save results to cloud storage (AWS S3).
"""
from urllib.request import urlopen

import boto3 as aws
import pandas as pd
from joblib import load
from sklearn.base import BaseEstimator

DATA_URL = ('http://bodywork-batch-job-project.s3.eu-west-2.amazonaws.com'
            '/data/iris_classification_data.csv')
TRAINED_MODEL_FILENAME = 'classification_model.joblib'
SCORED_DATA_AWS_BUCKET = 'bodywork-batch-job-project'
SCORED_DATA_FILENAME = 'iris_classification_data_scored.csv'


def main() -> None:
    """Main script to be executed."""
    data = download_dataset(DATA_URL)
    model = load(TRAINED_MODEL_FILENAME)
    scored_data = score_data(data, model)
    upload_results(scored_data)


def download_dataset(url: str) -> pd.DataFrame:
    """Get data from cloud object storage."""
    print(f'downloading training data from {DATA_URL}')
    data_file = urlopen(url)
    return pd.read_csv(data_file)


def score_data(data: pd.DataFrame, model: BaseEstimator) -> pd.DataFrame:
    """Score data using model."""
    feature_columns = [
        'sepal length (cm)',
        'sepal width (cm)',
        'petal length (cm)',
        'petal width (cm)'
    ]
    label_to_classes_map = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
    X = data[feature_columns].values
    data['predicted_labels'] = model.predict(X)
    data['predicted_class'] = (
        data['predicted_labels']
        .apply(lambda e: label_to_classes_map[e])
    )
    return data


def upload_results(scored_data: pd.DataFrame) -> None:
    """Put scored data into cloud object storage."""
    scored_data.to_csv(SCORED_DATA_FILENAME, index=False)
    try:
        s3_client = aws.client('s3')
        s3_client.upload_file(
            f'bodywork_project/score-data/{SCORED_DATA_FILENAME}',
            SCORED_DATA_AWS_BUCKET,
            f'scored-data/{SCORED_DATA_FILENAME}'
        )
        print(f'scored data saved to s3://{SCORED_DATA_AWS_BUCKET}'
              f'/{SCORED_DATA_FILENAME}')
    except Exception:
        print('could not upload scored data to S3 - check AWS credentials')


if __name__ == '__main__':
    main()
