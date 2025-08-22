from cnnClassifier import logger
from cnnClassifier.pipeline.stage_01_data_ingestion import DataIngestionPipeline

## No longer required
## logger.info("Welcome to my custom log")

STAGE_NAME = "Data Ingestion stage"

class DataIngestionPipeline:
    def __init__(self):
        pass 
        
    def main(self):
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        config  = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<")


if __name__ == "__main__":
    try:
        obj = DataIngestionPipeline()
        obj.main()
    except Exception as e:
        logger.exception(e)
        raise e
        
