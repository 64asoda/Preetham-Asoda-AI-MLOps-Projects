import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from src.feature_store import RedisFeatureStore
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *

logger = get_logger(__name__)

class DataPreProcessing:
    def __init__(self,train_data_path, test_data_path, feature_store : RedisFeatureStore):
        self.train_data_path = train_data_path
        self.test_data_path = test_data_path
        self.data = None
        self.test_data = None
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None

        self.x_resampled = None
        self.y_resampled = None

        self.feature_store = feature_store
        logger.info("Data Processing is initialized")

    def load_data(self):
        try:
            self.data = pd.read_csv(self.train_data_path)
            self.test_data = pd.read_csv(self.test_data_path)
            logger.info("Successfully read the data")
        except Exception as e:
            logger.error(f"Error while reading data {e}")
            raise CustomException(str(e))
        
    def preprocess_data(self):
        try:
            self.data = pd.concat([self.data, pd.get_dummies(self.data['Geography'],prefix='Geography',drop_first=True)],axis=1).drop('Geography',axis=1)
            self.data['Gender'] = self.data['Gender'].map({'Female':0,'Male':1})
            self.data['Age'] = np.where(self.data['Age']>70,70,self.data['Age'])
            self.data['Balance'] = np.where(self.data['Balance']>200000,200000,self.data['Balance'])
            self.data['NumOfProducts'] = np.where(self.data['NumOfProducts']>3,3,self.data['NumOfProducts'])
            
            logger.info("Data Preprocessing done...")

        except Exception as e:
            logger.error(f"Error while preprocessing data {e}")
            raise CustomException(str(e))
        

    def store_feature_in_redis(self):
        try:
            batch_data = {}
            for index,row in self.data.iterrows():
                entity_id = row['CustomerId']
                features = {
                    "CustomerId" : row['CustomerId'],
                    "Surname" : row['Surname'],
                    "CreditScore" : row["CreditScore"],
                    "Gender" : row["Gender"],
                    "Age" : row["Age"],
                    "Tenure": row["Tenure"],
                    "Balance" : row["Balance"],
                    "NumOfProducts" : row["NumOfProducts"],
                    "HasCrCard" : row["HasCrCard"],
                    "IsActiveMember" : row["IsActiveMember"],
                    "EstimatedSalary" : row["EstimatedSalary"],
                    "Exited" : row["Exited"],
                    "Geography_Germany" : row["Geography_Germany"],
                    "Geography_Spain" : row["Geography_Spain"],
                }
                batch_data[entity_id] = features
            self.feature_store.store_batch_features(batch_data)
            logger.info("Data has been loaded into the Feature Store")
        except Exception as e:
            logger.error(f"Error while feature storing data {e}")
            raise CustomException(str(e))
        
    def retrieve_feature_redis_store(self,entity_id):
        features = self.feature_store.get_features(entity_id)
        if features:
            return features
        return None
    
    def run(self):
        try:
            logger.info("Start of Data Processing Pipeline")
            self.load_data()
            self.preprocess_data()
            self.store_feature_in_redis()
            
            logger.info("End of Data Preprocessing")

        except Exception as e:
            logger.error(f"Error during Data Processing {e}")
            raise CustomException(str(e))
        

if __name__=="__main__" :
    feature_store = RedisFeatureStore()
    data_processor = DataPreProcessing(TRAIN_PATH, TEST_PATH, feature_store)
    data_processor.run()

    print(data_processor.retrieve_feature_redis_store(entity_id=15619304))





        
    



                                  

