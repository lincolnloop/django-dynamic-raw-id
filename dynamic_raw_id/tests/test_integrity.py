"""
Test the basic integrity of the app. We can't test the Javascript side
and all those fancy popups, but we can load an admin view and check that
dynamic_raw_id was successfully loaded and displays items properly.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from pytest_django.asserts import assertContains

from dynamic_raw_id.tests.testapp.models import (
    CharPrimaryKeyModel,
    IntPrimaryKeyModel,
    ModelToTest,
    UUIDPrimaryKeyModel,
)

if TYPE_CHECKING:
    from django.test import Client


@pytest.fixture()
def staff_user(db: Any) -> User:
    """Staff user with no additional permissions."""
    user = User.objects.create_user("staff", "", "staff")
    user.is_staff = True
    user.save()
    return user


@pytest.fixture()
def sample_obj(db: Any) -> dict[str, Any]:
    """
    Create a bit of sample data we can use to assign.
    """
    user1 = User.objects.create_superuser("jon", "jon@example.com", "")
    user2 = User.objects.create_superuser("jim", "jim@example.com", "")
    char = CharPrimaryKeyModel.objects.create(chr="helloworld")
    num = IntPrimaryKeyModel.objects.create(num=12345)
    uuid = UUIDPrimaryKeyModel.objects.create(
        uuid="9a10987b-51ba-472f-9dfe-175286e2258a"
    )

    obj = ModelToTest.objects.create(
        rawid_fk=user1,
        rawid_fk_limited=user1,
        dynamic_raw_id_fk=user1,
        dynamic_raw_id_fk_limited=user1,
        dynamic_raw_id_fk_int_pk=num,
        dynamic_raw_id_fk_char_pk=char,
        dynamic_raw_id_fk_uuid_pk=uuid,
    )
    obj.rawid_many.add(user1, user2)
    obj.dynamic_raw_id_many.add(user1, user2)

    return obj


def get_labelview_url(multi: bool = False) -> str:
    """
    Create a URL to the JSON view that creates the dynamic labels.
    """ ""
    name = multi and "dynamic_raw_id_multi_label" or "dynamic_raw_id_label"
    return reverse(
        f"dynamic_raw_id:{name}",
        kwargs={"app_name": "testapp", "model_name": "modeltotest"},
    )


def test_changelist_integrity(admin_client: Client, sample_obj: Any) -> None:
    """
    The `DynamicRawIDFilter` is hooked up in the right filter bar of the
    testapp changelist view.
    """
    list_url = reverse("admin:testapp_modeltotest_changelist")
    response = admin_client.get(list_url, follow=True)
    assert response.status_code == 200
    assertContains(response, "dynamic_raw_id-related-lookup")


def test_change_integrity(admin_client: Client, sample_obj: Any) -> None:
    """
    The `DynamicRawIDFilter` buttons are displayed next to the FK Widget.
    """
    list_url = reverse("admin:testapp_modeltotest_change", args=(sample_obj.pk,))
    response = admin_client.get(list_url, follow=True)
    assert response.status_code == 200
    assertContains(response, "dynamic_raw_id-clear-field")
    assertContains(response, "dynamic_raw_id-related-lookup")


def test_labelview_unauthed(client: Client, sample_obj: Any) -> None:
    """
    Label view required authentication and a staff account
    """
    response = client.get(get_labelview_url(), follow=True)
    assert response.status_code == 404


def test_labelview_no_permission(
    client: Client, staff_user: User, sample_obj: Any
) -> None:
    """
    Valid Label view request is denied if user has no change permisson for the app.
    """
    client.login(username="staff", password="staff")  # noqa: S106 Hardcoded password
    response = client.get(
        get_labelview_url(multi=True), {"id": sample_obj.pk}, follow=True
    )
    assert response.status_code == 403


def test_labelview(admin_client: Client, sample_obj: Any) -> None:
    """
    Call the labelview directly (what usually an Ajax JS call would do)
    and check for proper response.
    """
    response = admin_client.get(get_labelview_url(), {"id": sample_obj.pk}, follow=True)
    assert response.status_code == 200


def test_multi_labelview(admin_client: Client, sample_obj: Any) -> None:
    """
    Call the labelview directly (what usually an Ajax JS call would do)
    and check for proper response. Exect a multi response.
    """
    response = admin_client.get(
        get_labelview_url(multi=True), {"id": sample_obj.pk}, follow=True
    )
    assert response.status_code == 200


def test_invalid_id(admin_client: Client) -> None:
    """
    Test label view with where model primary key is invalid.
    """
    response = admin_client.get(get_labelview_url(), {"id": "wrong"}, follow=True)
    assert response.status_code == 400


def test_id_does_not_exist(admin_client: Client) -> None:
    """
    Test label view with where a model primary key does not exist.
    """
    response = admin_client.get(get_labelview_url(), {"id": "123456"}, follow=True)
    assert response.status_code == 400


def test_no_id(admin_client: Client) -> None:
    """
    Test label view with no ID given.
    """
    response = admin_client.get(get_labelview_url(), follow=True)
    assert response.status_code == 400


def test_invalid_appname(admin_client: Client) -> None:
    """
    Test label view with invalid app/model name.
    """
    url = get_labelview_url().replace("testapp", "foobar")
    response = admin_client.get(url, {"id": "123456"}, follow=True)
    assert response.status_code == 400
