import pytest
from faker import Faker

from src.domain.exceptions.messages import TextTooLongException, EmptyTextException
from src.domain.value_objects.messages import Text, Title


def test_create_text_success(faker: Faker):
    value = faker.text()[:100]
    text = Text(value=value)
    assert text.value == value


def test_create_text_empty():
    with pytest.raises(EmptyTextException):
        Text('')


def test_create_title_success(faker: Faker):
    value = faker.text()[:100]
    title = Title(value=value)
    assert title.value == value


def test_create_title_empty():
    with pytest.raises(EmptyTextException):
        Title('')


def test_create_title_too_long(faker: Faker):
    with pytest.raises(TextTooLongException):
        value = faker.text(max_nb_chars=300)
        Title(value=value)
