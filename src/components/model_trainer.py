import os
import sys

from catboost import CatBoostClassifier, CatBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from xgboost import XGBClassifier, XGBRegressor

from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
    RandomForestRegressor,
)

from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_trainer(self, train_array, test_array):
        try:
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],  
                train_array[:, -1],  
                test_array[:, :-1],   
                test_array[:, -1],    
            )
            model = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
                  
            }



            model_report : dict = evaluate_models(x_train = x_train, y_train = y_train, x_test = x_test, y_test = y_test, models = model)
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
                ]
            best_model = model[best_model_name]
            
            if best_model_score < 0.6:
                raise CustomException(
                    "No best model found with sufficient accuracy.."
                )
            logging.info(f"Best model found: {best_model_name} with score: {best_model_score}")
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            
            predicted = best_model.predict(x_test)
            r2_square = r2_score(y_test, predicted)
            
            return r2_square
                
        except Exception as e:
            raise CustomException(e, sys)
