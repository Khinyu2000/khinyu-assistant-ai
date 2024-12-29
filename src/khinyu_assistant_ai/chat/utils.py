from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from logging import getLogger, DEBUG
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.base.llms.types import MessageRole
from llama_index.core.chat_engine.types import ChatMode
import os

logger = getLogger(__name__)
logger.setLevel(DEBUG)

chat_store = SimpleChatStore()

async def stream_chat(llm: FunctionCallingLLM, embed_model: BaseEmbedding, user_message: str, key: str | None):
    try:
        if key is None:
            chat_store_key = "user"
            chat_store.add_message(key=chat_store_key, message=ChatMessage(role=MessageRole.USER, content=user_message))
            chat_memory = ChatMemoryBuffer.from_defaults(
                token_limit=3000,
                chat_store=chat_store,
                chat_store_key=chat_store_key,
            )
        else:
            chat_store_key = key
            chat_store.add_message(key=chat_store_key, message=ChatMessage(role=MessageRole.USER, content=user_message))
            chat_memory = ChatMemoryBuffer(
                token_limit=3000,
                chat_store=chat_store,
                chat_store_key=chat_store_key
            )
        # response: list[ChatMessage] = chat_memory.get(chat_store_key="user")
        # logger.info(response)
        # for message in response:
        #     logger.info(message.content)
        #     logger.info(message.role)
        # return "success"
        logger.info(chat_memory.to_string())
        DATA_DIR = "./data"
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        index = VectorStoreIndex.from_documents(documents=documents, embed_model=embed_model)
        chat_engine = index.as_chat_engine(llm=llm, chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT, memory=chat_memory)
        response = chat_engine.chat(user_message)
        chat_store.add_message(key=chat_store_key, message=ChatMessage(role=MessageRole.ASSISTANT, content=response.response))
        logger.info(response.response)
        logger.info(type(response.response))
        return response.response
    except Exception as e:
        logger.info(e)
    

