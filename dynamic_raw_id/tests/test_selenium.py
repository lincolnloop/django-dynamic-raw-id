import time
from logging import getLogger

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver

from dynamic_raw_id.tests.testapp.models import (
    CharPrimaryKeyModel,
    IntPrimaryKeyModel,
    ModelToTest,
    UUIDPrimaryKeyModel,
)

logger = getLogger(__name__)


class BaseSeleniumTests(StaticLiveServerTestCase):
    wd: FirefoxWebDriver = FirefoxWebDriver()

    def setUp(self) -> None:
        super().setUp()
        self.admin_user = "jane"
        self.jane = User.objects.create_superuser("jane", "jane@example.com", "foobar")

        # More users for testing m2m relations
        self.tick = User.objects.create_user("tick", "tick@example.com", "foobar")
        self.trick = User.objects.create_user("trick", "trick@example.com", "foobar")
        self.track = User.objects.create_user("track", "track@example.com", "foobar")

        self.add_modeltotest_url = "{}{}".format(
            self.live_server_url, reverse("admin:testapp_modeltotest_add")
        )

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.wd.implicitly_wait(10)
        cls.wd.set_page_load_timeout(10)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.wd.quit()
        super().tearDownClass()

    def _wait(self, seconds: int = 10) -> None:
        """
        Explicit wait, use it for debugging, not to overcome timing issues.
        """
        time.sleep(seconds)

    def _login_admin(self) -> None:
        """
        Login into the Django Admin with our Admin credentials
        :return:
        """
        self.wd.get("{}{}".format(self.live_server_url, reverse("admin:index")))
        self.wd.find_element(By.NAME, "username").send_keys("jane")
        self.wd.find_element(By.NAME, "password").send_keys("foobar")
        self.wd.find_element(By.CSS_SELECTOR, "input[type=submit]").click()

        # Wait until index page is loaded
        self.wd.find_element(By.LINK_TEXT, "TESTAPP")

    def _goto_add_page(self) -> None:
        """
        Go to the "TestApp" Add form page
        :return:
        """
        self.wd.get(self.add_modeltotest_url)

    def _click_lookup_and_choose(self, row_id: str, link_text: str) -> None:
        """
        Clicks on the little glass icon selector and waits until the
        selector popup opens. Then it selects the given link text.
        """
        # Click on the Glass icon with the id <lookup_id>.
        self.wd.find_element(By.ID, f"lookup_id_{row_id}").click()

        #  Activate the popup window with the `window.name = <window_id>`
        self.wd.switch_to.window(self.wd.window_handles[1])

        # Click on the username/line item with the link text <link_text>.
        self.wd.find_element(By.LINK_TEXT, link_text).click()

        # Activate default window
        self.wd.switch_to.window(self.wd.window_handles[0])

    def _save_and_continue(self) -> None:
        """
        Hit "Save and continue editing" and make sure
        the response has no error.
        """
        self.wd.find_element(By.CSS_SELECTOR, "input[name=_continue]").click()

        # Wait until page is loaded and success message is displayed
        assert self.wd.find_element(By.CSS_SELECTOR, "li.success").is_displayed()

    def test_dynamic_foreignkey(self) -> None:
        """
        dynamic_raw_id on a regular ForeignKey field
        """
        row_id = "dynamic_raw_id_fk"  # The admin row ID/indicator we test
        user_to_test = self.tick

        self._login_admin()
        self._goto_add_page()
        self._click_lookup_and_choose(row_id, user_to_test.username)

        # user id is inside the input field
        assert self.wd.find_element(By.ID, f"id_{row_id}").get_property("value") == str(
            user_to_test.pk
        )

        # username is displayed next to the element
        assert (
            self.wd.find_element(By.ID, f"{row_id}_dynamic_raw_id_label").text
            == user_to_test.username
        )

        self._save_and_continue()

    def test_dynamic_foreignkey_limited(self) -> None:
        """
        dynamic_raw_id on a regular ForeignKey field with `limit_choices_to`
        """
        row_id = "dynamic_raw_id_fk_limited"  # The admin row ID/indicator we test
        user_to_test = self.jane

        self._login_admin()
        self._goto_add_page()
        self._click_lookup_and_choose(row_id, user_to_test.username)

        # user id is inside the input field
        assert self.wd.find_element(By.ID, f"id_{row_id}").get_property("value") == str(
            user_to_test.pk
        )

        # username is displayed next to the element
        assert (
            self.wd.find_element(By.ID, f"{row_id}_dynamic_raw_id_label").text
            == user_to_test.username
        )

        self._save_and_continue()

    def test_dynamic_many2many(self) -> None:
        """
        dynamic_raw_id on a many2many field
        """
        row_id = "dynamic_raw_id_many"  # The admin row ID/indicator we test

        self._login_admin()
        self._goto_add_page()

        self._click_lookup_and_choose(row_id, self.tick.username)
        self._click_lookup_and_choose(row_id, self.trick.username)
        self._click_lookup_and_choose(row_id, self.track.username)

        # the three user ids are inside the element
        expected = f"{self.tick.pk},{self.trick.pk},{self.track.pk}"
        assert (
            self.wd.find_element(By.ID, f"id_{row_id}").get_property("value")
            == expected
        )

        # tick, trick and track are now be displayed next to the form field
        # This is actually a bug, same ID for multiple elements
        expected = (
            f"{self.tick.username},  {self.trick.username},  {self.track.username}"
        )
        assert (
            self.wd.find_element(By.ID, f"{row_id}_dynamic_raw_id_label").text
            == expected
        )

        self._save_and_continue()

    def test_dynamic_direct_charfield(self) -> None:
        """
        dynamic_raw_id on a custom Model with a CharField
        """
        row_id = "dynamic_raw_id_fk_char_pk"  # The admin row ID/indicator we test
        username = "Hello World"

        # Add a test model instances
        custom_obj = CharPrimaryKeyModel.objects.create(chr="Hello World")

        self._login_admin()
        self._goto_add_page()
        self._click_lookup_and_choose(row_id, username)

        # object id is inside the input field
        assert self.wd.find_element(By.ID, f"id_{row_id}").get_property("value") == str(
            custom_obj.pk
        )

        # object label is now be displayed next to the form field
        assert (
            self.wd.find_element(By.ID, f"{row_id}_dynamic_raw_id_label").text
            == custom_obj.chr
        )

        self._save_and_continue()

    def test_dynamic_direct_integerfield(self) -> None:
        """
        dynamic_raw_id on a custom Model with an IntegerField
        """
        row_id = "dynamic_raw_id_fk_int_pk"  # The admin row ID/indicator we test
        num = "12345"

        # Add a test model instances
        custom_obj = IntPrimaryKeyModel.objects.create(num=num)

        self._login_admin()
        self._goto_add_page()
        self._click_lookup_and_choose(row_id, num)

        # object id is inside the input field
        assert self.wd.find_element(By.ID, f"id_{row_id}").get_property("value") == str(
            custom_obj.pk
        )

        # object label is now be displayed next to the form field
        assert self.wd.find_element(
            By.ID, f"{row_id}_dynamic_raw_id_label"
        ).text == str(custom_obj.pk)

        self._save_and_continue()

    def test_dynamic_direct_uuidfield(self) -> None:
        """
        dynamic_raw_id on a custom Model with an UUIDField
        """
        row_id = "dynamic_raw_id_fk_uuid_pk"  # The admin row ID/indicator we test
        uuid = "9a10987b-51ba-472f-9dfe-175286e2258a"
        # Add a test model instances
        custom_obj = UUIDPrimaryKeyModel.objects.create(uuid=uuid)

        self._login_admin()
        self._goto_add_page()
        self._click_lookup_and_choose(row_id, uuid)

        # object id is inside the input field
        assert self.wd.find_element(By.ID, f"id_{row_id}").get_property("value") == str(
            custom_obj.pk
        )

        # object label is now be displayed next to the form field
        assert self.wd.find_element(
            By.ID, f"{row_id}_dynamic_raw_id_label"
        ).text == str(custom_obj.pk)

        self._save_and_continue()

    def test_dynamic_filter(self) -> None:
        """
        Create multiple dynamic_raw_id_fk instances
        and then trigger the change list filter.
        """
        # Some Test instances
        ModelToTest.objects.create(dynamic_raw_id_fk=self.tick)
        ModelToTest.objects.create(dynamic_raw_id_fk=self.trick)
        ModelToTest.objects.create(dynamic_raw_id_fk=self.track)

        self._login_admin()

        # Go to the change list page.
        changelist_url = "{}{}".format(
            self.live_server_url, reverse("admin:testapp_modeltotest_changelist")
        )
        self.wd.get(changelist_url)

        # tick, trick and track are visible in the changelist table
        assert self.wd.find_element(By.LINK_TEXT, "tick").is_displayed()
        assert self.wd.find_element(By.LINK_TEXT, "trick").is_displayed()
        assert self.wd.find_element(By.LINK_TEXT, "track").is_displayed()

        # Click on the filter glass icon and choose 'trick'
        self._click_lookup_and_choose("dynamic_raw_id_fk", "trick")

        # Click the submit icon of the filter panel
        self.wd.find_element(
            By.CSS_SELECTOR, "#changelist-filter input[type=submit]"
        ).click()

        # Only "trick" is visible in the changelist table
        self.wd.implicitly_wait(0)
        assert self.wd.find_element(By.LINK_TEXT, "trick").is_displayed()
        assert len(self.wd.find_elements(By.LINK_TEXT, "tick")) == 0
        assert len(self.wd.find_elements(By.LINK_TEXT, "track")) == 0
