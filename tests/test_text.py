from guiderail.text import STOPWORDS, stem, tokenize


def test_plural_and_singular_share_a_stem():
    assert stem("gloves") == stem("glove")
    assert stem("surfaces") == stem("surface")
    assert stem("masks") == stem("mask")
    assert stem("vaccines") == stem("vaccine")


def test_short_words_and_numbers_untouched():
    assert stem("use") == "use"
    assert stem("2024") == "2024"


def test_tokenize_drops_stopwords_and_lowercases():
    assert tokenize("The Hands ARE washed") == ["hand", "wash"]


def test_negations_are_kept():
    for word in ("not", "no", "never", "without"):
        assert word not in STOPWORDS
    assert "never" in tokenize("Never reuse gloves")


def test_tokenize_is_deterministic():
    text = "Wear gloves, a gown and eye protection."
    assert tokenize(text) == tokenize(text)
