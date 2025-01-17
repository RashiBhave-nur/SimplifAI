import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI()
# openai_api_key = os.getenv("OPENAI_API_KEY")

# def read_files_in_directory(directory_path):
#     file_data = {}
#     try:
#         for root, _, files in os.walk(directory_path):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 relative_path = os.path.relpath(file_path, directory_path)  # Include relative path
#                 with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
#                     file_data[relative_path] = f.read()  # Use relative path as the key

#         return file_data
#     except Exception as e:
#         return {"ERROR": str(e)}

# def generate_chat_response(question, file_data):
#     try:
#         file_summary = "\n\n".join([f"File: {name}\nContent:\n{content}..." for name, content in file_data.items()])
#         prompt = f"""
#         You are an assistant that provides insights about files in a directory.
#         Below are the files and their content:

#         {file_summary}

#         Here is the user's question:
#         {question}

#         Please provide a detailed and accurate answer.
#         """
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{'role': 'user', 'content': prompt}],
#             max_tokens=500,
#             temperature=0.7
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"An error occurred: {e}"

# st.title("CodeXpert")

# # Initialize session state for directory path
# if "directory_path" not in st.session_state:
#     st.session_state["directory_path"] = None

# # Step 1: Input directory path
# if st.session_state["directory_path"] is None:
#     directory_path = st.text_input("Enter the path to a directory:", placeholder="/path/to/your/directory")
#     if directory_path and os.path.isdir(directory_path):
#         st.session_state["directory_path"] = directory_path
#         st.rerun()  # Force rerun to update UI
#     elif directory_path:
#         st.error("The provided path is not a valid directory.")
# else:
#     directory_path = st.session_state["directory_path"]

# # Step 2: Display files in a tree structure in the sidebar and read the files
# if directory_path:
#     file_data = read_files_in_directory(directory_path)
    
#     if "ERROR" in file_data:
#         st.error(f"Error reading files: {file_data['Error']}")
#     else:
#         # Sidebar: Display interactive file list
#         st.sidebar.title("Project Files")
#         selected_file = st.sidebar.selectbox("Select a file:", options=["All Files"] + list(file_data.keys()))
        
#         if selected_file != "All Files":
#             st.sidebar.markdown(f"**Selected File:** `{selected_file}`")
        
#         # Step 3: Chat interface for user queries
#         st.subheader("Ask Questions About Your Files")
#         question = st.text_input("Enter your question:")
        
#         if st.button("Get Answer"):
#             if question.strip():
#                 with st.spinner("Analyzing files and generating response..."):
#                     if selected_file == "All Files":
#                         # Pass all file data if "All Files" is selected
#                         response = generate_chat_response(question, file_data)
#                     else:
#                         # Pass only the selected file's content
#                         response = generate_chat_response(question, {selected_file: file_data[selected_file]})
#                 st.markdown(response)
#             else:
#                 st.error("Please enter a question.")

print('Always printed')

if st.button('Button'):
    print('Button clicked')