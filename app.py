import streamlit as st
import os
from utils.audio_utils import extract_text_from_audio
from utils.summarizer import generate_summary

# Ensure folders exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

st.set_page_config(page_title="🎧 Podcast Summary Generator", layout="centered")

st.title("🎙️ Podcast Summary Generator")
st.markdown("Upload your podcast audio file, and get a quick. AI-generated summary!")

uploaded_file = st.file_uploader("Upload your podcast (MP3/M4A/WAV)", type=["mp3", "m4a", "wav"])
if uploaded_file is not None:
    try:
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    except Exception as e:
        st.error(f"❌ Error saving file: {str(e)}")
        st.stop()

    st.success("✅File uploaded successfully!")
    st.audio(file_path, format="audio/mp3")

    if st.button("Generate Summary"):
        with st.spinner("🎧Extracting text from audio and generating summary... Please wait."):
            # Extract text from audio
            transcript = extract_text_from_audio(file_path)
            if transcript.startswith("❌"):
                st.error(transcript)
            else:
                st.subheader("Transcript:")
                st.write(transcript)

                #step 2: Generate summary
                summary = generate_summary(transcript)
                st.subheader("📃summary:")
                st.write(summary)

                #save summary
                output_path = os.path.join("outputs", uploaded_file.name+"_summary.txt")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(summary)

                st.success("✅ summary generated and saved!")
                st.download_button(
                    label="Download Summary",
                    data=summary,
                    file_name="podcast_summary.txt",
                    mime="text/plain"
                )
                
                # Clean up the uploaded file
                try:
                    os.remove(file_path)
                except Exception:
                    pass  # Ignore cleanup errors
else:
    st.info("upload an audio file to begin.")