import time
import zipfile
import urllib.request
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class GeoDownloader:
    """Downloads and manages GeoNames postal code files."""

    BASE_URL = 'https://download.geonames.org/export/zip/'
    FULL_ZIP_COUNTRIES = {'CA', 'GB', 'NL'}

    def __init__(self, data_dir='data', max_age_days=30):
        self.data_dir = Path(data_dir)
        self.max_age_days = max_age_days
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def get_country_file(self, country_code, force=False):
        """Return path to country file, downloading if needed."""
        file_name = f"{country_code}_full.txt" if country_code in self.FULL_ZIP_COUNTRIES else f"{country_code}.txt"
        
        txt_path = self.data_dir / file_name

        if not force and not self._is_stale(txt_path):
            return txt_path
        
        self._download_and_extract(country_code)
        return txt_path
        
    def _is_stale(self, txt_path):
        txt_path = Path(txt_path)
        if not txt_path.exists():
            return True
        file_age = time.time() - txt_path.stat().st_mtime
        return file_age > (self.max_age_days * 86400)
    
    def _download_and_extract(self, country_code):
        zip_name = f"{country_code}_full.csv.zip" if country_code in self.FULL_ZIP_COUNTRIES else f"{country_code}.zip"
        zip_path = self.data_dir / zip_name
        url = f"{self.BASE_URL}{zip_name}"

        try:

            logger.info(f"Downloading {url}...")
            urllib.request.urlretrieve(url, zip_path)
            logger.info(f"Downloaded {zip_name} to {self.data_dir}")
        except Exception:
            logger.exception(f"Failed to download {url}")
            raise
        
        try:
            logger.info(f"Extracting {zip_name} to {self.data_dir}...")
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(self.data_dir)
            logger.info(f"Extracted {zip_name} to {self.data_dir} successfully")
        except zipfile.BadZipFile:
            logger.error(f"Downloaded file is not a valid zip: {zip_path}")
            zip_path.unlink(missing_ok=True) # Remove corrupt file so next run retries
            raise

