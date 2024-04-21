"""
Test Dynamic Raw ID Filter with Selenium
"""

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from dynamic_raw_id.tests.testapp.models import (
    CharPrimaryKeyModel,
    IntPrimaryKeyModel,
    ModelToTest,
    UUIDPrimaryKeyModel,
)

if TYPE_CHECKING:
    from django.db.models import Model
    from pytest_django.live_server_helper import LiveServer
    from selenium.webdriver.firefox.webdriver import WebDriver

logger = getLogger(__name__)


@pytest.fixture()
def _login(selenium: WebDriver, live_server: LiveServer) -> None:
    """Log into Admin with a Superuser."""
    User.objects.create_superuser("admin", password="admin")  # noqa: S106 Hardcoded password

    selenium.get(f"{live_server}/admin/login/?next=/admin/")
    selenium.find_element(By.CSS_SELECTOR, "input[name=username]").send_keys("admin")
    selenium.find_element(By.CSS_SELECTOR, "input[name=password]").send_keys("admin")
    selenium.find_element(By.CSS_SELECTOR, "input[type=submit]").click()


@pytest.fixture()
def _changelist_page(
    selenium: WebDriver, live_server: LiveServer, _login: None
) -> None:
    """
    Open the "Changelist" admin page of the test model.
    """
    selenium.get(f"{live_server.url}{reverse('admin:testapp_modeltotest_changelist')}")


@pytest.fixture()
def _add_page(selenium: WebDriver, live_server: LiveServer, _login: None) -> None:
    """
    Open the "Add" admin page of the test model.
    """

    selenium.get(f"{live_server.url}{reverse('admin:testapp_modeltotest_add')}")


@pytest.fixture()
def _sample_primary_keys() -> None:
    """Create sample Primary key model instances."""
    User.objects.create(username="user1")
    User.objects.create(username="user2")
    IntPrimaryKeyModel.objects.create(num=123)
    CharPrimaryKeyModel.objects.create(chr="abc")
    UUIDPrimaryKeyModel.objects.create(uuid="9a10987b-51ba-472f-9dfe-175286e2258a")


@pytest.mark.usefixtures("_add_page", "_sample_primary_keys")
def test_widgets(selenium: WebDriver) -> None:
    """
    Test the variations of the Dynamic Raw ID Widget.

    The tests select the "Lookup" icon, choose the first element in the result set,
    and test that the selected element name appears next to the field.

    Doing this in a all-in-one testcase, rather a parameterized test, so it's much
    faster.
    """

    # Input Field ID, Select Value, Test Value
    tests = (
        ("dynamic_raw_id_fk", "user1", "user1"),
        ("dynamic_raw_id_fk_limited", "admin", "admin"),
        ("dynamic_raw_id_many", "user1", "user1"),
        ("dynamic_raw_id_many", "user2", "user1,  user2"),  # Second click on Many2Many
        ("dynamic_raw_id_fk_int_pk", "123", "123"),
        ("dynamic_raw_id_fk_char_pk", "abc", "abc"),
        (
            "dynamic_raw_id_fk_uuid_pk",
            "9a10987b-51ba-472f-9dfe-175286e2258a",
            "9a10987b-51ba-472f-9dfe-175286e2258a",
        ),
    )

    for id_value, select_value, test_value in tests:
        # Select the "Lookup" icon next to the field
        selenium.find_element(By.ID, f"lookup_id_{id_value}").click()

        #  Activate the popup window with the `window.name = <window_id>`
        selenium.switch_to.window(selenium.window_handles[1])

        # Select the result element matching the link text
        selenium.find_element(By.LINK_TEXT, select_value).click()

        # Activate the default window
        selenium.switch_to.window(selenium.window_handles[0])

        # Find the attached label next to it, and draw a red border around it
        label = selenium.find_element(By.ID, f"{id_value}_dynamic_raw_id_label")

        # Test that the displayed value matches the test value
        assert label.text == test_value

        # For debugging, draw green border around the label and wait a bit
        # selenium.execute_script("arguments[0].style.border='3px solid green'", label)
        # time.sleep(1)


@pytest.mark.parametrize(
    ("id_value", "pk_model", "pk_name", "test_values"),
    [
        (
            "dynamic_raw_id_fk",  # Changelist Field ID
            User,  # Primary Key Model to create
            "username",  # Primary Key Model pk fieldname
            ["tick", "trick", "track"],  # Primary Key Test values
        ),
        (
            "dynamic_raw_id_fk_int_pk",
            IntPrimaryKeyModel,
            "num",
            [1, 2, 3],
        ),
        (
            "dynamic_raw_id_fk_char_pk",
            CharPrimaryKeyModel,
            "chr",
            ["abc", "def", "ghi"],
        ),
        (
            "dynamic_raw_id_fk_uuid_pk",
            UUIDPrimaryKeyModel,
            "uuid",
            [
                "95a14df6-8753-41a4-bc7a-94da9f8e82f3",
                "ab34dbb8-d885-48a7-9055-41d02667e4b3",
                "a745c8fc-d39a-4800-89dd-292929379bb3",
            ],
        ),
    ],
)
@pytest.mark.usefixtures("_changelist_page")
def test_changelist_filter(
    selenium: WebDriver,
    id_value: str,
    pk_model: Model,
    pk_name: str,
    test_values: list[str | int],
) -> None:
    """
    Test the Dynamic Raw ID Widget in a Django Admin Changelist Filter.

    This is done for the various types of a primary key (regular, char, uuid, ...).
    """
    # Create testmodel instances
    for value in test_values:
        ModelToTest.objects.create(
            **{id_value: pk_model.objects.create(**{pk_name: value})}
        )

    test_value = test_values[0]

    # Select the "Lookup" icon next to the field
    selenium.find_element(By.ID, f"lookup_id_{id_value}").click()

    #  Activate the popup window with the `window.name = <window_id>`
    selenium.switch_to.window(selenium.window_handles[1])

    # Select the element matching the link text of the first test value
    selenium.find_element(By.LINK_TEXT, str(test_value)).click()

    # Activate the default window
    selenium.switch_to.window(selenium.window_handles[0])

    # Only the first element will be listed on the filtered changelist
    assert selenium.find_element(By.LINK_TEXT, str(test_value)).is_displayed()

    for other_value in test_values[1:]:
        assert len(selenium.find_elements(By.LINK_TEXT, str(other_value))) == 0
