import names
import pytest

def test_make_full_name():
    assert names.make_full_name("Marie","Toussaint") == "Toussaint; Marie"
    assert names.make_full_name("Olivier","Toussaint") == "Toussaint; Olivier"
    assert names.make_full_name("George","Washington") == "Washington; George"
    assert names.make_full_name("Martha","Washington") == "Washington; Martha"

def test_extract_family_name():
    assert names.extract_family_name("Toussaint; Marie") == "Toussaint"
    assert names.extract_family_name("Toussaint; Olivier") == "Toussaint"
    assert names.extract_family_name("Washington; George") == "Washington"
    assert names.extract_family_name("Washington; Martha") == "Washington"

def test_extract_given_name():
    assert names.extract_given_name("Toussaint; Marie") == "Marie"
    assert names.extract_given_name("Toussaint; Olivier") == "Olivier"
    assert names.extract_given_name("Washington; George") == "George"
    assert names.extract_given_name("Washington; Martha") == "Martha"

pytest.main(["-v", "--tb=line", "-rN", __file__])