import time
import os 
from geonames_addr.downloader import GeoDownloader

class TestStalenessCheck:
    """Tests for the file staleness logic"""

    def test_missing_file_is_stale(self, tmp_path):
        dl = GeoDownloader(data_dir=tmp_path)
        fake_path = tmp_path / "nonexistent.txt"
        assert dl._is_stale(fake_path) is True

    def test_fresh_file_is_not_stale(self,tmp_path):
        dl = GeoDownloader(data_dir=tmp_path, max_age_days=30)
        file_path = tmp_path / "test.txt"
        file_path.write_text("data")
        assert dl._is_stale(file_path) is False

    def test_old_file_is_stale(self, tmp_path):
        dl = GeoDownloader(data_dir=tmp_path, max_age_days=1)
        file_path = tmp_path / "test.txt"
        file_path.write_text("data")

        # Set modification time to 2 days ago
        two_days_ago = time.time() - (2 *86400)
        os.utime(file_path,(two_days_ago, two_days_ago))

        assert dl._is_stale(file_path) is True

class TestDataDir:
    """Tests for data directory management."""

    def test_creates_data_dir_if_missing(self, tmp_path):
        new_dir = tmp_path / "new_data_dir"
        assert not new_dir.exists()
        dl = GeoDownloader(data_dir=new_dir)
        assert new_dir.exists()

    def test_accepts_existing_dir(self, tmp_path):
        dl = GeoDownloader(data_dir=tmp_path)
        assert dl.data_dir == tmp_path

class TestGetCountryFileCheck:
    """ Tests if path is returned correctly."""
    
    def test_return_correct_file_name(self, tmp_path):
        dl = GeoDownloader(data_dir=tmp_path)

        #Get existing file
        us_file_loc = tmp_path / "US.txt"
        file_loc = dl.get_country_file('US',False)
        assert file_loc == us_file_loc

