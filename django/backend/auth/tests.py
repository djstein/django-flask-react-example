import json
from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class UserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test@test.com",
            email="test@test.com",
            password="this-is-a-bad-password",
        )

    def test_user_created(self):
        self.assertEqual(get_user_model().objects.count(), 1)
        user = get_user_model().objects.get()
        self.assertEqual(user.username, "test@test.com")


class UserViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(
            username="test@test.com",
            email="test@test.com",
            password="this-is-a-bad-password",
        )
        self.user_two = get_user_model().objects.create(
            username="test2@test.com",
            email="test2@test.com",
            password="this-is-a-bad-password",
        )

    def test_fetch_list(self):
        response = self.client.get("/users/")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(response.json().get("results")), 2)

    def test_fetch_resource(self):
        response = self.client.get("/users/1/")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(response.json().get("results")), 1)
        self.assertEqual(
            response.json().get("results")[0].get("fields").get("username"),
            "test@test.com",
        )

    def test_update_resource(self):
        response = self.client.patch(
            "/users/1/", json.dumps({"email": "helloworld@test.com"})
        )
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(response.json().get("results")), 1)
        self.assertEqual(
            response.json().get("results")[0].get("fields").get("email"),
            "helloworld@test.com",
        )

    def test_delete_resource(self):
        self.assertTrue(get_user_model().objects.get(pk=2))
        response = self.client.delete("/users/2/")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(response.json().get("results")), 0)
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(pk=2)
