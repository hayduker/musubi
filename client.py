from imapclient import IMAPClient
import os


class IMAPCreds:
    def __init__(self):
        self.host = self._get_imap_variable('IMAP_HOST')
        self.port = self._get_imap_variable('IMAP_PORT')
        self.username = self._get_imap_variable('IMAP_USERNAME')
        self.password = self._get_imap_variable('IMAP_PASSWORD')

    def _get_imap_variable(self, name):
        if name in os.environ:
            return os.environ[name]
        
        with open('.envrc', 'r') as f:
            for line in f:
                if line.startswith(f'export {name}='):
                    return line.split('=')[1].strip().strip('"')


class ProtonClient:
    def __init__(self):
        creds = IMAPCreds()
        self._client = IMAPClient(creds.host, creds.port, ssl=False)
        self._client.login(creds.username, creds.password)

    def __enter__(self):
        self._client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.__exit__(exc_type, exc_val, exc_tb)

    def find_messages(self, folder):
        select_info = self._client.select_folder(folder)
        print(f"Found {select_info[b'EXISTS']} messages in '{folder}'...")
        return self._client.search('ALL')

    def get_message_text(self, message_id):
        fetched = self._client.fetch(message_id, ['RFC822'])
        text_bytes = fetched[message_id][b'RFC822']
        return text_bytes.decode()

    def close(self):
        return self._client.logout()
