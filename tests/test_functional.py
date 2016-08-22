from bs4 import BeautifulSoup
from cms.api import add_plugin, create_page, publish_page
from django.contrib.auth.models import User
from django.test import TestCase, override_settings


class LocalNavigationFunctionalTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', email='', password='admin'
        )
        self.page = create_page('Hello world', 'base.html', 'en')

    def add_text(self, text):
        """
        Add a `TextPlugin` instance to the main page with the given text.
        """
        placeholder = self.page.placeholders.get(slot='content')
        add_plugin(placeholder, 'TextPlugin', 'en', body=text)
        # Immediately publish the changes
        publish_page(self.page, self.admin, 'en')

    def add_navigation(self):
        """
        Add a `LocalNavigationPlugin` instance to the main page with the given
        text.
        """
        placeholder = self.page.placeholders.get(slot='content')
        add_plugin(placeholder, 'LocalNavigationPlugin', 'en')
        publish_page(self.page, self.admin, 'en')

    def assertHeadingWithIdExists(self, id, content):
        """
        Assert that an HTML element exists in `content` with an HTML `id`
        attribute that starts with the given `id`.
        """
        soup = BeautifulSoup(content)
        headings = soup.select('[id^="{}"]'.format(id))
        self.assertEqual(
            len(headings), 1, "Couldn't find id {} in {}".format(id, content)
        )

    def assertElementExists(self, tag, content):
        """
        Assert that an HTML element exists in `content` with the `tag` HTML
        tag.
        """
        soup = BeautifulSoup(content)
        hrefs = soup.find_all(tag)
        self.assertEqual(
            len(hrefs), 1,
            "Couldn't find element {} in {}".format(tag, content)
        )

    def assertElementsAreUnique(self, tag, attribute, content):
        """
        Assert that the given `attribute` of all `tag` tags are unique
        together.
        """
        soup = BeautifulSoup(content)
        elements = soup.find_all(tag)
        attributes = {elem[attribute] for elem in elements}
        self.assertEqual(len(attributes), len(elements))

    def test_processor_adds_ids_to_elements(self):
        self.add_text('<h2>Hello</h2>')

        response = self.client.get('/en/')
        self.assertHeadingWithIdExists('hello-', response.content)

    @override_settings(CMS_LOCAL_NAVIGATION_NAV_ELEMENTS='h1')
    def test_nav_elements_setting_adds_ids_to_elements_set(self):
        self.add_text('<h1>Hello</h1><p>world</p>')

        response = self.client.get('/en/')
        self.assertHeadingWithIdExists('hello-', response.content)
        self.assertIn('<p>world</p>', response.content)

    def test_headings_are_present_in_menu(self):
        self.add_text('<h2>Hello</h2><p>world</p>')
        self.add_navigation()

        response = self.client.get('/en/')
        self.assertElementExists('a', response.content)

    def test_generated_ids_are_unique(self):
        self.add_text('<h2>Hello</h2>')
        self.add_text('<h2>Hello</h2>')
        self.add_navigation()

        response = self.client.get('/en/')
        self.assertElementsAreUnique('h2', 'id', response.content)

    def test_generated_links_are_unique(self):
        self.add_text('<h2>Hello</h2>')
        self.add_text('<h2>Hello</h2>')
        self.add_navigation()

        response = self.client.get('/en/')
        self.assertElementsAreUnique('a', 'href', response.content)

    def test_patched_elements_have_class_set(self):
        self.add_text('<h2>Hello</h2>')

        response = self.client.get('/en/')
        soup = BeautifulSoup(response.content)
        heading = soup.find_all('h2')
        self.assertEqual(len(heading), 1)
        self.assertEqual(heading[0]['class'], ['local-navigation-item'])

    def test_patched_elements_with_existing_class_get_class_appended(self):
        self.add_text('<h2 class="hello">Hello</h2>')

        response = self.client.get('/en/')
        soup = BeautifulSoup(response.content)
        heading = soup.find_all('h2')
        self.assertEqual(len(heading), 1)
        self.assertEqual(
            heading[0]['class'], ['hello', 'local-navigation-item']
        )
