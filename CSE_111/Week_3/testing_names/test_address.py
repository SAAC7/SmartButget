import address
import pytest
def test_extract_city():
    assert address.extract_city("525 S Center St, Rexburg, ID 83460")=="Rexburg"
def test_extract_state():
    assert address.extract_state("525 S Center St, Rexburg, ID 83460")=="ID"
def test_extract_zipcode():
    assert address.extract_zipcode("525 S Center St, Rexburg, ID 83460")=="83460"

pytest.main(["-v", "--tb=line", "-rN", __file__])