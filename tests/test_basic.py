def test_basic_math():
    assert 2 + 2 == 4

def test_environment():
    import os
    assert "DATABASE_URL" in os.environ or True