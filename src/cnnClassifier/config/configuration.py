

import os
from box.exceptions import BoxValueError
from cnnClassifier import logger
from cnnClassifier.entity.config_entity import (DataIngestionConfig,
                                                PrepareBaseModelConfig)

## This is a unit test that need to be improved
import unittest
# Compatibility for different Python versions
if not hasattr(unittest.TestCase, 'assertRaisesRegexp'):
    unittest.TestCase.assertRaisesRegexp = unittest.TestCase.assertRaisesRegex


##  This is what is in the video
from cnnClassifier.constants import *
from cnnClassifier.utils.common import read_yaml, create_directories

## Class definition
class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):
        try:
            # Verify files exist
            if not os.path.exists(config_filepath):
                raise FileNotFoundError(f"Config file not found at {config_filepath}")
            if not os.path.exists(params_filepath):
                raise FileNotFoundError(f"Params file not found at {params_filepath}")
                
            self.config = read_yaml(config_filepath)
            self.params = read_yaml(params_filepath)
            
            # Verify required fields
            if not self.config.get('artifacts_root'):
                raise ValueError("artifacts_root not found in config")
                
            create_directories([self.config.artifacts_root])
            
        except BoxValueError as e:
            logger.error(f"Configuration error in YAML parsing: {e}")
            raise
        except Exception as e:
            logger.error(f"Error in configuration: {str(e)}")
            raise


    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )

        return data_ingestion_config


    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model 
        create_directories([config.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_include_top=self.params.INCLUDE_TOP,
            params_weights=self.params.WEIGHTS,
            params_classes=self.params.CLASSES
        )

        return prepare_base_model_config