import streamlit as st
from prompts import BRD_to_product_stories,refiner,BRD_to_QA_stories
from schema import UserStoryCollection,ProjectDetails,TestCaseCreateRequest,TestCaseResponse
from openai_uitls import openai_response_structured,openai_response,non_stream_get_response_openai_preview
import pandas as pd
import re
import contextlib
from url import get_all_routes
if "testcase_created" not in st.session_state:
    st.session_state["testcase_created"]=[]
#
if "base_url" not in st.session_state:
    st.session_state["base_url"] = ""
if "login_url" not in st.session_state:
    st.session_state["login_url"] = ""
if "username" not in st.session_state:
            st.session_state["username"] = ""
if "password" not in st.session_state:
    st.session_state["password"] = ""
if "scrapped_url" not in st.session_state:
    st.session_state["scrapped_url"] = ""
if "generated_code" not in st.session_state:
    st.session_state["generated_code"]=[]
def generate(test_cases):

    with st.spinner("Analyzing the given BRD"):
        prompt = BRD_to_product_stories.format(brd=test_cases)
        prompt=refiner+str(test_cases)
        messages=[
            {
                "role":"system",
                "content":prompt
            }
        ]
       
        response = openai_response_structured(messages=messages,model="gpt-4o",max_tokens=4096,temperature=0.2,stream=False,output_model=ProjectDetails)
        response=response.__dict__
        modules=response[ "modules"]
    
        st.session_state["brd_filter"] = response
        del response["modules"]
        prompt = BRD_to_product_stories.format(brd=response)
        messages=[
            {
                "role":"system",
                "content":prompt
            }]

    with st.spinner("Creating Test cases to assist....."):

        for i in modules:
            prompt = BRD_to_QA_stories.format(brd=test_cases)
            messages.append(
            {
                "role":"user",
                "content":str(i)+"\n make n number of detailed test cases helping QA to full fledged testing on it"
            }
            )
            
            result =openai_response_structured(messages=messages,model="gpt-4o",max_tokens=4096,temperature=0.2,stream=False,output_model=TestCaseResponse)
            messages.append(
            {
                "role":"system",
                "content":str(result)
            }
            )
            # print(result.__dict__)
            
            result=result.__dict__
            st.session_state["testcase_created"].append(result)
            story_details = [story.__dict__ for story in result['test_cases']]
            for i in range(0,len(story_details)):
                story = story_details[i]

                steps_list = story["steps_to_execute"] 
                steps_list = str([str(step) for step in steps_list]).replace("[","").replace("]","")
                story_details[i]["steps_to_execute"]  = steps_list
               
            df = pd.DataFrame(story_details)
            st.header(result["module_name"])
            # with st.expander(result["module_name"]):
            st.table(df)
            for i in story_details:

                prompt=f"""
You are given a test case to check the functionality of a web application. Below are the specific instructions and details for your task:

1. **Task Overview**:
- Write Selenium code in Python that is directly executable to test the web application.
- Use the provided `username`, `password`, and `login_url` to log in and verify functionality.
- keep the timout for 1 min for all the process no no time ouT  all
2. **Resources Provided**:
- A list of page routes.
- Scraped HTML content of the web pages.
- Credentials for logging into the application:
    




5. **Output Format**:
- Provide the Selenium Python code in a clean and properly indented format.
- The output should be standalone executable code, ready to be saved into a Python file.

6. **Test Case Details**:
- Refer to the following for test-specific instructions: `{i}`

---

**Output Format**:
```
# Python Selenium code starts here

<code>

# Python Selenium code ends here
```

**Note**: Do not include additional explanations, comments, or text before or after the code block. verify once from your end and give the code


"""
                messages=[
                        {
                            "role":"user",
                            "content":prompt
                        }
                    ]
                with st.spinner("creating sample code..."):
                    response = non_stream_get_response_openai_preview(messages=messages,max_tokens=4096,model="o1-preview",stream=False,temperature=0.8)
                    # response = {'response': '```python\nfrom selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.common.keys import Keys\nimport time\n\n# Initialize the Chrome driver\ndriver = webdriver.Chrome()\n\n# Open the login page\ndriver.get("http://3.83.24.72:8000/")\n\n# Find the username and password fields and enter the credentials\nusername_field = driver.find_element(By.NAME, "username")\npassword_field = driver.find_element(By.NAME, "password")\n\nusername_field.send_keys("user")\npassword_field.send_keys("letuserpass")\n\n# Find the login button and click it\nlogin_button = driver.find_element(By.XPATH, "//button[@type=\'submit\']")\nlogin_button.click()\n\n# Wait for the page to load\ntime.sleep(3)\n\n# Navigate to the Attendance section\nattendance_link = driver.find_element(By.LINK_TEXT, "Attendance")\nattendance_link.click()\n\n# Wait for the page to load\ntime.sleep(3)\n\n# Test the Check-In feature\ncheck_in_button = driver.find_element(By.XPATH, "//button[contains(text(), \'Check-In\')]")\ncheck_in_button.click()\n\n# Wait for the action to complete\ntime.sleep(2)\n\n# Test the Check-Out feature\ncheck_out_button = driver.find_element(By.XPATH, "//button[contains(text(), \'Check-Out\')]")\ncheck_out_button.click()\n\n# Wait for the action to complete\ntime.sleep(2)\n\n# Close the browser\ndriver.quit()\n```'}
                    # print(response)
                    
                    pattern = r'```(.*?)```'
                    match = re.search(pattern, response["response"], re.DOTALL)

                    if match:
                        python_code = match.group(1).strip().replace("python","")
                        with st.expander(i["title"]):
                            st.session_state["generated_code"].append(python_code)
                            st.code(python_code)


if st.session_state["extracted_text"] is not None:
    
    st.subheader("Welcome to QA Assistance with BRD 🛫")
    st.write("Enter Website cred Details")
    if st.session_state["base_url"] =="":
        with st.form(key='api_details_form'):
            base_url = st.text_input("Base URL", '')
            login_url = st.text_input("Login URL", '')
            username = st.text_input("Username", 'user')
            password = st.text_input("Password", type='password')

            submit_button = st.form_submit_button(label='Submit')

            # If the form is submitted, store the details in session state
            if submit_button:
                st.session_state["base_url"] = base_url
                st.session_state["login_url"] = login_url
                st.session_state["username"] = username
                st.session_state["password"] = password

            st.success("API details have been saved to session state.")
    st.write("Session State Details:")
    st.write(f"Base URL: {st.session_state.get('base_url')}")
    st.write(f"Login URL: {st.session_state.get('login_url')}")
    st.write(f"Username: {st.session_state.get('username')}")
    st.write(f"Password: {st.session_state.get('password')}")
    if st.session_state["base_url"] !="":
        bt = st.button("Generate Test cases")
        if bt:
            bt1 = st.button("Extract Urls")
            if bt1:
                with st.spinner("Fetching all the routes"):
                    with st.expander("List of all the routes in the given test link"):
                        if st.session_state["scrapped_url"] == "":
                            urls=get_all_routes(st.session_state["base_url"],st.session_state["login_url"] ,st.session_state["username"] , st.session_state["password"])
                            st.write(urls)
                        else:
                            st.write(st.session_state["scrapped_url"])
        
            # with st.expander()
            generate(st.session_state["extracted_text"])

        clear_bt1 = st.button("Test new webpage")
        if clear_bt1:
            st.session_state["base_url"] = ""
            st.session_state["login_url"] = ""
            st.session_state["username"] = ""
            st.session_state["password"] = ""


else:
    st.warning("You have to upload BRD in the home page")