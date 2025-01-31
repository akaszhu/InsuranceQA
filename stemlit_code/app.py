import streamlit as st
from docx import Document
import pytesseract
from PIL import Image
import io
import tempfile
import re
import contextlib
from prompts import BRD_to_product_stories,refiner,BRD_to_QA_stories
from schema import UserStoryCollection,ProjectDetails,TestCaseCreateRequest
from openai_uitls import non_stream_get_response_bedrock,claude_response,invoke_claude_with_model #openai_response_structured,openai_response,non_stream_get_response_openai, 
import pandas as pd
from pdfminer.high_level import extract_text

st.set_page_config(
    page_title="Bajaj Insurance",  # Title of the app
    page_icon="👩🏻‍💻",  # Favicon (emoji or file path)
    layout="wide",  # Wide layout for better use of space
    initial_sidebar_state="expanded"  # Sidebar state: "expanded" or "collapsed"
)
# Function to convert DOCX to PDF
def convert_docx_to_pdf(docx_file):
    document = Document(docx_file)
    pdf_buffer = io.BytesIO()
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    for para in document.paragraphs:
        c.drawString(100, height - 50, para.text)
        height -= 20

    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

def chat_with_document(user_query, document_text):
    # Combine user query with the extracted text
    messages = [
        # {"role": "assistant", "content": "You are a helpful assistant who answers questions based on the provided document."},
        {"role": "user", "content": f"Document content: {document_text}\n\nQuestion: {user_query}"}
    ]
    # Use OpenAI or another model to generate a response
    response = non_stream_get_response_bedrock(messages=messages, max_tokens=1000, temperature=0.7)
 
    return response
# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        # Extract text from the PDF file
        response_data = []
        for i in range(0, 30):
            text = extract_text(pdf_path, page_numbers=[i])
            response_data.append(text)
        return response_data
    except Exception as e:
        # Handle any exceptions that may occur during the process
        print(f"Error extracting text: {e}")
        return None

def summarize_brd(analyzed_text,role):
    messages=[
        # {
        #     "role": "user",
        #     "content": [{"type": "text", "text": "hi"}],
        # },

        {"role":"user",
        "content": f"Create a neat summary for the {role} on this brd document. Make it personalized based on the story, This is the brd{analyzed_text}"
        }
    ]
    
    # st.write_stream(claude_response(messages=messages,max_tokens=2000,temperature=0.5))
    st.write(non_stream_get_response_bedrock(messages=messages,max_tokens=2000,temperature=0.5))

def display_story(result):
    st.session_state["story_created"].append(result)
    story_details = [story.__dict__ for story in result['story_details']]
    df = pd.DataFrame(story_details)
    st.header(result["module_name"])
    st.header(result["phase"])
    st.subheader(f"No of days to complete the sprint:{result['total_days_to_close_spirint']}")
    st.table(df)


if "brd_filter" not in st.session_state:
    st.session_state["brd_filter"] = ""

if "story_created" not in st.session_state:
    st.session_state["story_created"] = []

if "file_uploaded" not in st.session_state:
    st.session_state["file_uploaded"] = None

if "extracted_text" not in st.session_state:
    st.session_state["extracted_text"] = None

if "generated code" not in st.session_state:
    st.session_state["generated"] = []
def generate(test_cases):
    with st.spinner("Analyzing the given BRD"):
        prompt = BRD_to_product_stories.format(brd=test_cases)
        prompt=refiner+str(test_cases)
        messages=[
            {
                "role":"assistant",
                "content":prompt
            }
        ]
        response = invoke_claude_with_model(query=prompt,max_tokens=4096,temprature=0.3)# openai_response_structured(messages=messages,model="gpt-4o",max_tokens=4096,temperature=0.2,stream=False,output_model=ProjectDetails)
        response=response.__dict__
        modules=response[ "modules"]
        st.session_state["brd_filter"] = response
        del response["modules"]
        prompt = BRD_to_product_stories.format(brd=response)
        messages=[
            {
                "role":"system",
                "content":prompt
            }
        ]

    with st.spinner("User stories to assist sprint planning and story creation"):
        for i in modules:
            prompt = BRD_to_QA_stories.format(brd=test_cases)
            messages.append(
            {
                "role":"user",
                "content":str(i)+"\n make n number of detailed tasks helping managers and developers"
            }
            )
            prompt=str(i)+"\n make n number of detailed tasks helping managers and developers"
            result =invoke_claude_with_model(max_tokens=4096,temprature=0.2,query=prompt)#openai_response_structured(messages=messages,model="gpt-4o",max_tokens=4096,temperature=0.2,stream=False,output_model=UserStoryCollection)
            messages.append(
            {
                "role":"system",
                "content":str(result)
            }
            )
            # print(result.__dict__)
            
            result=result.__dict__
            st.session_state["story_created"].append(result)
            story_details = [story.__dict__ for story in result['story_details']]
            df = pd.DataFrame(story_details)
            st.header(result["module_name"])
            with st.expander(result["module_name"]):
                st.header(result["phase"])
                st.subheader(f"No of days to complete the sprint:{result['total_days_to_close_spirint']}")
                st.table(df)
                


    print(st.session_state["story_created"])
# Streamlit app
st.title("Bajaj Automated QA System: DOCX/PDF Text Extraction and Test Case Generation")

uploaded_file = st.file_uploader("Upload a DOCX or PDF file", type=["docx", "pdf"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".docx"):
        pdf_buffer = convert_docx_to_pdf(uploaded_file)
        pdf_file = pdf_buffer
    else:
        pdf_file = uploaded_file
    st.session_state["file_uploaded"] = pdf_file

    with st.spinner("Extracting text from document"):
        text = extract_text_from_pdf(pdf_file)
        st.session_state["extracted_text"] = text
    # st.write("Extracted Text:")
    # st.write(text)
    
    # Call the generate function with the extracted text
    options = ["Project Manger", "Product Manger", "QA Engineer","Devops Engineer","Frontend Developer","Backend Developer","Client"]


    selected_option = st.selectbox("Select an option to summarize:", options)   
    summary  = st.button("Summarize BRD")
    if summary:
        summarize_brd(st.session_state["extracted_text"],selected_option)
    
    st.subheader("Exclusive for Project and Product mangers")
    story_cases  = st.button("Generate story with BRD")
    if story_cases:
        generate(text)

    st.subheader("Chat with the Document")
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if st.session_state["extracted_text"]:
        user_query = st.chat_input("Ask a question about the document:")
        if user_query:
            # Combine extracted text for chatbot context
            extracted_text = "\n".join(st.session_state["extracted_text"])
            bot_response = chat_with_document(user_query, extracted_text)
            
            # Update chat history
            st.session_state["chat_history"].append({"user": user_query, "bot": bot_response})
        
        # Display conversation history
        for message in st.session_state["chat_history"]:
            st.chat_message("user").write(message["user"])
            st.chat_message("assistant").write(message["bot"])
    else:
        st.info("Please upload a document to chat with.")
    

