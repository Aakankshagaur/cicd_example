from example.hello import greet


def test_default_greeting() -> None:
    assert greet() == "Hello, World!"


def test_named_greeting() -> None:
    assert greet("Karen") == "Hello, Karen!"