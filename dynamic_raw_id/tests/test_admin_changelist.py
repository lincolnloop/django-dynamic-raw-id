"""
Test Dynamic Raw ID Widgets with Selenium in a Admin Changelist Filterset
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By

from dynamic_raw_id.tests.testapp.models import (
    CharPrimaryKeyModel,
    IntPrimaryKeyModel,
    ModelToTest,
    UUIDPrimaryKeyModel,
)

if TYPE_CHECKING:
    from django.db.models import Model
    from selenium.webdriver.firefox.webdriver import WebDriver


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
