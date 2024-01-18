import pandas as pd
import numpy as np
import hyperopt as ho
from catboost import CatBoostRegressor, Pool, metrics, cv, MetricVisualizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


class DietPredictor:
    def __init__(self) -> None:
        self.regressor = CatBoostRegressor(iterations=500,
                          grow_policy='Depthwise',
                          depth=8,
                          od_type='Iter',
                          od_wait=40,
                          loss_function=metrics.MAE(),
                          random_state=42,
                          learning_rate=0.03,
                          l2_leaf_reg=0.5,
                          eval_metric=metrics.MAE())
        
        self.path_to_saved = 'model.dump'

    def train(self, dataset: pd.DataFrame) -> None:
        x_data = dataset.drop('diet_recommendation', axis=1)
        y_data = dataset.diet_recommendation

        x_train, x_validation, y_train, y_validation = train_test_split(x_data, y_data, train_size=0.75, random_state=42)
        categotial_features_indexes = np.where(x_data.dtypes == object)[0]

        self.regressor.fit(x_train, y_train,
            cat_features=categotial_features_indexes,
            eval_set=(x_validation, y_validation),
            logging_level='Verbose',
            plot=True)

        y_predicted = self.regressor.predict(x_validation)
        r2 = r2_score(y_validation, y_predicted)
        print(f'r2 = {r2}')

    def train1(self, dataset: pd.DataFrame) -> None:
        x_data = dataset.drop('diet_recommendation', axis=1)
        y_data = dataset.diet_recommendation

        x_train, x_validation, y_train, y_validation = train_test_split(x_data, y_data, train_size=0.75, random_state=42)
        categotial_features_indexes = np.where(x_data.dtypes == object)[0]

        self.regressor.fit(x_train, y_train,
            cat_features=categotial_features_indexes,
            eval_set=(x_validation, y_validation),
            logging_level='Verbose',
            plot=True)
        
        y_predicted = self.regressor.predict(x_validation)
        r2 = r2_score(y_validation, y_predicted)
        print(f'r2 = {r2}')
        print()

        train_pool = Pool(x_train, y_train, categotial_features_indexes)
        feature_importances = self.regressor.get_feature_importance(train_pool)
        feature_names = x_train.columns
        print('features importances:')
        for score, name in sorted(zip(feature_importances, feature_names), reverse=True):
            print(f'{name}: {score}')
        
        print()
            
    def predict(self, product_info, person_info):
        x = [product_info['product'], product_info['protein'], product_info['fats'], product_info['carbohydrates'],
             product_info['calorie_content'], product_info['sugar'], product_info['expiration_date']]
        
        x.extend([person_info['sex'], person_info['age'], person_info['height'], person_info['weight'], person_info['disease']])
        return self.regressor.predict(x)


    @staticmethod
    def find_opt_params(dataset: pd.DataFrame) -> None:
        x_data = dataset.drop('diet_recommendation', axis=1)
        y_data = dataset.diet_recommendation
        categotial_features_indexes = np.where(x_data.dtypes == object)[0]

        def ho_obj(params):
            model = CatBoostRegressor(l2_leaf_reg=int(params['l2_leaf_reg']),
                learning_rate=params['learning_rate'],
                grow_policy = 'Depthwise',
                depth=8,
                iterations=500,
                od_type='Iter',
                od_wait=40,
                loss_function=metrics.MAE(),
                eval_metric=metrics.MAE(),
                random_seed=42,
                verbose=False)

            print('start_cv')
            cv_data = cv(Pool(x_data, y_data, categotial_features_indexes),
                         model.get_params(),
                         logging_level='Silent')
            
            print(cv_data)
            best_acc = np.max(cv_data['test-MAE-mean'])
            return best_acc
        
        params_space = {
            'l2_leaf_reg': ho.hp.qloguniform('l2_leaf_reg', 0, 2, 1),
            'learning_rate': ho.hp.uniform('learning_rate', 1e-3, 5e-1),
        }
        
        trails = ho.Trials()
        best = ho.fmin(ho_obj,
                       space=params_space,
                       algo=ho.tpe.suggest,
                       max_evals=50,
                       trials=trails)
        
        print(best)
    
    def save_model(self) -> None:
        self.regressor.save_model(self.path_to_saved)

    def load_model(self) -> None:
        self.regressor.load_model(self.path_to_saved)
