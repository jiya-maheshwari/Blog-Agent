import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from tools import blog_scraper
from langchain.agents import create_agent

load_dotenv()

class PodcastAgent:
    def __init__(self):
        self.audio_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
        self.agent = create_agent(
                        name='Blog Summarizer',
                        model = self.model,
                        tools = [blog_scraper],
                        system_prompt = ["You are a blog-to-podcast conversion agent. "
                                "Use the scrape_blog tool to extract the article content from the provided URL. "
                                "Then transform it into a clear, concise, conversational podcast script "
                                "(maximum 2000 characters). "
                                "The script should sound natural when spoken aloud, flow logically, "
                                "and highlight the key ideas without unnecessary filler. "
                                "Do not use markdown formatting."
                ]
        )

    def audio_converter(self,text):
        audio = self.audio_client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        )
        return audio
    

    def blog_to_podcast(self,url):
        audio_summary = self.agent.invoke({'input':f'Convert this URL: {url} to a podcast summary'})
        return audio_summary

    








