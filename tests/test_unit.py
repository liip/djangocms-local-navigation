from bs4 import BeautifulSoup
from django.test import TestCase

from djangocms_local_navigation.cms_plugin_processors import add_ids


class LocalNavigationUnitTestCase(TestCase):
    def assertElementsEqual(self, elements, comparison):
        self.assertEqual(
            [str(element) for element in elements],
            comparison
        )

    def test_add_ids_creates_unique_ids(self):
        text = '<h2>Hello</h2><h2>Hello</h2>'
        text_with_ids = add_ids(BeautifulSoup(text).find_all('h2'))

        self.assertElementsEqual(
            text_with_ids,
            ['<h2 id="hello">Hello</h2>', '<h2 id="hello-1">Hello</h2>']
        )

    def test_add_ids_creates_unique_ids_among_different_tags(self):
        text = '<h2>Hello</h2><p>Hello</p>'
        soup = BeautifulSoup(text)
        elements = soup.find_all(['h2', 'p'])
        add_ids(elements)

        self.assertEqual(
            ''.join(str(element) for element in soup.body),
            '<h2 id="hello">Hello</h2><p id="hello-1">Hello</p>'
        )

    def test_add_ids_adds_ids(self):
        text = '<h2>Hello</h2>'
        text_with_ids = add_ids(BeautifulSoup(text).find_all('h2'))

        self.assertElementsEqual(
            text_with_ids,
            ['<h2 id="hello">Hello</h2>']
        )

    def test_add_ids_adds_ids_only_to_given_tags(self):
        text = '<h2>Hello</h2><p>World</p>'
        soup = BeautifulSoup(text)
        elements = soup.find_all('p')
        add_ids(elements)

        self.assertEqual(
            ''.join(str(element) for element in soup.body),
            '<h2>Hello</h2><p id="world">World</p>'
        )

    def test_add_ids_returns_empty_text_on_empty_text(self):
        text = ''
        text_with_ids = add_ids(BeautifulSoup(text).find_all('h2'))

        self.assertEqual(text_with_ids, [])
