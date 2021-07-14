FILTER_WORDS = [
    "who",
    "http",
    "twitch",
    "onlyfans",
    "instagram",
    "snapchat",
    "website",
    "profile",
    "ethereum",
    "commentmessage"
    "snap",
    "youtube",
]


def is_valid_comment(raw_text):
    """ Makes sure the comment is not spam, is not just asking for who it is, does not contain link, and is somewhat long """
    comment_text = raw_text.lower()
    if len(comment_text) <= 14:
        return False

    for word in FILTER_WORDS:
        if comment_text.find(word) != -1:
            return False
    return True
