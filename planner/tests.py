from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task


class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ali', password='Pass12345!')
        self.other = User.objects.create_user(username='omar', password='Pass12345!')
        self.client.login(username='ali', password='Pass12345!')

    def test_create_task(self):
        self.client.post(reverse('task_create'), {
            'title': 'Study Django', 'description': 'Ch5',
            'priority': 'HIGH', 'status': 'PENDING',
        })
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().user, self.user)

    def test_update_task(self):
        task = Task.objects.create(user=self.user, title='Old')
        self.client.post(reverse('task_update', args=[task.pk]), {
            'title': 'New', 'priority': 'MEDIUM', 'status': 'PENDING',
        })
        task.refresh_from_db()
        self.assertEqual(task.title, 'New')

    def test_delete_task(self):
        task = Task.objects.create(user=self.user, title='Temp')
        self.client.post(reverse('task_delete', args=[task.pk]))
        self.assertEqual(Task.objects.count(), 0)

    def test_cannot_access_others_task(self):
        task = Task.objects.create(user=self.other, title='Secret')
        response = self.client.get(reverse('task_update', args=[task.pk]))
        self.assertEqual(response.status_code, 404)   