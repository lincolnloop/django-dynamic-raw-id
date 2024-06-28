"""
Test vanilla Django raw id fields since we overwrite it's Javascript
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
    Test the classic Django Foreignkey Widget to make sure,
    this application does not break the vanilla behavior.
    """

    # Input Field ID, Select Value, Test Value
    tests = (
        ("rawid_fk", "user1", "user1"),
        ("rawid_fk_limited", "admin", "admin"),
        ("rawid_many", "user1", None),
        ("rawid_many", "user2", None),  # Second click on Many2Many
    )

    for id_value, select_value, _ in tests:
        # Select the "Lookup" icon next to the field
        selenium.find_element(By.ID, f"lookup_id_{id_value}").click()

        #  Activate the popup window with the `window.name = <window_id>`
        selenium.switch_to.window(selenium.window_handles[1])

        # Select the result element matching the link text
        selenium.find_element(By.LINK_TEXT, select_value).click()

        # Activate the default window
        selenium.switch_to.window(selenium.window_handles[0])

    # Click the save button and wait for page reload
    selenium.find_element(By.NAME, "_continue").click()
    selenium.implicitly_wait(0.5)  # Wait a bit for page reload

    # Test that all selected ForeignKeys are now displayed after reload.
    for id_value, _, test_value in tests:
        # ManyToMany fields don't display a label in Vanilla Django raw id fields.
        if test_value is None:
            continue

        label = selenium.find_element(By.CSS_SELECTOR, f"#id_{id_value} ~ strong")
        assert label.text == test_value
