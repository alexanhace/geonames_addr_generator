import pytest
from geonames_addr.locator import GeoLocator

class TestGeoLocatorInit:
    """Tests for GeoLocator initialization."""

    def test_loads_data_from_file(self, sample_geonames_file):
        locator = GeoLocator.__new__(GeoLocator)  #Create without __init__
        locator._downloader = None
        locator._frames = {}
        # Directly test the parsing
        df = locator._parse(sample_geonames_file)
        assert len(df) == 6

    def test_raises_on_missing_file(self, tmp_path):
        fake_path = tmp_path / "nonexistent.txt"
        locator = GeoLocator.__new__(GeoLocator)
        with pytest.raises(FileNotFoundError):
            locator._parse(fake_path)

class TestGetRandomLocation:
    """Tests for the get_random_location method."""

    @pytest.fixture
    def locator(self, sample_geonames_file):
        """Create a locator with test data loaded."""
        locator = GeoLocator.__new__(GeoLocator)
        locator._frames = {}
        df = locator._parse(sample_geonames_file)
        for code in df['country_code'].unique():
            locator._frames[code] = df[df['country_code']==code]
        return locator
    
    def test_returns_location_dict(self,locator):
        loc = locator.get_random_location('US')
        assert isinstance(loc, dict)
        assert 'country' in loc
        assert 'city' in loc
        assert 'postal_code' in loc
        assert 'state_province' in loc
        assert 'latitude' in loc
        assert 'longitude' in loc

    def test_filters_by_country(self, locator):
        loc = locator.get_random_location('DE')
        assert loc['country'] == 'DE'

    def test_us_locations_are_valid(self, locator):
        loc = locator.get_random_location('US')
        assert loc['country'] == 'US'
        assert loc['city'] in ['New York', 'Berverly Hills', 'Chicago']

    def test_rasises_on_unknown_country(self, locator):
        with pytest.raises(ValueError, match="not loaded"):
            locator.get_random_location('XX')

class TestAddCountry:
    """Tests for dynamically adding countries."""

    def test_add_country_makes_it_available(self, tmp_path):
        # Create two separate country files
        us_file = tmp_path / "US.txt"
        us_file.write_text(
            "US\t10001\tNew York\tNew York\tNY\tNew York\t061\t\t\t40.7484\t-73.9967\t4\n"
        )
        de_file = tmp_path / "DE.txt"
        de_file.write_text(
            "DE\t10115\tBerlin\tBerlin\tBE\t\t\t\t\t52.5323\t13.3846\t4\n"
        )

        #Start with only US loaded
        locator = GeoLocator(['US'], data_dir=tmp_path)
        assert 'US' in locator
        assert 'DE' not in locator

        #Now add Germany
        locator.add_country('DE')
        assert 'DE' in locator
        loc = locator.get_random_location('DE')
        assert loc['country'] == 'DE'

    def test_add_country_ignores_existing_country(self, tmp_path):
        us_file = tmp_path / "US.txt"
        us_file.write_text(
            "US\t10001\tNew York\tNew York\tNY\tNew York\t061\t\t\t40.7484\t-73.9967\t4\n"
        )

        locator = GeoLocator(['US'], data_dir=tmp_path)
        original_len = len(locator)
        
        #Adding the same data should not change the object
        locator.add_country('US')
        assert len(locator) == original_len
