from enum import Enum
from logging import getLogger
from logging.config import fileConfig
from os.path import join
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ROOT = "./"
LOG_INI = join(PROJECT_ROOT, 'log.ini')
SOURCE = join(PROJECT_ROOT, 'source')
Prompt_Template = join(PROJECT_ROOT, 'prompt_templates')

# pinecone
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def load_env():
    load_dotenv(join(PROJECT_ROOT, ".env"))

class PromptTemplate(Enum):
    SAVED_REPLY = "saved_reply.txt"
    MAIN_PROMPT = "main_prompt.txt"

class Source(Enum):
    CSV_DATA = "info.csv"
    MESSAGE_HISTORY_SQLITE3 = "msg_history.db"

class ModelType(str, Enum):
    gpt4o = 'gpt-4o'
    gpt4o_mini = 'gpt-4o-mini'
    embedding = "text-embedding-3-large"

def get_prompt_template(prompt_template: PromptTemplate):
    with open(join(Prompt_Template, prompt_template.value), "rt") as f:
        return f.read()

def configure_logging(get_logger=False):
    global logging_configured
    if not logging_configured:
        fileConfig(LOG_INI)
        logging_configured = True
    if get_logger:
        logger = getLogger('freedo')
        return logger