import json

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_201_CREATED, \
    HTTP_200_OK

from termcolor import colored

# Run using:
#    python manage.py test blog

class APITest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staff",
            password="staff")
        self.staff_user.is_staff=True
        self.staff_user.save()

        self.staff_user2 = User.objects.create_user(
            username="staff2",
            password="staff2")
        self.staff_user2.is_staff=True
        self.staff_user2.save()

        self.regular_user = User.objects.create_user(
            username="user",
            password="user")

    def test_post(self):
        self.client.login(username="staff", password="staff")
        print()
        print(colored("""
*   Only users with is_staff=True can create, edit posts and delete comments.
*   Anyone can create comments.
*   Non-anonymous owners of comments can edit them.""", 'cyan'))
        print()
        print(
            colored("LOGIN:", 'yellow'),
            colored("staff", 'green'))
        print()
        print(
            colored("CREATE:", 'yellow'),
            "content=",
            colored("'My First Post'", 'blue'),
            "by",
            colored("staff", 'green'))
        print(
            colored("POST:", 'yellow'),
            colored(reverse('post-list'), 'red'))

        response = self.client.post(reverse('post-list'), {
            'author': self.regular_user.id,
            'content': "My First Post"
        })
        print()
        print("1. ", response.content.decode('utf-8'), response.status_code,
            "CREATED")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        data = json.loads(response.content.decode('utf-8'))

        # Check the author is still staff_user rather than regular_user.
        self.assertEqual(data.get('author', None), self.staff_user.id)

        url = data['url'] # Store the Post's URL

        print()
        print(colored("EDIT:", 'yellow'),
            colored(url, 'red'),
            "content=",
            colored("'My 1st Post, with careful edit.'", 'blue'),
            "by",
            colored("staff", 'green'))
        print(
            colored("PATCH:", 'yellow'),
            colored(url, 'red'))

        response = self.client.patch(url, data=json.dumps({
            'content': 'My 1st Post, with careful edit.'
        }), content_type="application/json")

        print()
        print("2. ", response.content.decode('utf-8'), response.status_code,
            "OK")

        # Test staff can edit own post.
        self.assertEqual(response.status_code, HTTP_200_OK)

        self.client.logout()
        print()
        print(colored("LOGIN:", 'yellow'), colored("another staff", 'green'))
        self.client.login(username="staff2", password="staff2")

        print()
        print(colored("EDIT:", 'yellow'),
            colored(url, 'red'),
            "content=",
            colored("'not so good edit.'", 'blue'),
            "by",
            colored("another staff", 'green'))

        print(
            colored("PATCH:", 'yellow'),
            colored(url, 'red'))
        response = self.client.patch(url, data=json.dumps({
            'content': 'not so good edit'
        }), content_type="application/json")

        print()
        print("3. ", response.content.decode('utf-8'), response.status_code,
            "FORBIDDEN")
        print(colored("    # (Due to permission_classes=[Or(IsReadOnly, "
              "IsStaff), Or(IsReadOnly, IsAuthor)])", 'magenta'))

        # Test staff cannot edit another person's post.
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

        self.client.logout()
        print()
        print(colored("LOGIN:", 'yellow'), colored("non-staff user", 'green'))
        self.client.login(username="user", password="user")

        response = self.client.post(reverse('post-list'), {
            'author': self.regular_user.id,
            'content': "Hahahah"
        })

        print()
        print(
            colored("CREATE:", 'yellow'),
            "content=",
            colored("'Hahahah'", 'blue'),
            "by",
            colored("non-staff user", 'green'))
        print(
            colored("POST:", 'yellow'),
            colored(reverse('post-list'), 'red'))
        print()
        print("4. ", response.content.decode('utf-8'), response.status_code,
            "FORBIDDEN")
        print(colored("    # (Due to permission_classes=[Or(IsReadOnly, "
              "IsStaff), Or(IsReadOnly, IsAuthor)])", 'magenta'))
        # Check regular users *cannot* create posts.
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


    def test_comment(self):
        pass
