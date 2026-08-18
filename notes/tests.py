from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note


class NoteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='noor', password='Pass12345!')
        self.client.login(username='noor', password='Pass12345!')

    def test_create_note(self):
        self.client.post(reverse('note_create'), {'title': 'My Note', 'content': 'Hello'})
        self.assertEqual(Note.objects.filter(user=self.user).count(), 1)