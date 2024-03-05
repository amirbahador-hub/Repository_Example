from similarity.utils import clean_name


def test_clean_name_capital_letters():
    assert "amir_bahador_bahadori" == clean_name("Amir_Bahador_BAHADORI")


def test_clean_name_spaces():
    assert "amir_bahador_bahadori" == clean_name("Amir       Bahador Bahadori")


def test_clean_name_special_keywords():
    assert "amir_bahador_bahadori" == clean_name("Amir@!!!Bahador Bahadori")
