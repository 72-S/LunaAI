from datetime import datetime
import sqlite3

import numpy as np


class EmbeddingDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.initialize_db()

    def initialize_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS embeddings
                               (id INTEGER PRIMARY KEY, prompt TEXT, embedding TEXT, timestamp TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history
                                   (id INTEGER PRIMARY KEY AUTOINCREMENT, prompt TEXT, response TEXT, timestamp TEXT)''')
        self.conn.commit()

    def trim_chat_history(self, limit=30):
        self.cursor.execute("SELECT COUNT(*) FROM chat_history")
        count = self.cursor.fetchone()[0]
        if count > limit:
            delete_count = count - limit
            self.cursor.execute(
                "DELETE FROM chat_history WHERE id IN (SELECT id FROM chat_history ORDER BY id ASC LIMIT ?)",
                (delete_count,))
            self.conn.commit()

    def add_chat_message(self, prompt, response):
        self.cursor.execute("SELECT prompt FROM chat_history ORDER BY id DESC LIMIT 1")
        last_message = self.cursor.fetchone()
        if last_message is None or last_message[0] != prompt:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO chat_history (prompt, timestamp, response) VALUES (?, ?, ?)",
                                (prompt, timestamp, response))
            self.conn.commit()
            self.trim_chat_history()
        else:
            print("Identische Nachricht bereits vorhanden, wird nicht erneut hinzugefügt.")

    def add_or_retrieve_prompt(self, prompt, embedding):
        self.cursor.execute("SELECT id, embedding FROM embeddings")
        for row in self.cursor.fetchall():
            db_id, db_embedding = row
            db_embedding = np.fromstring(db_embedding, sep=',')
            similarity = np.dot(embedding, db_embedding) / (np.linalg.norm(embedding) * np.linalg.norm(db_embedding))
            if similarity > 0.95:
                self.cursor.execute("SELECT prompt FROM embeddings WHERE id = ?", (db_id,))
                return self.cursor.fetchone()[0], True
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        embedding_text = ','.join(map(str, embedding))
        self.cursor.execute("INSERT INTO embeddings (prompt, embedding, timestamp) VALUES (?, ?, ?)",
                            (prompt, embedding_text, timestamp))
        self.conn.commit()
        return prompt, False

    def retrieve_recent_chat_messages(self, limit=10):
        self.cursor.execute("SELECT prompt, response FROM chat_history ORDER BY id DESC LIMIT ?", (limit,))
        messages = [{'prompt': row[0], 'response': row[1]} for row in self.cursor.fetchall()]
        return messages[::-1]

    def retrieve_similar_prompts(self, embedding, threshold=0.8):
        similar_prompts = []
        self.cursor.execute("SELECT id, embedding, prompt FROM embeddings")
        for row in self.cursor.fetchall():
            db_id, db_embedding, db_prompt = row
            db_embedding = np.fromstring(db_embedding, sep=',')
            similarity = np.dot(embedding, db_embedding) / (np.linalg.norm(embedding) * np.linalg.norm(db_embedding))
            if similarity > threshold:
                similar_prompts.append(db_prompt)
        return similar_prompts

    def search_chat_history(self, query_embedding, threshold=0.75):
        self.cursor.execute("SELECT prompt, response, embedding FROM chat_history")
        results = []
        for row in self.cursor.fetchall():
            prompt, response, db_embedding_str = row
            db_embedding = np.fromstring(db_embedding_str, sep=',')
            similarity = np.dot(query_embedding, db_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(db_embedding))
            if similarity > threshold:
                results.append({'prompt': prompt, 'response': response})
        return results

    def close(self):
        self.conn.close()
