from langchain.llms import OpenAI
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Set up OpenAI GPT-4
gpt4_model = OpenAI(model_name="gpt-4")

# Initialize models for Fon translation
nllb_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
nllb_tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    if source_lang == "yo":
        return gpt4_model.Completion.create(prompt=f"Translate the following Yoruba text to {target_lang}:\n{text}").choices[0].text.strip()
    elif source_lang == "fon":
        inputs = nllb_tokenizer(text, return_tensors="pt", padding=True)
        translated_tokens = nllb_model.generate(**inputs)
        translated_text = nllb_tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        if target_lang == "en":
            return gpt4_model.Completion.create(prompt=f"Translate the following French text to English:\n{translated_text}").choices[0].text.strip()
        else:
            return translated_text
    else:
        raise ValueError("Unsupported source language for translation")
