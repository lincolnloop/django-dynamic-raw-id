from django.contrib.auth.models import User
from django.test.testcases import TestCase
from django.urls import reverse

from dynamic_raw_id.tests.testapp.models import (
    CharPrimaryKeyModel,
    IntPrimaryKeyModel,
    ModelToTest,
    UUIDPrimaryKeyModel,
)


class DynamicRawIDTestCase(TestCase):
    """
    Test the basic integrity of the app. We can't test the Javascript side
    and all those fancy popups, but we can load an admin view and check that
    dynamic_raw_id was successfully loaded and displays items properly.
    """

    def setUp(self) -> None:
        # Create admin and login by default
        self.admin = User.objects.create_superuser("admin", "", "admin")
        self.client.login(username="admin", password="admin")  # noqa: S106 Hardcoded password

        # Create additional staff user without any app permissions
        self.user_noperm = User.objects.create_user("user", "", "user")
        self.user_noperm.is_staff = True
        self.user_noperm.save()

    def tearDown(self) -> None:
        self.client.logout()

    def get_labelview_url(self, multi: bool = False) -> str:
        name = multi and "dynamic_raw_id_multi_label" or "dynamic_raw_id_label"
        return reverse(
            f"dynamic_raw_id:{name}",
            kwargs={"app_name": "testapp", "model_name": "modeltotest"},
        )

    def create_sample_data(self) -> None:
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

        self.obj = ModelToTest.objects.create(
            rawid_fk=user1,
            rawid_fk_limited=user1,
            dynamic_raw_id_fk=user1,
            dynamic_raw_id_fk_limited=user1,
            dynamic_raw_id_fk_int_pk=num,
            dynamic_raw_id_fk_char_pk=char,
            dynamic_raw_id_fk_uuid_pk=uuid,
        )
        self.obj.rawid_many.add(user1, user2)
        self.obj.dynamic_raw_id_many.add(user1, user2)

    def test_changelist_integrity(self) -> None:
        """
        The `DynamicRawIDFilter` is hooked up in the right filter bar of the
        testapp changelist view.
        """
        self.create_sample_data()
        list_url = reverse("admin:testapp_modeltotest_changelist")
        response = self.client.get(list_url)
        assert response.status_code == 200

    def test_change_integrity(self) -> None:
        """
        The `DynamicRawIDFilter` is hooked up in the right filter bar of the
        testapp changelist view.
        """
        self.create_sample_data()
        list_url = reverse("admin:testapp_modeltotest_change", args=(self.obj.pk,))
        response = self.client.get(list_url)
        assert response.status_code == 200

    def test_labelview_unauthed(self) -> None:
        """
        Label view required authentication and a staff account
        """
        self.client.logout()
        response = self.client.get(self.get_labelview_url(), follow=True)
        assert response.status_code == 404

    def test_labelview_no_permission(self) -> None:
        """
        Valid Label view request is denied if user has
        no change permisson for the app.
        """
        self.client.logout()
        self.client.login(username="user", password="user")  # noqa: S106 Hardcoded password
        self.create_sample_data()
        response = self.client.get(
            self.get_labelview_url(multi=True), {"id": self.obj.pk}, follow=True
        )
        assert response.status_code == 403

    def test_labelview(self) -> None:
        """
        Call the labelview directly (what usually an Ajax JS call would do)
        and check for proper response.
        """
        self.create_sample_data()
        response = self.client.get(
            self.get_labelview_url(), {"id": self.obj.pk}, follow=True
        )
        assert response.status_code == 200

    def test_multi_labelview(self) -> None:
        """
        Call the labelview directly (what usually an Ajax JS call would do)
        and check for proper response.
        """
        self.create_sample_data()
        response = self.client.get(
            self.get_labelview_url(multi=True), {"id": self.obj.pk}, follow=True
        )
        assert response.status_code == 200

    def test_invalid_id(self) -> None:
        """
        Test invalid id.
        """
        self.create_sample_data()
        response = self.client.get(
            self.get_labelview_url(), {"id": "wrong"}, follow=True
        )
        assert response.status_code == 400

    def test_id_does_not_exist(self) -> None:
        """
        Test model primary key does not exist.
        """
        self.create_sample_data()
        response = self.client.get(
            self.get_labelview_url(), {"id": "123456"}, follow=True
        )
        assert response.status_code == 400

    def test_no_id(self) -> None:
        """
        Test invalid app/model name.
        """
        self.create_sample_data()
        response = self.client.get(self.get_labelview_url(), follow=True)
        assert response.status_code == 400

    def test_invalid_appname(self) -> None:
        """
        Test invalid app/model name.
        """
        self.create_sample_data()
        url = self.get_labelview_url().replace("testapp", "foobar")
        response = self.client.get(url, {"id": self.obj.pk}, follow=True)
        assert response.status_code == 400
