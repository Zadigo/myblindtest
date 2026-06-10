from django.test import TestCase
from blindtest.youtube_search.query import QueryDict, QueryList
from blindtest.youtube_search.base import BaseSearch
from faker import Faker

fake_instance = Faker()

item = {
    'age': fake_instance.random_int(min=18, max=22),
    'name': 'Kendall',
    'address': {
        'country': fake_instance.country(),
        'city': fake_instance.city(),
        'details': {
            'number': fake_instance.random_int(min=1, max=50)
        }
    }
}

items = [item for _ in range(5)]


class TestQuery(TestCase):
    def test_instance(self):
        value = {'name': 'Kendall'}

        instance = QueryDict(value)

        self.assertIn('name', instance)
        self.assertEqual(instance['name'], 'Kendall')

        klass = instance.new(value)
        self.assertIsInstance(klass, QueryDict)

    def test_get_from_instance(self):
        value = {'name': 'Kendall', 'address': {'country': 'USA'}}

        instance = QueryDict(value)

        value = instance.get('address__country')
        self.assertEqual(value, 'USA')

        value = instance.get('name')
        self.assertEqual(value, 'Kendall')

    def test_check_from_instance(self):
        value = {'name': 'Kendall', 'address': {'country': 'USA'}}

        instance = QueryDict(value)

        result, return_value = instance.check('address', value)
        self.assertTrue(result)

        result, return_value = instance.check('name', value)
        self.assertFalse(result)


class TestQueryList(TestCase):
    def test_query_list(self):
        instance = QueryList(items)

        for item in instance.data:
            with self.subTest(item=item):
                self.assertTrue(isinstance(item, QueryDict))

        result = instance.filter('address__city__details')
        for item in result:
            with self.subTest(item=item):
                self.assertIn('number', item)


class TestBaseSearch(TestCase):
    def test_base_search(self):
        instance = BaseSearch('katy perry')
        instance.base_url = 'https://www.youtube.com/youtubei/v1/search'
        session, request = instance.create_request()

        self.assertIsNotNone(session)
        self.assertIsNotNone(request)

        response = session.send(request)

        self.assertTrue(response.status_code == 200)

        data = response.json()
        print(data)
