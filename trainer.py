import re
from collections import Counter
from glob import glob
from tqdm import tqdm

from model import Model
from client import ProtonClient


class Trainer:
    token_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-'$"
    token_pattern = f"[^{re.escape(token_chars)}]+"

    def __init__(self):
        self.model = Model()

    def remove_html_tags(self, text: str) -> str:
        comment_pattern = r'<!--.*?-->'
        # tag_pattern = r'<[^>]+>'
        return re.sub(comment_pattern, '', text, flags=re.DOTALL)

    def valid_token(self, t: str) -> bool:
        return 1 < len(t) < 15 and not t.isdigit()

    def count_tokens(self, text: str) -> Counter:
        without_tags = self.remove_html_tags(text)
        tokens = re.split(self.token_pattern, without_tags)
        tokens = [t.lower() for t in tokens]
        tokens = list(filter(self.valid_token, tokens))
        return Counter(tokens)

    def count_folder(self, client, folder, is_good):
        messages_ids = client.find_messages(folder)
        for message_id in tqdm(messages_ids):
            text = client.get_message_text(message_id)
            self.update_counts(text, is_good)

    def update_counts(self, text: str, is_good: bool):
        counts = self.count_tokens(text)
        if is_good:
            self.model.good_counts += counts
            self.model.num_good_emails += 1
        else:
            self.model.bad_counts += counts
            self.model.num_bad_emails += 1
    
    def write_model(self, path: str):
        self.model.write(path)

    def train_model(self):
        with ProtonClient() as client:
            self.count_folder(client, 'Folders/Good Truth', is_good=True)
            print(f'Counted {len(self.model.good_counts)} tokens from good emails...\n')

            self.count_folder(client, 'Folders/Bad Truth', is_good=False)
            print(f'Counted {len(self.model.bad_counts)} tokens from bad emails...\n')

            filename = 'model/model.pickle'
            print(f'Writing model to {filename}...')
            self.write_model(filename)

            print('Done.\n')


if __name__ == "__main__":
    Trainer().train_model()
