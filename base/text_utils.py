import re
import unicodedata


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def text_to_id(text):
    """
    Convert input text to id.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    text = remove_accents(text.lower())
    text = re.sub(r"[ ]+", "_", text)
    text = re.sub(r"[^0-9a-zA-Z_-]", "", text)
    return text
