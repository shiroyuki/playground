from time import time
from unittest import TestCase

from sqlalchemy import text

from microblog.db_factory import DbFactory
from microblog.message_service import MessageService
from microblog.models import Message


def random_test_id() -> str:
    return f'test-{time()}'


class TestMessageService(TestCase):
    _engine = DbFactory.engine(DbFactory.get_url())

    def tearDown(self):
        with self._engine.connect() as conn:
            conn.execute(text('DELETE FROM messages WHERE id LIKE "test-%"'))
            conn.commit()

    def test_happy_path(self):
        test_id = random_test_id()
        test_message = Message(id=test_id, author_id='test', content='panda')

        message_service = MessageService()

        created_message = message_service.create(test_message)
        self.assertEqual(test_message.id, created_message.id)
        self.assertEqual(test_message.author_id, created_message.author_id)
        self.assertEqual(test_message.content, created_message.content)
        self.assertIsNone(test_message.created_at)
        self.assertIsNone(test_message.updated_at)
        self.assertIsNotNone(created_message.created_at)
        self.assertIsNotNone(created_message.updated_at)

        expected_additional_size = 5
        for __ in range(expected_additional_size):
            message_service.create(Message(id=random_test_id(), author_id='text', content='panda'))

        listed_messages = message_service.get_recent()
        self.assertGreaterEqual(len(listed_messages), expected_additional_size + 1, f'Must have at least {expected_additional_size + 1} (randomly created + intentionally created)')

        intentionally_created_messages = [m for m in listed_messages if m.id == test_id]
        self.assertGreaterEqual(len(intentionally_created_messages), 1, f'Must have the intentionally created message')

        intentionally_created_message = intentionally_created_messages[0]
        self.assertEqual(intentionally_created_message.id, created_message.id)
        self.assertEqual(intentionally_created_message.author_id, created_message.author_id)
        self.assertEqual(intentionally_created_message.content, created_message.content)
        self.assertEqual(intentionally_created_message.created_at, created_message.created_at)
        self.assertEqual(intentionally_created_message.updated_at, created_message.updated_at)

        get_message = message_service.get(test_id)
        self.assertEqual(get_message.id, created_message.id)
        self.assertEqual(get_message.author_id, created_message.author_id)
        self.assertEqual(get_message.content, created_message.content)
        self.assertEqual(get_message.created_at, created_message.created_at)
        self.assertEqual(get_message.updated_at, created_message.updated_at)

        message_service.delete(test_id)
        self.assertEqual(len([m for m in message_service.get_recent() if m.id == test_id]), 0)
