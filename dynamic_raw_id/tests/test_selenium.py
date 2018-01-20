from __future__ import unicode_literals

import time
from logging import getLogger
from unittest import skipIf

import django
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import skipIfDBFeature

from dynamic_raw_id.tests.testapp.models import CharPrimaryKeyModel, \
    DirectPrimaryKeyModel, TestModel

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

logger = getLogger(__file__)

IS_DJANGO_18 = django.get_version().startswith('1.8')

def get_webdriver():
    from selenium.webdriver.firefox.webdriver import WebDriver
    return WebDriver()

class BaseSeleniumTests(StaticLiveServerTestCase):
    def setUp(self):
        super(BaseSeleniumTests, self).setUp()
        self.admin_user = 'jane'
        self.jane = User.objects.create_superuser('jane', 'jane@example.com', 'foobar')

        # More users for testing m2m relations
        self.tick = User.objects.create_user('tick', 'tick@example.com', 'foobar')
        self.trick = User.objects.create_user('trick', 'trick@example.com', 'foobar')
        self.track = User.objects.create_user('track', 'track@example.com', 'foobar')

        self.add_testmodel_url = '{0}{1}'.format(
            self.live_server_url, reverse('admin:testapp_testmodel_add'))

    @classmethod
    def setUpClass(cls):
        super(BaseSeleniumTests, cls).setUpClass()
        cls.wd = get_webdriver()
        cls.wd.implicitly_wait(10)
        cls.wd.set_page_load_timeout(10)

    @classmethod
    def tearDownClass(cls):
        cls.wd.quit()
        super(BaseSeleniumTests, cls).tearDownClass()

    def _wait(self, seconds=10):
        """
        Explicit wait, use it for debugging, not to overcome timing issues.
        """
        time.sleep(seconds)

    def _login_admin(self):
        """
        Login into the Django Admin with our Admin credentials
        :return:
        """
        self.wd.get('{0}{1}'.format(self.live_server_url, reverse('admin:index')))
        self.wd.find_element_by_name("username").send_keys('jane')
        self.wd.find_element_by_name("password").send_keys('foobar')
        self.wd.find_element_by_css_selector('input[type=submit]').click()

        # Wait until index page is loaded
        self.wd.find_element_by_link_text("Testapp")

    def _goto_add_page(self):
        """
        Go to the "TestApp" Add form page
        :return:
        """
        self.wd.get(self.add_testmodel_url)

    def _click_lookup_and_choose(self, row_id, link_text):
        """
        Clicks on the little glass icon selector and waits until the
        selector popup opens. Then it selects the given link text.
        """
        # Click on the Glass icon with the id <lookup_id>.
        self.wd.find_element_by_id('lookup_id_{0}'.format(row_id)).click()

        #  Activate the popup window with the `window.name = <window_id>`
        self.wd.switch_to.window(self.wd.window_handles[1])

        # Click on the username/line item with the link text <link_text>.
        self.wd.find_element_by_link_text(link_text).click()

        # Activate default window
        self.wd.switch_to.window(self.wd.window_handles[0])

    def _save_and_continue(self):
        """
        Hit "Save and continue editing" and make sure
        the response has no error.
        """
        self.wd.find_element_by_css_selector('input[name=_continue]').click()

        # Wait until page is loaded and success message is displayed
        self.assertTrue(self.wd.find_element_by_css_selector('li.success').is_displayed())

    def test_dynamic_foreignkey(self):
        """
        dynamic_raw_id on a regular ForeignKey field
        """
        row_id = 'dynamic_raw_id_fk' # The admin row ID/indicator we test
        user_to_test = self.tick

        self._login_admin()
        self._goto_add_page()
        self._click_lookup_and_choose(row_id, user_to_test.username)

        # user id is inside the input field
        self.assertEqual(self.wd.find_element_by_id(
            'id_{0}'.format(row_id)).get_property('value'), str(user_to_test.pk))

        # username is displayed next to the element
        self.assertEqual(self.wd.find_element_by_id(
            '{0}_dynamic_raw_id_label'.format(row_id)).text, user_to_test.username)

        self._save_and_continue()

    def test_dynamic_foreignkey_limited(self):
        """
        dynamic_raw_id on a regular ForeignKey field with `limit_choices_to`
        """
        row_id = 'dynamic_raw_id_fk_limited' # The admin row ID/indicator we test
        user_to_test = self.jane

        self._login_admin()
        self._goto_add_page()
        self._click_lookup_and_choose(row_id, user_to_test.username)

        # user id is inside the input field
        self.assertEqual(self.wd.find_element_by_id(
            'id_{0}'.format(row_id)).get_property('value'), str(user_to_test.pk))

        # username is displayed next to the element
        self.assertEqual(self.wd.find_element_by_id(
            '{0}_dynamic_raw_id_label'.format(row_id)).text, user_to_test.username)

        self._save_and_continue()

    def test_dynamic_many2many(self):
        """
        dynamic_raw_id on a many2many field
        """
        row_id = 'dynamic_raw_id_many' # The admin row ID/indicator we test

        self._login_admin()
        self._goto_add_page()

        self._click_lookup_and_choose(row_id, self.tick.username)
        self._click_lookup_and_choose(row_id, self.trick.username)
        self._click_lookup_and_choose(row_id, self.track.username)

        # the three user ids are inside the element
        expected = '{0},{1},{2}'.format(self.tick.pk, self.trick.pk, self.track.pk)
        self.assertEqual(self.wd.find_element_by_id(
            'id_{0}'.format(row_id)).get_property('value'), expected)

        # tick, trick and track are now be displayed next to the form field
        # This is actually a bug, same ID for multiple elements
        expected = '{0},  {1},  {2}'.format(
            self.tick.username, self.trick.username, self.track.username)
        self.assertEqual(self.wd.find_element_by_id(
            '{0}_dynamic_raw_id_label'.format(row_id)).text, expected)

        self._save_and_continue()

    def test_dynamic_direct_charfield(self):
        """
        dynamic_raw_id on a custom Model with a CharField
        """
        row_id = 'dynamic_raw_id_fk_char_pk' # The admin row ID/indicator we test
        username = 'Hello World'

        # Add a test model instances
        custom_obj = CharPrimaryKeyModel.objects.create(chr='Hello World')

        self._login_admin()
        self._goto_add_page()
        self._click_lookup_and_choose(row_id, username)

        # object id is inside the input field
        self.assertEqual(self.wd.find_element_by_id(
            'id_{0}'.format(row_id)).get_property('value'), str(custom_obj.pk))

        # object label is now be displayed next to the form field
        self.assertEqual(self.wd.find_element_by_id(
            '{0}_dynamic_raw_id_label'.format(row_id)).text, custom_obj.chr)

        self._save_and_continue()

    def test_dynamic_direct_integerfield(self):
        """
        dynamic_raw_id on a custom Model with an IntegerField
        """
        row_id = 'dynamic_raw_id_fk_direct_pk' # The admin row ID/indicator we test
        username = '12345'

        # Add a test model instances
        custom_obj = DirectPrimaryKeyModel.objects.create(num=12345)

        self._login_admin()
        self._goto_add_page()
        self._click_lookup_and_choose(row_id, username)

        # object id is inside the input field
        self.assertEqual(self.wd.find_element_by_id(
            'id_{0}'.format(row_id)).get_property('value'), str(custom_obj.pk))

        # object label is now be displayed next to the form field
        self.assertEqual(self.wd.find_element_by_id(
            '{0}_dynamic_raw_id_label'.format(row_id)).text, str(custom_obj.num))

        self._save_and_continue()

    # Django 1.8 has some odd behavior with Selenium where the
    # click event on the Glass icon in the filter does not work.
    # It's working fine in a manual test. Since Django 1.8 is at the end of
    # it's lifetime, we simply skip it.
    @skipIf(IS_DJANGO_18, 'Dynamic Filter and Selenium dont work together in Django 1.8')
    def test_dynamic_filter(self):
        """
        Create multiple dynamic_raw_id_fk instances
        and then trigger the change list filter.
        """
        # Some Test instances
        TestModel.objects.create(dynamic_raw_id_fk=self.tick)
        TestModel.objects.create(dynamic_raw_id_fk=self.trick)
        TestModel.objects.create(dynamic_raw_id_fk=self.track)

        self._login_admin()

        # Go to the change list page.
        changelist_url = '{0}{1}'.format(
            self.live_server_url, reverse('admin:testapp_testmodel_changelist'))
        self.wd.get(changelist_url)

        # tick, trick and track are visible in the changelist table
        self.assertTrue(self.wd.find_element_by_link_text('tick').is_displayed())
        self.assertTrue(self.wd.find_element_by_link_text('trick').is_displayed())
        self.assertTrue(self.wd.find_element_by_link_text('track').is_displayed())

        # Click on the filter glass icon and choose 'trick'
        self._click_lookup_and_choose('dynamic_raw_id_fk', 'trick')

        # Click the submit icon of the filter panel
        self.wd.find_element_by_css_selector('#changelist-filter input[type=submit]').click()

        # Only "trick" is visible in the changelist table
        self.wd.implicitly_wait(0)
        self.assertTrue(self.wd.find_element_by_link_text('trick').is_displayed())
        self.assertTrue(len(self.wd.find_elements_by_link_text('tick')) == 0)
        self.assertTrue(len(self.wd.find_elements_by_link_text('track')) == 0)
