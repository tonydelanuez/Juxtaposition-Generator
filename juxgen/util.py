from flask import Response, make_response

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
    "commentMessage" "snap",
    "youtube",
    "80.re",
    "@",
]


def serve_image(raw: bytes) -> Response:
    response = make_response(raw)
    response.headers.set("Content-Type", "image/jpeg")
    response.headers.set("Content-Disposition", "attachment", filename="image.png")
    return response


class CommentFilter:
    @staticmethod
    def is_valid_comment(raw_text: str) -> bool:
        """Makes sure the comment is not spam, is not just asking for who it is,
        does not contain link, and is somewhat long"""
        comment_text = raw_text.lower()
        if len(comment_text) <= 14:
            return False

        for word in FILTER_WORDS:
            if comment_text.find(word) != -1:
                return False
        return True
