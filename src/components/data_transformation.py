import sys
import os
import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from dataclasses import dataclass

from src.exception import CustomException
from src.logger  import logging

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocesser_obj_file_path=os.path.join('artifact','proprocessor.pkl')
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_Config=DataTransformationConfig()
    def get_data_transformation_object(self):
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
            num_pipeline=Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ('Std', StandardScaler())
                    ]
                )
        
            cat_pipeline=Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot', OneHotEncoder()),
                    ('Std', StandardScaler(with_mean=False))
                    ]
                )
            logging.info(f"Numerical Columns :{numerical_columns}")
            logging.info(f"Catgorical columns :{categorical_columns}")
        
        
            preprocessor=ColumnTransformer(
                [
                    ('num pipeline', num_pipeline, numerical_columns),
                    ('cat pipeline', cat_pipeline, categorical_columns)
                ]
            )
        
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initite_data_transformation(self, train_path, test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path) 
            
            logging.info("read train and test dataset")
            
            logging.info('obtainig prepocessing object')
            
            preprocessing_obj=self.get_data_transformation_object()
            
            target_column_name='math_score'
            numerical_columns = ["writing_score", "reading_score"]
            
            input_feature_train_df=train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df=train_df[target_column_name]
            
            input_feature_test_df=test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df=test_df[target_column_name]
            
            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe.")
            
            
            input_feature_train_arr=preprocessing_obj.fit(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            
            train_arr=np.c_[
                input_feature_train_df , np.array(target_feature_train_df)
            ]
            test_arr=np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            logging.info(f"preporcessing object saved")
            
            save_object(
                file_path=self.data_transformation_Config.preprocesser_obj_file_path,
                obj=preprocessing_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_Config.preprocesser_obj_file_path
            )
            
               
        except Exception as e:
            raise CustomException(e, sys)    
        
