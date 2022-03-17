from typing import List
from uuid import uuid4

from sqlalchemy import text

from microblog.db_factory import DbFactory
from microblog.models import Message


class UnknownMessageError(RuntimeError):
    pass


class MessageService:
    def __init__(self):
        self.__engine = DbFactory.engine(DbFactory.get_url())

    def create(self, message: Message) -> Message:
        message.id = message.id or str(uuid4())

        assert message.author_id, 'The author ID of the message is required.'
        assert message.content, 'The content of the message is required.'

        with self.__engine.connect() as conn:
            conn.execute(
                # language=sql
                text("""
                    INSERT INTO messages (id, author_id, content, created_at, updated_at) 
                    VALUES (:id, :author_id, :content, NOW(), NOW())
                """),
                [message.dict()]
            )
            conn.commit()

        return self.get(message.id)

    # noinspection PyShadowingBuiltins
    def get(self, id: str) -> Message:
        with self.__engine.connect() as conn:
            # language=sql
            rows = [r for r in conn.execute(text('SELECT * FROM messages WHERE id = :id'), [{'id': id}])]
        if not rows:
            raise UnknownMessageError(id)
        return Message(**rows[0])

    def get_recent(self) -> List[Message]:
        with self.__engine.connect() as conn:
            # language=sql
            rows = [Message(**r) for r in conn.execute(text('SELECT * FROM messages ORDER BY created_at DESC'))]
        return rows

    # noinspection PyShadowingBuiltins
    def patch(self, id: str, message: Message):
        existing_message = self.get(id)
        if not existing_message:
            raise UnknownMessageError(id)

        assert message.author_id or message.content, 'The author ID or the content of the message is required.'

        if message.author_id:
            existing_message.author_id = message.author_id

        if message.content:
            existing_message.content = message.content

        with self.__engine.connect() as conn:
            conn.execute(
                # language=sql
                text("""
                    UPDATE messages
                    SET author_id = :author_id, 
                        content = :content, 
                        created_at = NOW(), 
                        updated_at = NOW()
                    WHERE id = :id
                """),
                [
                    {
                        'id': existing_message.id,
                        'author_id': existing_message.author_id,
                        'content': existing_message.content,
                    }
                ]
            )
            conn.commit()

    # noinspection PyShadowingBuiltins
    def delete(self, id: str):
        with self.__engine.connect() as conn:
            conn.execute(
                # language=sql
                text('DELETE FROM messages WHERE id = :id'),
                [{'id': id}]
            )
            conn.commit()
