import pandas as pd
from .downloader import GeoDownloader

class GeoLocator:
    """This class returns a random address based on the country code from data downloaded from www.geonames.org
       Query interface for GeoNames postal code data"""
   
    #List of headers for data
    COLUMN_NAMES = [
        'country_code', 'postal_code', 'place_name',
        'admin_name1', 'admin_code1', 'admin_name2',
        'admin_code2', 'admin_name3', 'admin_code3',
        'latitude', 'longitude', 'accuracy'
    ]

    def __init__(self, country_codes, data_dir='data', max_age_days=30):
        self._downloader = GeoDownloader(data_dir, max_age_days)
        self._frames = {}

        for code in country_codes:
            self._frames[code] = self._load_country(code)

    def _load_country(self, country_code, force=False):
        txt_path = self._downloader.get_country_file(country_code, force=force)
        return self._parse(txt_path)
        
    def _parse(self, txt_path):
        return pd.read_csv(
            txt_path, sep='\t', header=None, names=self.COLUMN_NAMES,
            dtype=str, low_memory=False
        )
    
    def get_random_location(self, country_code):
        if country_code not in self._frames:
            raise ValueError(f"Country '{country_code}' not loaded.")
        row = self._frames[country_code].sample(1).iloc[0]
        return {
            'country': row['country_code'],
            'postal_code': row['postal_code'],
            'city': row['place_name'],
            'state_province': row['admin_name1'],
            'state_abbr': row['admin_code1'],
            'latitude': row['latitude'],
            'longitude': row['longitude'],
        }
    
    def add_country(self, country_code):
        if country_code not in self._frames:
            self._frames[country_code] = self._load_country(country_code)
    
    def refresh(self, country_code=None):
        codes = [country_code] if country_code else list(self._frames.keys())
        for code in codes:
            self._frames[code] = self._load_country(code, force=True)
    
    def __repr__(self):
        countries = ','.join(sorted(self._frames.keys()))
        total = sum(len(df) for df in self._frames.values())
        return f"GeoLocator(countries=[{countries}], records={total})"
    
    def __len__(self):
        return sum(len(df) for df in self._frames.values())
    
    def __contains__(self, country_code):
        return country_code in self._frames
    
    def __getitem__(self, country_code):
        if country_code not in self._frames:
            raise KeyError(f"Country '{country_code}' not loaded")
        return self._frames[country_code]
    
    def __iter__(self):
        return iter(self._frames)