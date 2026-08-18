from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import AIConversation, AIMessage


class AIAssistantTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='hana', password='Pass12345!')
        self.other = User.objects.create_user(username='sara', password='Pass12345!')
        self.client.login(username='hana', password='Pass12345!')

    def test_chat_page_loads(self):
        response = self.client.get(reverse('ai_chat'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_cannot_access(self):
        self.client.logout()
        response = self.client.get(reverse('ai_chat'))
        self.assertNotEqual(response.status_code, 200)  

    @patch('ai_assistant.views.get_ai_response')
    def test_new_conversation_created_and_messages_stored(self, mock_ai):
        mock_ai.return_value = "Django is a Python web framework."
        self.client.post(reverse('ai_chat'), {'prompt': 'What is Django?'})

        self.assertEqual(AIConversation.objects.filter(user=self.user).count(), 1)
        conv = AIConversation.objects.first()
        self.assertEqual(conv.messages.filter(role='USER').count(), 1)
        self.assertEqual(conv.messages.filter(role='ASSISTANT').count(), 1)

    @patch('ai_assistant.views.get_ai_response')
    def test_history_passed_and_prompt_once(self, mock_ai):
        mock_ai.return_value = "answer"
        self.client.post(reverse('ai_chat'), {'prompt': 'Explain SQL joins.'})
        conv = AIConversation.objects.first()

        self.client.post(reverse('ai_conversation', args=[conv.pk]),
                         {'prompt': 'Give me an example.'})

        args, kwargs = mock_ai.call_args
        current_prompt = args[0]
        history = kwargs.get('history_messages') or []

        self.assertEqual(current_prompt, 'Give me an example.')
        self.assertEqual(len(history), 2)
        history_texts = [m.content for m in history]
        self.assertNotIn('Give me an example.', history_texts)

    @patch('ai_assistant.views.get_ai_response')
    def test_history_chronological_order(self, mock_ai):
        mock_ai.return_value = "answer"
        self.client.post(reverse('ai_chat'), {'prompt': 'first'})
        conv = AIConversation.objects.first()
        self.client.post(reverse('ai_conversation', args=[conv.pk]), {'prompt': 'second'})

        _, kwargs = mock_ai.call_args
        history = kwargs.get('history_messages') or []
        self.assertEqual(history[0].content, 'first')

    @patch('ai_assistant.views.get_ai_response')
    def test_ai_failure_handled_gracefully(self, mock_ai):
        mock_ai.side_effect = Exception("API down")
        response = self.client.post(reverse('ai_chat'), {'prompt': 'hi'}, follow=True)
        self.assertEqual(response.status_code, 200)
        conv = AIConversation.objects.first()
        ai_msg = conv.messages.filter(role='ASSISTANT').first()
        self.assertIn("unavailable", ai_msg.content)

    @patch('ai_assistant.views.get_ai_response')
    def test_cannot_access_others_conversation(self, mock_ai):
        conv = AIConversation.objects.create(user=self.other, title="secret")
        response = self.client.get(reverse('ai_conversation', args=[conv.pk]))
        self.assertEqual(response.status_code, 404)

    @patch('ai_assistant.views.get_ai_response')
    def test_conversation_delete(self, mock_ai):
        conv = AIConversation.objects.create(user=self.user, title="temp")
        self.client.post(reverse('conversation_delete', args=[conv.pk]))
        self.assertEqual(AIConversation.objects.filter(pk=conv.pk).count(), 0)

    def test_api_key_not_hardcoded(self):
        import ai_assistant.services as svc
        import inspect
        source = inspect.getsource(svc)
        self.assertNotIn('AIza', source)  