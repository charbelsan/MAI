import ast
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
  
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that translates {input_language} to {output_language}.",
        ),
        ("human", "{input}"),
    ]
)

langs = {
    "yo": "Yoruba",
    "fr": "French",
    "en": "English",
}

class GPTInference:
    def __init__(self, model_name="gpt-4o", temperature=0):
        # self.model = OpenAI(model_name=model_name) # Set up OpenAI GPT-4
        self.model = ChatOpenAI(model_name=model_name, temperature=0, max_tokens=150, verbose=True)
        
    def inference(self, text, src_lang="yo", target_lang="fr"):
        chain = prompt | self.model
        print(f"Translation : {langs[f'{src_lang}']} To {langs[f'{target_lang}']}")
        result = chain.invoke(
            {"input_language": f"{langs[f'{src_lang}']}", 
             "output_language": f"{langs[f'{target_lang}']}", 
             "input": f"{text}"
            })
        return result.content

langs_nllb = {
    "fon": "fon_Latn",
    "fr": "fra_Latn",
    "en": "eng_Latn",
}

class NLLBInference:
    def __init__(self, model_name="facebook/nllb-200-distilled-600M"):
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.processor = AutoTokenizer.from_pretrained(model_name)
    
    def inference(self, text, target_lang="fr"):
        inputs = self.processor(text, return_tensors="pt")
        translated_tokens = self.model.generate(
            **inputs, forced_bos_token_id=self.processor.lang_code_to_id[f"{langs_nllb[f'{target_lang}']}"], max_length=150
        )
        text_output = self.processor.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return text_output


if __name__ == '__main__':
    import os
    # current_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # import yaml
    # # Load the YAML file
    # with open(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/config/config.yaml', 'r') as file:
    #     config = yaml.safe_load(file)
        
    # print(config['models']['gpt4_model'])
    
    # quit()
    
    # import os
    # os.environ["OPENAI_API_KEY"] = "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"
    
    # gpt4o = GPTInference(model_name="gpt-4o")
    
    # text = "ṣùgbọ́n ọlọpáá alábòójútó ìhámọ́ lé"
    # print(gpt4o.inference(text, src_lang="yo", target_lang="fr"))
    # print(gpt4o.inference(text, src_lang="yo", target_lang="en"))
    
    # text = "Cependant, le policier superviseur a souri"
    # print(gpt4o.inference(text, src_lang="fr", target_lang="yo"))
    # print(gpt4o.inference(text, src_lang="fr", target_lang="en"))
    
    # text = "However, the supervising police officer smiled"
    # print(gpt4o.inference(text, src_lang="en", target_lang="yo"))
    # print(gpt4o.inference(text, src_lang="en", target_lang="fr"))
    
    # print("="*50)
    
    # nllb = NLLBInference(model_name="facebook/nllb-200-distilled-600M")
    
    # text = "Xɛ́, nɛ̌ wɛ a ka gbɔn, nɔví ce?"
    # print(nllb.inference(text, target_lang="en"))
    
    # text = "C'est quoi, mon frère?"
    # print(nllb.inference(text, target_lang="fon"))
    
    
    # import pygame.mixer
    # pygame.mixer.init()
    # def play_mp3(file_path):
    #     pygame.mixer.music.load(file_path)
    #     pygame.mixer.music.play()
    #     while pygame.mixer.music.get_busy():
    #         pygame.time.Clock().tick(10)
            
    # print("Speak a prompt...")
    # play_mp3("/home/boubacar-diallo/LLAMA/Challenge/MAI/temp.wav")