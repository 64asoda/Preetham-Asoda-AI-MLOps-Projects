from src.logger import get_logger
from src.custom_exception import CustomException
import pandas as pd
from src.feature_store import RedisFeatureStore
from sklearn.model_selection import train_test_split, GridSearchCV
import xgboost as xgb
import os
import pickle
import sys
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.metrics import precision_recall_fscore_support

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, feature_store:RedisFeatureStore,model_save_path="artifacts/models/"):
        self.feature_store = feature_store
        self.model_save_path = model_save_path
        self.model = None

        os.makedirs(self.model_save_path, exist_ok=True)
        logger.info("Model Training initialized")

    def load_data_from_redis(self, entity_ids):
        try:
            logger.info("Extracting data from Redis")

            data = []
            for entity_id in entity_ids:
                features = self.feature_store.get_features(entity_id)
                if features:
                    data.append(features)
                else:
                    logger.warning("Feature is not found")
            return data
        except Exception as e:
            logger.error(f"Error while loading data from Redis {e}")
            raise CustomException(str(e))
        
    def prepare_data(self):
        try:
            entity_ids = self.feature_store.get_all_entity_ids()

            train_entity_ids, test_entity_ids = train_test_split(entity_ids,test_size=0.2,random_state=40)

            train_data = self.load_data_from_redis(train_entity_ids)
            test_data = self.load_data_from_redis(test_entity_ids)

            train_df = pd.DataFrame(train_data)
            test_df = pd.DataFrame(test_data)

            y_train = train_df['Exited']
            y_test = test_df['Exited']

            cols_to_drop = ['CustomerId','Surname','Exited']

            x_train = train_df.drop(cols_to_drop,axis=1)
            logger.info(x_train.columns)
            x_test = test_df.drop(cols_to_drop,axis=1)
    

            logger.info("Train and Test Split Completed")
            return x_train, x_test, y_train, y_test
        except Exception as e:
            logger.error(f"Error in preparing data for training {e}")
            raise CustomException(str(e))
            
    def hyperparameter_tuning(self, x_train, y_train):
        try:
            params = {
                'n_estimators':[50,100,200],
                'max_depth':[3,5,7],
                'learning_rate':[0.01,0.1,0.2]
            }
            xgb_model = xgb.XGBClassifier(objective='binary:logistic')
            grid_search = GridSearchCV(estimator=xgb_model,param_grid=params, cv=5, scoring='accuracy',n_jobs=-1)
            grid_search.fit(x_train, y_train)

            logger.info(f"Best parameters : {grid_search.best_params_}")
            return grid_search.best_estimator_
        except Exception as e:
            logger.error(f"Error in hyperparameter tuning {e}")
            raise CustomException(str(e))
        
    def train_and_evaluate(self, x_train, y_train, x_test, y_test):
        try:
            best_xgb = self.hyperparameter_tuning(x_train, y_train)
            y_pred = best_xgb.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            logger.info(f"Accuracy is {accuracy} ")

            self.save_model(best_xgb)
            return accuracy
        except Exception as e:
            logger.error(f"Error while model training {e}")
            raise CustomException(str(e))
        
    def save_model(self, model):
        try:
            model_filename = f"{self.model_save_path}xgb_classifier.pkl"

            with open(model_filename, 'wb') as model_file:
                pickle.dump(model, model_file)

            logger.info(f"Model saved at {model_filename}")
        except Exception as e:
            logger.error(f"Error while saving the model {e}")
            raise CustomException(str(e))
        
    def run(self):
        try:
            logger.info("Starting Model Training..")
            x_train, x_test, y_train, y_test = self.prepare_data()
            accuracy = self.train_and_evaluate(x_train, y_train, x_test, y_test)

            logger.info("End of Model Training")
        except Exception as e:
            logger.info(f"Error while model training {e}")
            raise CustomException(str(e))
        
if __name__=="__main__":
    feature_store = RedisFeatureStore()
    model_trainer = ModelTraining(feature_store)
    model_trainer.run()







        
        






            
