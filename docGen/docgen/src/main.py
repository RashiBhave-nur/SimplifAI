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

# Initialize session state for directory path, chat history, and selected file
if "directory_path" not in st.session_state:
    st.session_state["directory_path"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Step 1: Input directory path
if st.session_state["directory_path"] is None:
    directory_path = st.text_input("Enter directory path or GitHub repo link:")
    if directory_path:
        st.session_state["directory_path"] = directory_path
        st.rerun()  # Force rerun to update UI
    elif directory_path:
        st.error("The provided path is not a valid directory.")
else:
    directory_path = st.session_state["directory_path"]
    if st.sidebar.button("Reset Directory"):
        st.session_state["directory_path"] = None
        st.session_state["messages"] = []
        st.rerun()  # Reset the app state

if directory_path:
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

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
        st.sidebar.markdown("### File Contents:")
        st.sidebar.code(code_content[selected_file])

    st.sidebar.markdown("---")

    # Add High-Level Design button at bottom of sidebar
    if st.sidebar.button("Generate High-Level Design"):
        with st.spinner("Analyzing codebase and generating design document..."):
            if selected_file == "All Files":

                filtered_content = model.filter_important_files(code_content)
                batched_content = model.batch_process_files(filtered_content) 

                summaries = []
                progress_bar = st.progress(0)
                for i, batch in enumerate(batched_content):
                    summary = model.generate_detailed_summary(batch)
                    summaries.append(summary)
                    progress_bar.progress((i + 1) / len(batched_content))
                
                # Combine summaries and generate final design
                combined_summary = model.combine_summaries(summaries)
                design = model.generate_high_level_design(combined_summary)
                # Generate summary and design for all files
            else:
                # Generate summary and design for selected file only
                file_content = {selected_file: code_content[selected_file]}
                summary = model.generate_detailed_summary(file_content)
                design = model.generate_high_level_design(summary)
            
            # Display results in main area
            # st.header("Code Analysis")

            # Display high-level design
            st.subheader("High-Level Design")
            st.markdown(design)
    
    # Step 3: Chat interface for user queries
    # st.subheader("Talk to your code")
    # question = st.text_input("Ask a question:", label_visibility="collapsed")
    
    if prompt := st.chat_input("Ask a question"):
        # Add prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Get answer
        # result, sources = model.retrieval_qa_inference(prompt)
        response = None
        with st.spinner("Analyzing file(s)..."):
            if selected_file == "All Files":
                st.error("Please select a file to ask questions.")
            else:
                response = model(code_content[selected_file], prompt)

        # Add answer and sources
        st.chat_message("assistant").write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # if st.button("Ask!"):
    #     response = None
    #     if question.strip():
    #         with st.spinner("Analyzing files and generating response..."):
    #             if selected_file == "All Files":
    #                 st.error("Please select a file to ask questions.")
    #             else:
    #                 response = model(code_content[selected_file], question)
    #         if response:
    #             st.markdown(response)
    #     else:
    #         st.error("Please enter a question.")
