import re
from collections import Counter
from glob import glob

def remove_html_tags(text: str) -> str:
    comment_pattern = r'<!--.*?-->'
    # tag_pattern = r'<[^>]+>'
    return re.sub(comment_pattern, '', text, flags=re.DOTALL)

def valid_token(t: str) -> bool:
    return 1 < len(t) < 15 and not t.isdigit()

def count_tokens(filename):
    token_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-'$"
    token_pattern = f"[^{re.escape(token_chars)}]+"

    with open(filename, 'r') as f:
        without_tags = remove_html_tags(f.read())
        tokens = re.split(token_pattern, without_tags)
        tokens = [t.lower() for t in tokens]
        tokens = list(filter(valid_token, tokens))

    return Counter(tokens)

def count_corpus(glob_pattern):
    emails = glob(glob_pattern)
    return sum([count_tokens(e) for e in emails], Counter()), len(emails)

good_counts, num_good = count_corpus('good/g*.html')
bad_counts,  num_bad  = count_corpus('bad/b*.html')

