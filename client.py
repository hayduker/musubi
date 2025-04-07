from imapclient import IMAPClient
from tqdm import tqdm
import os

from trainer import Trainer


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




model_trainer = Trainer()

imap_creds = IMAPCreds()

with IMAPClient(host=imap_creds.host, port=imap_creds.port, ssl=False) as client:
    client.login(imap_creds.username, imap_creds.password)

    folder = 'Folders/Bad Truth'
    select_info = client.select_folder(folder)
    print(f"{select_info[b'EXISTS']} messages in {folder}")
    
    messages = client.search('ALL')

    for msgid, data in client.fetch(messages, ['RFC822']).items():
        rfc822 = data[b'RFC822']
        print(f'Counting ID #{msgid}...')
        model_trainer.update_counts(rfc822.decode(), is_good=False)

    print(model_trainer.model.num_bad_emails)
    print(model_trainer.model.bad_counts)
