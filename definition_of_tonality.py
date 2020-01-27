from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel


def analysis(comments):
    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    messages = [
        comments
    ]
    results = model.predict(messages, k=1)
    for tonality in results[0]:
        pass
    return tonality
