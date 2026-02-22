import pytest 

@pytest.fixture
def sample_geonames_file(tmp_path):
    """Create a small fake GeoNames file for testing"""
    content = (
        "US\t10001\tNew York\tNew York\tNY\tNew York\t061\t\t\t40.7484\t-73.9967\t4\n"
        "US\t90210\tBeverly Hills\tCalifornia\tCA\tLos Angeles\t037\t\t\t34.0901\t-118.4065\t4\n"
        "US\t60601\tChicago\tIllinois\tIL\tCook\t031\t\t\t41.8819\t-87.6278\t4\n"
        "DE\t10115\tBerlin\tBerlin\tBE\t\t\t\t\t52.5323\t13.3846\t4\n"
        "DE\t80331\tMunich\tBayern\tBY\t\t\t\t\t48.1374\t11.5755\t4\n"
        "FR\t75001\tParis\Île-de-France\tIDF\t\t\t\t\t48.8600\t2.3470\t4\n"
    )
    file_path = tmp_path / "test_countries.txt"
    file_path.write_text(content)
    return file_path

@pytest.fixture
def sample_us_file(tmp_path):
    """Create a US-only GeoNames file."""
    content = (
        "US\t10001\tNew York\tNew York\tNY\tNew York\t061\t\t\t40.7484\t-73.9967\t4\n"
        "US\t90210\tBeverly Hills\tCalifornia\tCA\tLos Angeles\t037\t\t\t34.0901\t-118.4065\t4\n"
        "US\t60601\tChicago\tIllinois\tIL\tCook\t031\t\t\t41.8819\t-87.6278\t4\n"
    )
    file_path = tmp_path /"US.txt"
    file_path.write_text(content)
    return file_path