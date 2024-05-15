from app.services.transcription import WhisperInference, ASRInference, TTSInference
from app.services.translation import NLLBInference, GPTInference
from app.services.image_description import describe_image
from app.services.gps_detection import requires_gps
from langchain_community.llms import OpenAI
import yaml
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the current file path
app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
class Pipeline:
    def __init__(self, config_file:str):
        # Load the YAML file
        with open(f'{app_path}/config/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
            
        self.load_models(self.config)
        
    def load_models(self, config):
        #Fetch the API key from environment
        
        
        # Initialize models
        self.gpt4_text = OpenAI(model_name=self.config['models']['gpt4_text'], openai_api_key=openai_api_key)
        # Initialize OpenAI GPT-4
        self.whisper = WhisperInference(model_name=config['models']['whisper'])
        self.asr = ASRInference(model_name=config['models']['asr'])
        self.tts = TTSInference(model_name=config['models']['tts'])
        self.gpt4_chat = GPTInference(model_name=config['models']['gpt4_chat'])
        self.nllb = NLLBInference(model_name=config['models']['nllb'])
        
    def pipeline_att(self, audio_file:str, language:str):
        if language == "yo":
            transcription = self.whisper.inference(audio_file)
            print(transcription)
            return self.gpt4_chat.inference(transcription, src_lang="yo", target_lang="en")
        elif language == "fon":
            transcription = self.asr.inference(audio_file)
            print(transcription)
            return self.nllb.inference(transcription, target_lang="fr")
        else:
            raise ValueError("Unsupported language for pipeline_att")
        
    def pipeline_ta(self, text:str, language:str):
        if language == "yo":
            translate = self.gpt4_chat.inference(text, src_lang="en", target_lang="yo")
            print(translate)
            audio_array, audio_file = self.tts.inference(translate)
            return audio_file
        elif language == "fon":
            translate = self.nllb.inference(text, target_lang="fon")
            audio_array, audio_file = self.tts.inference(translate)
            return audio_file
        else:
            raise ValueError("Unsupported language for pipeline_ta")
        

if __name__ == '__main__':
    
    config_file = "/home/boubacar-diallo/LLAMA/Challenge/MAI/tourism_companion/app/config/config.yaml"
    pipe = Pipeline(config_file)
    
    import sys
    print(sys.path)
    
    audio_file = "tests/fon.wav"
    print(pipe.pipeline_att(audio_file, language="fon"))
    
    audio_file = "tests/yoruba.wav"
    print(pipe.pipeline_att(audio_file, language="yo"))
    
    text = "Xɛ́, nɛ̌ wɛ a ka gbɔn, nɔví ce?"
    print(pipe.pipeline_ta(text, language="fon"))
    
    text = "áfíríkà nínú ìgbìmọ̀ ààbò àjọ"
    print(pipe.pipeline_ta(text, language="yo"))