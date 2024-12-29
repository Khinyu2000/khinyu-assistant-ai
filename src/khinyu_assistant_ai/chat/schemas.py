from pydantic import BaseModel

class PostChat(BaseModel):
    user_message: str
    chat_store_key: str | None = None
