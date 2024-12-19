import sqlite3
import json
import config
import os
from src.rag_chatbot import chat_with_rag

# Establish a connection to the database
conn = sqlite3.connect(os.path.join(config.SOURCE, config.Source.MESSAGE_HISTORY_SQLITE3.value))

# Create a cursor object using the connection
cursor = conn.cursor()

# Create a new table called 'message_history'
cursor.execute('''
CREATE TABLE IF NOT EXISTS message_history (
    id INTEGER PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    msg_history TEXT NOT NULL,  -- Storing JSON as a string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit the changes
conn.commit()

# Function to insert or update a message history
def insert_message_history(conversation_id, new_messages):
    # Check if a record exists with the conversation_id
    cursor.execute('''
        SELECT msg_history FROM message_history
        WHERE conversation_id = ?
    ''', (conversation_id,))
    result = cursor.fetchone()
    if result:
        # Record exists, append new messages to the existing msg_history
        existing_messages = json.loads(result[0])
        updated_messages = existing_messages + new_messages
        msg_history_json = json.dumps(updated_messages)

        # Update the record with the new message history
        cursor.execute('''
            UPDATE message_history
            SET msg_history = ?
            WHERE conversation_id = ?
        ''', (msg_history_json, conversation_id))
        print(f'Message history updated for conversation {conversation_id}.')
    else:
        # Record does not exist, insert a new one with the new messages
        msg_history_json = json.dumps(new_messages)
        cursor.execute('''
            INSERT INTO message_history (conversation_id, msg_history)
            VALUES (?, ?)
        ''', (conversation_id, msg_history_json))
        print('Inserted message history with id:', cursor.lastrowid)
    
    conn.commit()

# Function to retrieve message history by conversation_id
def get_message_history(conversation_id):
    cursor.execute('''
        SELECT msg_history FROM message_history
        WHERE conversation_id = ?
    ''', (conversation_id,))

    # Fetch the result
    result = cursor.fetchone()

    if result:
        # Deserialize the JSON string back into a Python list
        msg_history = json.loads(result[0])
        return msg_history
    else:
        print('No records found for the given conversation ID.')
        return []

def delete_message_history(conversation_id):
    cursor.execute('''
        DELETE FROM message_history
        WHERE conversation_id = ?
    ''', (conversation_id,))
    # Commit the changes
    conn.commit()
    print(f'Messages deleted for conversation {conversation_id}.')

def end_db():
    conn.close()
    print(f'db connections closed')

def process(msg_history):
    """Transforms a list of Message objects into a single text string.

    Args:
      messages: A list of Message objects.

    Returns:
      A string representation of the messages.
    """
    text = ""
    for message in msg_history:
        text += f"{list(message.keys())[0]}: {list(message.values())[0]}\n"
    return text

def send_email(visitor_name, visitor_country, visitor_city, thread_id, ai_response):
    conversation_link = f'https://conversations-app.brevo.com/conversations/{thread_id}'
    pass

def get_response(data):
    eventName = data.get('eventName', '')
    visitor = data.get('visitor', {})
    # Extract thread id and conversation link
    thread_id = visitor.get('threadId', '')

    if eventName == "conversationTranscript":
        delete_message_history(thread_id)
        return None
    
    # Extract visitor details
    visitor_name = visitor.get('displayedName', '')
    visitor_country = visitor.get('country', '')
    visitor_city = visitor.get('city', '')

    # Extract messages history
    messages = data.get('messages', [])  # This works for 'conversationTranscript' and 'conversationFragment'
    if 'message' in data:
        messages = [data['message']]  # For the 'conversationStarted' format which contains a single message
    for message in messages:
        # Each message is a dictionary; here we print out just the text, but you can format this however you need
        sender = 'assistant' if message.get('type', '') == 'agent' else 'user'
        text = message.get('text', '')
        if sender == "user":
            msg_history = get_message_history(thread_id)
            chat_history = process(msg_history)
            ai_response = chat_with_rag(question=text, conversation=chat_history)
            # print(ai_response)
            insert_message_history(thread_id, [{sender: text}])
            send_email(visitor_name, visitor_country, visitor_city, thread_id, ai_response)