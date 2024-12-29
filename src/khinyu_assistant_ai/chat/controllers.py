from litestar import Controller, post
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex
from .schemas import PostChat
from .utils import stream_chat
from logging import getLogger, DEBUG
import os

logger = getLogger(__name__)
logger.setLevel(DEBUG)

LLM_MODEL = os.environ.get("LLM_MODEL", None)
LLM_HOST = os.environ.get("LLM_HOST", None)
EMBED_MODEL = os.environ.get("EMBED_MODEL", None)

llm = Ollama(model=LLM_MODEL, base_url=LLM_HOST)
embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)


class ChatController(Controller):
    path = "/api/chat"

    @post("/")
    async def chat(self, data: PostChat) -> str:
        try:
            return stream_chat(llm, embed_model, data.user_message, data.chat_store_key)
        except Exception as e:
            logger.info(e)


        



