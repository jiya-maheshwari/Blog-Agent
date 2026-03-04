import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from tools import blog_scraper
from langchain.agents import create_agent
from gtts import gTTS
import io

load_dotenv()

def get_secret(key):
    try:
        import streamlit as st
        return st.secrets[key]
    except:
        return os.getenv(key)


class PodcastAgent:
    def __init__(self):
        self.audio_client = ElevenLabs(api_key=get_secret("ELEVENLABS_API_KEY"))
        self.model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        self.agent = create_agent(
                        name='Blog Summarizer',
                        model = self.model,
                        tools = [blog_scraper],
                        system_prompt = ("You are a blog-to-podcast conversion agent. "
                                "Use the scrape_blog tool to extract the article content from the provided URL. "
                                "Then transform it into a clear, concise, conversational podcast script "
                                "(maximum 2000 characters). "
                                "The script should sound natural when spoken aloud, flow logically, "
                                "and highlight the key ideas without unnecessary filler. "
                                "Do not use markdown formatting."
                        )
        )

    def generate_summary(self,url):
        summary = self.agent.invoke({'messages':[{'role':'user','content':f'Convert this URL: {url} to a podcast script'}]})
        result = summary.get("messages", [])
        last = result[-1].content if result else str(summary)
        if isinstance(last, list):
            res = []
            for block in last:
                if block:
                    res.append(block.get("text", ""))
            return "".join(res)
        return last


    def audio_converter(self,text):
        # audio = self.audio_client.text_to_speech.convert(
        # text=text,
        # voice_id="JBFqnCBsd6RMkjVDRZzb",
        # model_id="eleven_multilingual_v2",
        # output_format="mp3_44100_128",
        # )
        
        # chunks = []
        # for chunk in audio:
        #     if chunk:
        #         chunks.append(chunk)
    
        # return b"".join(chunks)
        tts = gTTS(text=text, lang='en')
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    

    def blog_to_podcast(self,url):
        text = self.generate_summary(url)
        audio_summary = self.audio_converter(text)
        return audio_summary










