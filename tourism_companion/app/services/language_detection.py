import pycld2 as cld2
import langid

def detect_language(text: str) -> str:
    is_reliable, _, details = cld2.detect(text)
    language = details[0][1]
    if language in ["yo", "fon"]:
        return language
    else:
        return langid.classify(text)[0]
