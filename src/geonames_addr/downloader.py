import time
import zipfile
import urllib.request
from pathlib import Path

class GeoDownloader:
    """Downloads and manages GeoNames postal code files."""

    BASE_URL = 'https://download.geonames.org/export/zip/'

    def __init__(self, data_dir='data', max_age_days=30):
        self.data_dir = Path(data_dir)
        self.max_age_days = max_age_days
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def get_country_file(self, country_code, force=False):
        """Return path to country file, downloading if needed."""
        txt_path = self.data_dir / f"{country_code}.txt"

        if not force and not self._is_stale(txt_path):
            return txt_path
        
        self._downlaod_and_extract(country_code)
        return txt_path
        
    def _is_stale(self, txt_path):
        if not txt_path.exists():
            return True
        file_age = time.time() - txt_path.stat().st_mtime
        return file_age > (self.max_age_days * 86400)
    
    def _downlaod_and_extract(self, country_code):
        FULL_ZIP_COUNTRIES = {'CA', 'GB', 'NL'}

        zip_name = f"{country_code}_full.csv.zip" if country_code in FULL_ZIP_COUNTRIES else f"{country_code}.zip"
            
        zip_path = self.data_dir / zip_name
        url = f"{self.BASE_URL}{zip_name}"

        print(f"Downloading {url}...")
        local_file, headers = urllib.request.urlretrieve(url, zip_path)
        print(f"File downloaded to: {local_file}")

        print(f"Extracting {zip_name} to {self.data_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(self.data_dir)
        print(f"File unzipped to {self.data_dir}")

