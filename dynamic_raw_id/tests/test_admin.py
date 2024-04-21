"""
Test Dynamic Raw ID Widgets with Selenium in a ModelAdmin
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from selenium.webdriver.common.by import By

if TYPE_CHECKING:
    from selenium.webdriver.firefox.webdriver import WebDriver


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
