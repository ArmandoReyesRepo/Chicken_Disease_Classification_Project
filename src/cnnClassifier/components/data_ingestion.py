import os
import urllib.request as request
import zipfile
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
import requests
import certifi
from pathlib import Path
from cnnClassifier.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        """Download file from URL if not already present"""
        local_path = Path(self.config.local_data_file)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        if not local_path.exists():
            try:
                logger.info(f"📥 Downloading from {self.config.source_URL} ...")

                with requests.get(self.config.source_URL, stream=True, verify=certifi.where(), timeout=30) as r:
                    r.raise_for_status()  # raises HTTPError for bad status codes

                    with open(local_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

                size = local_path.stat().st_size
                logger.info(f"✅ Downloaded {local_path} (size: {size/1024:.2f} KB)")

            except requests.exceptions.SSLError:
                raise Exception(
                    f"SSL verification failed for {self.config.source_URL}. "
                    "Check if you used a GitHub 'blob' link instead of a 'raw' link."
                )
            except requests.exceptions.HTTPError as e:
                raise Exception(
                    f"HTTP error {e.response.status_code} while downloading {self.config.source_URL}"
                )
            except Exception as e:
                raise Exception(f"Failed to download {self.config.source_URL}: {e}")

        else:
            logger.info(f"File already exists at {local_path} (size: {get_size(local_path)} KB)")



    
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)