import pandas as pd
import numpy as np
from catboost import CatBoostRegressor, Pool, metrics, cv, MetricVisualizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


class DietPredictor:
    def __init__(self) -> None:
        self.regressor = CatBoostRegressor(random_seed=42)

    def train(self, dataset: pd.DataFrame) -> None:
        x_data = dataset.drop('diet_recommendation', axis=1)
        y_data = dataset.diet_recommendation

        x_train, x_validation, y_train, y_validation = train_test_split(x_data, y_data, train_size=0.75, random_state=42)
        categotial_features_indexes = np.where(x_data.dtypes == object)[0]

        self.regressor.fit(
            x_train, y_train,
            cat_features=categotial_features_indexes,
            eval_set=(x_validation, y_validation),
            logging_level='Verbose',
            plot=True
        )

        y_predicted = self.regressor.predict(x_validation)
        r2 = r2_score(y_validation, y_predicted)
        print(f'r2 = {r2}')
