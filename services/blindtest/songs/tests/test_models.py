import datetime

import pytest
from faker import Faker

from songs import models

fake = Faker()

@pytest.fixture
def artist():
    return models.Artist.objects.create(
        name=fake.word(),
        birthname=fake.first_name(),
        date_of_birth=fake.date_of_birth(),
    )


@pytest.mark.django_db
def test_age_property(artist):
    artist.date_of_birth = datetime.date(1990, 1, 1)
    artist.save()

    assert isinstance(artist.age, int)
    assert artist.age == datetime.date.today().year - 1990
