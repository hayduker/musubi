from math import prod

from trainer import count_tokens # this is a weird dependence

class Evaluator:
    def __init__(self):
        self.model = Model.read('model/model.pickle')

    def prob_spam_given_token(self, t):
        if t not in good_counts and t not in bad_counts:
            return 0.4
        
        rg = min(1, 2 * good_counts[t] / num_good)
        rb = min(1, bad_counts[t] / num_bad)
        return max(0.01, min(0.99, rb / (rg + rb)))

    def prob_spam(self, text: str):
        token_interest = {t: abs(0.5 - self.prob_spam_given_token(t))
                        for t in count_tokens(text).keys()}

        most_interesting = sorted(token_interest, key=token_interest.get, reverse=True)[:15]

        positive = prod([prob_spam_given_token(t)     for t in most_interesting])
        negative = prod([1 - prob_spam_given_token(t) for t in most_interesting])
        
        return positive / (positive + negative)

    def is_spam(self, text: str):
        return True if self.prob_spam(text) > 0.9 else False
