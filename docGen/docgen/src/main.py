import os
import streamlit as st
import sys
from prepare_code import CodeFetcher, Model

@st.cache_resource
def init(source):
    code = CodeFetcher(source)
    model = Model()
    return code, model

st.title("CodeXpert")

# Initialize session state for directory path
if "directory_path" not in st.session_state:
    st.session_state["directory_path"] = None

# Step 1: Input directory path
if st.session_state["directory_path"] is None:
    directory_path = st.text_input("Enter directory path or GitHub repo link:")
    if directory_path and os.path.isdir(directory_path):
        st.session_state["directory_path"] = directory_path
        st.rerun()  # Force rerun to update UI
    elif directory_path:
        st.error("The provided path is not a valid directory.")
else:
    directory_path = st.session_state["directory_path"]

if directory_path:
    code, model = init(directory_path)
    code_content = code.code_content

    if 'ERROR' in code_content:
        st.error(code_content)
        sys.exit(1)

    # Sidebar: Display interactive file list
    st.sidebar.title("Project Files")
    selected_file = st.sidebar.selectbox("Select a file:", options=["All Files"] + list(code_content.keys()))
    
    if selected_file != "All Files":
        st.sidebar.markdown(f"**Selected File:** '{selected_file}'")

    st.sidebar.markdown("---")
    
    # Add High-Level Design button at bottom of sidebar
    if st.sidebar.button("Generate High-Level Design"):
        with st.spinner("Analyzing codebase and generating design document..."):
            if selected_file == "All Files":
                # Generate summary and design for all files
                summary = model.generate_detailed_summary(code_content)
                design = model.generate_high_level_design(summary)
            else:
                # Generate summary and design for selected file only
                file_content = {selected_file: code_content[selected_file]}
                summary = model.generate_detailed_summary(file_content)
                design = model.generate_high_level_design(summary)
            
            # Display results in main area
            st.header("Code Analysis")
            
            # Display detailed summary
            #st.subheader("Detailed Summary")
            #st.markdown(summary)
            
            # Add separator
            #st.markdown("---")
            
            # Display high-level design
            st.subheader("High-Level Design")
            st.markdown(design)
    
    # Step 3: Chat interface for user queries
    st.subheader("Talk to your code")
    question = st.text_input("")

    if st.button("Ask!"):
        if question.strip():
            with st.spinner("Analyzing files and generating response..."):
                if selected_file == "All Files":
                    # Pass all file data if "All Files" is selected
                    response = model(question)
                else:
                    # Pass only the selected file's content
                    response = model(question, {selected_file: code_content[selected_file]})
            st.markdown(response)
        else:
            st.error("Please enter a question.")
