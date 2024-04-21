"""
Test Dynamic Raw ID Filter with Selenium on a Django Model
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from dynamic_raw_id.tests.testapp.models import (
    CharPrimaryKeyModel,
    IntPrimaryKeyModel,
    UUIDPrimaryKeyModel,
)

if TYPE_CHECKING:
    from pytest_django.live_server_helper import LiveServer
    from selenium.webdriver.firefox.webdriver import WebDriver


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
def _add_page_with_inlines(
    selenium: WebDriver, live_server: LiveServer, _login: None
) -> None:
    """
    Open the "Add" admin page of the test model.
    """

    selenium.get(
        f"{live_server.url}{reverse('admin:testapp_modeltotestinlinesbase_add')}"
    )


@pytest.fixture()
def _sample_primary_keys() -> None:
    """Create sample Primary key model instances."""
    User.objects.create(username="user1")
    User.objects.create(username="user2")
    IntPrimaryKeyModel.objects.create(num=123)
    CharPrimaryKeyModel.objects.create(chr="abc")
    UUIDPrimaryKeyModel.objects.create(uuid="9a10987b-51ba-472f-9dfe-175286e2258a")
