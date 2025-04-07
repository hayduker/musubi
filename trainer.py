import re
from collections import Counter
from glob import glob

from model import Model

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

    def update_counts(self, text: str, is_good: bool):
        counts = self.count_tokens(text)
        if is_good:
            self.model.good_counts += counts
            self.model.num_good_emails += 1
        else:
            self.model.bad_counts += counts
            self.model.num_bad_emails += 1
