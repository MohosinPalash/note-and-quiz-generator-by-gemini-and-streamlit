import streamlit as st
from api_calling import note_generator, audio_transcriptor, quiz_generator

st.title("Note summary and Quiz Generator")
st.markdown("Note summary and 3 images to generate Note summary and quizzes")
st.divider()

with st.sidebar:
    st.header("Controls")
    images = st.file_uploader(
        "Upload Photo(s):",
        type = ['jpg', 'jpeg', 'png'],
        accept_multiple_files = True
    )

    if images:        
        if len(images) > 3:
            st.error("Uploaded more than 3 images")
        else:
            st.subheader("Uploaded images")
            col = st.columns(len(images))
            for i, img in enumerate(images):
                with col[i]:
                    st.image(img)

    difficulty = st.selectbox(
            "Difficulty Level:",
            ("Easy", "Medium", "Hard"),
            index = None
        )
    
    if difficulty:
        st.markdown(f"Selected Difficulty Level: **{difficulty}**")
    
        
    generate_pressed = st.button("Generate", type= "primary")

if generate_pressed:
    if not images:
        #Handle not images case
        st.error("You must upload atlease an image.")
    if not difficulty:
        st.error("Please select difficulty level")
    if images and difficulty:
        #Note
        with st.container(border = True):
            st.subheader("Note")
            with st.spinner("Thinking..."):
                generate_notes = note_generator(images)
                st.markdown(generate_notes)
                
        #Audio transcript
        with st.container(border = True):
            st.subheader("Audio Transcription")
            with st.spinner("Generating..."):
                audio_transcript = audio_transcriptor(generate_notes)
                st.audio(audio_transcript)
        
        #quiz
        with st.container(border = True):
            st.subheader(f"Quiz ({difficulty})")
            with st.spinner("Thinking..."):
                quizzes = quiz_generator(images, difficulty)
                st.markdown(quizzes)
        
    
