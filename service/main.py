import json
import re
import mysql.connector
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from time import sleep
from pathlib import Path

class ContactService:
    def __init__(self, db_config, watch_dir):
        self.db_config = db_config
        self.watch_dir = watch_dir
        self.connection = self.connect_db()

    def connect_db(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            return None

    def close_db(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def insert_contact(self, contact):
        query = "INSERT INTO contacts (name, email, phone) VALUES (%s, %s, %s)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (contact['name'], contact['email'], contact['phone']))
                self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Failed to insert contact: {err}")

    def validate_contact(self, contact):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", contact['email']):
            raise ValueError(f"Invalid email format: {contact['email']}")
        contact['phone'] = self.normalize_phone(contact['phone'])

    def normalize_phone(self, phone):
        phone = re.sub(r'\D', '', phone)
        return f"+1-{phone[:3]}-{phone[3:6]}-{phone[6:]}" if len(phone) >= 10 else phone

    def process_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                contacts = json.load(file)
                for contact in contacts:
                    self.validate_contact(contact)
                    self.insert_contact(contact)
            print(f"Processed file: {file_path}")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error processing file {file_path}: {e}")

    def start_service(self):
        observer = Observer()
        observer.schedule(ContactFileHandler(self), self.watch_dir, recursive=False)
        observer.start()
        print(f"Watching directory: {self.watch_dir}")
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

class ContactFileHandler(FileSystemEventHandler):
    def __init__(self, service):
        self.service = service

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".json"):
            print(f"New file detected: {event.src_path}")
            self.service.process_file(event.src_path)

if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '0170',
        'database': 'jbe'
    }

    watch_dir = Path(__file__).resolve().parent / '../api/storage/app/contacts'

    contact_service = ContactService(db_config, str(watch_dir))
    contact_service.start_service()
