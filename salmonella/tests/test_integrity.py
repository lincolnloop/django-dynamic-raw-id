from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from django.contrib.auth.models import User

from salmonella.tests.testapp.models import (CharPrimaryKeyModel,
                                             DirectPrimaryKeyModel,
                                             SalmonellaTest)

class SalmonellaTestCase(TestCase):
    """
    Test the basic integrity of the app. We can't test the Javascript side
    and all those fancy popups, but we can load an admin view and check that
    Salmonella was successfully loaded and displays items properly.
    """
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', '', 'admin')
        self.client.login(username='admin', password='admin')

    def tearDown(self):
        self.client.logout()

    def get_labelview_url(self, multi=False):
        name = multi and 'salmonella_multi_label' or 'salmonella_label'
        return reverse(name, kwargs={
            'app_name': 'testapp', 'model_name': 'salmonellatest'
        })

    def create_sample_data(self):
        """
        Create a bit of sample data we can use to assign.
        """
        self.u1 = User.objects.create_superuser('jon', 'jon@example.com', '')
        self.u2 = User.objects.create_superuser('jim', 'jim@example.com', '')
        self.c1 = CharPrimaryKeyModel.objects.create(chr='helloworld')
        self.n1 = DirectPrimaryKeyModel.objects.create(num=12345)

        self.obj = SalmonellaTest.objects.create(
            rawid_fk=self.u1,
            rawid_fk_limited=self.u1,
            rawid_fk_direct_pk=self.n1,
            salmonella_fk=self.u1,
            salmonella_fk_limited=self.u1,
            salmonella_fk_direct_pk=self.n1,
            salmonella_fk_char_pk=self.c1,
        )
        self.obj.rawid_many.add(self.u1, self.u2)
        self.obj.salmonella_many.add(self.u1, self.u2)

    def test_changelist_integrity(self):
        """
        The `SalmonellaFilter` is hooked up in the right filter bar of the
        testapp changelist view.
        """
        self.create_sample_data()
        list_url = reverse('admin:testapp_salmonellatest_changelist')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)

    def test_change_integrity(self):
        """
        The `SalmonellaFilter` is hooked up in the right filter bar of the
        testapp changelist view.
        """
        self.create_sample_data()
        list_url = reverse('admin:testapp_salmonellatest_change', args=(self.obj.pk,))
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)

    def test_labelview_unauthed(self):
        """
        Label view required authentication and a staff account
        """
        self.client.logout()
        response = self.client.get(self.get_labelview_url(), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_labelview(self):
        """
        Call the labelview directly (what usually an Ajax JS call would do)
        and check for proper response.
        """
        self.create_sample_data()
        response = self.client.get(self.get_labelview_url(), {'id': self.obj.pk},
                                   follow=True)
        self.assertEqual(response.status_code, 200)

    def test_multi_labelview(self):
        """
        Call the labelview directly (what usually an Ajax JS call would do)
        and check for proper response.
        """
        self.create_sample_data()
        response = self.client.get(self.get_labelview_url(multi=True),
                                   {'id': self.obj.pk}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_id(self):
        """
        Test invalid id.
        """
        self.create_sample_data()
        response = self.client.get(self.get_labelview_url(), {'id': 'wrong'},
                                   follow=True)
        self.assertEqual(response.status_code, 400)

    def test_no_id(self):
        """
        Test invalid app/model name.
        """
        self.create_sample_data()
        response = self.client.get(self.get_labelview_url(), follow=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_appname(self):
        """
        Test invalid app/model name.
        """
        self.create_sample_data()
        url = self.get_labelview_url().replace('testapp', 'foobar')
        response = self.client.get(url, {'id': self.obj.pk}, follow=True)
        self.assertEqual(response.status_code, 400)
