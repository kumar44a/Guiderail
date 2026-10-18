import hashlib

import numpy as np

from guiderail.embeddings import DIM, embed, embed_batch

# Golden value: if this changes, vectors changed and every index hash changes with it.
GOLDEN_TEXT = "hand hygiene before touching a patient"
GOLDEN_SHA256 = "3fe34b59ce2507d8fa595988cd078aee89c48b6283de558fce7dbf0621d4dc69"


def test_shape_dtype_and_unit_norm():
    v = embed("wear gloves and a gown")
    assert v.shape == (DIM,) and DIM == 256
    assert v.dtype == np.float32
    assert abs(float(np.linalg.norm(v)) - 1.0) < 1e-5


def test_same_text_gives_identical_bytes():
    assert embed("clean high-touch surfaces").tobytes() == embed("clean high-touch surfaces").tobytes()


def test_golden_vector_hash_is_stable():
    assert hashlib.sha256(embed(GOLDEN_TEXT).tobytes()).hexdigest() == GOLDEN_SHA256


def test_empty_and_stopword_only_text_gives_zero_vector():
    assert not embed("").any()
    assert not embed("the of and").any()


def test_related_text_is_closer_than_unrelated_text():
    query = embed("how long should I rub alcohol hand rub")
    related = embed("use an alcohol-based hand rub for 20 to 30 seconds")
    unrelated = embed("store frozen vaccines between minus 50 and minus 15 degrees")
    assert float(query @ related) > float(query @ unrelated)


def test_batch_matches_single():
    texts = ["wear gloves", "wash hands"]
    batch = embed_batch(texts)
    assert batch.shape == (2, DIM)
    assert np.array_equal(batch[0], embed(texts[0]))


def test_empty_batch():
    assert embed_batch([]).shape == (0, DIM)
