import streamlit as st
from agent import PodcastAgent 

st.title("🎙️ Blog to Podcast")
st.write("Paste a blog URL and generate a podcast episode instantly.")

if "agent" not in st.session_state:
    st.session_state.agent = PodcastAgent()

url = st.text_input("Blog URL",placeholder="https://example.com/article")

if st.button("Generate Podcast"):
    if url:
        with st.spinner('Generating Audio....'):
            audio = st.session_state.agent.blog_to_podcast(url)

        st.subheader("🎧 Listen")
        st.audio(audio, format="audio/mp3", start_time=0)

        st.download_button(
            label="⬇️ Download MP3",
            data=audio,
            file_name="podcast.mp3",
            mime="audio/mp3"
        )
    else:
        st.warning("Please enter a URL first.")
