from math import prod

def prob_spam_given_token(t):
    if t not in good_counts and t not in bad_counts:
        return 0.4
    
    rg = min(1, 2 * good_counts[t] / num_good)
    rb = min(1, bad_counts[t] / num_bad)
    return max(0.01, min(0.99, rb / (rg + rb)))

def prob_spam(filename):
    token_interest = {t: abs(0.5 - prob_spam_given_token(t))
                      for t in count_tokens(filename).keys()}

    most_interesting = sorted(token_interest, key=token_interest.get, reverse=True)[:15]

    positive = prod([prob_spam_given_token(t)     for t in most_interesting])
    negative = prod([1 - prob_spam_given_token(t) for t in most_interesting])
    
    return positive / (positive + negative)

def is_spam(filename):
    return True if prob_spam(filename) > 0.9 else False