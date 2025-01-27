from openai_uitls import non_stream_get_response_openai_preview,openai_response_structured
import os
from bs4 import BeautifulSoup
import json
import streamlit as st
import io
current_working_directory = os.getcwd()
html_data  =os.path.join(current_working_directory, "scraped_data.json")
image_path  =os.path.join(current_working_directory, "screenshots")

def main(query):
    try:
        query="""Check-in and check-out functionality"""
        prompt=f"""
        Your are give with a test case for checking a web app,
        for that i am giving you all the routes of the webpage, i want you to identify in which of the routes the test case case can be tested or found to test
        test case:
        {query}

        return exactly 2 urls only
        url of all the routes:
        [
            "http://aris-api.goml.io/helpdesk/faq-view/2/",
            "https://aris-api.goml.io/employee/organisation-chart/",
            "https://aris-api.goml.io/configuration/holiday-view",
            "https://aris-api.goml.io/payroll/view-reimbursement/",
            "http://aris-api.goml.io/attendance/",
            "https://aris-api.goml.io/pms/view-meetings/",
            "https://aris-api.goml.io/helpdesk/faq-view/3/",
            "http://aris-api.goml.io/pms/feedback-view/",
            "http://aris-api.goml.io/helpdesk/faq-view/1/",
            "https://aris-api.goml.io/employee/employee-profile/",
            "https://aris-api.goml.io/attendance/attendance-overtime-view/?year=2024",
            "https://aris-api.goml.io/employee/employee-view/",
            "https://aris-api.goml.io/employee/disciplinary-actions/",
            "https://aris-api.goml.io/pms/objective-list-view/",
            "http://aris-api.goml.io/leave/leave-allocation-request-view/",
            "https://aris-api.goml.io/leave/user-request-view/",
            "https://aris-api.goml.io/leave/leave-employee-dashboard?dashboard=true",
            "https://aris-api.goml.io/payroll/view-payslip/",
            "https://aris-api.goml.io/attendance/view-my-attendance/",
            "http://aris-api.goml.io/employee/employee-view/",
            "https://aris-api.goml.io/helpdesk/faq-view/4/",
            "http://aris-api.goml.io/pms/view-meetings/",
            "http://aris-api.goml.io/employee/disciplinary-actions/",
            "https://aris-api.goml.io/attendance/attendance-overtime-view/",
            "https://aris-api.goml.io/helpdesk/faq-category-view/",
            "http://aris-api.goml.io/pms/objective-list-view/",
            "http://aris-api.goml.io/helpdesk/faq-view/3/",
            "https://aris-api.goml.io",
            "http://aris-api.goml.io/attendance/late-come-early-out-view/",
            "https://aris-api.goml.io/leave/restrict-view",
            "https://aris-api.goml.io/employee/employee-profile",
            "https://aris-api.goml.io/asset/asset-request-allocation-view/",
            "https://aris-api.goml.io/pms/view-key-result/",
            "http://aris-api.goml.io/employee/",
            "https://aris-api.goml.io/employee/work-type-request-view/",
            "https://aris-api.goml.io/pms/dashboard-view",
            "http://aris-api.goml.io/",
            "http://aris-api.goml.io/attendance/attendance-overtime-view/",
            "https://aris-api.goml.io/employee/shift-request-view/",
            "https://aris-api.goml.io/",
            "https://aris-api.goml.io/helpdesk/faq-view/1/",
            "https://aris-api.goml.io/employee/view-policies/",
            "https://aris-api.goml.io/pms/employee-bonus-point",
            "http://aris-api.goml.io/attendance/attendance-activity-view/",
            "http://aris-api.goml.io/employee/shift-request-view/",
            "http://aris-api.goml.io/attendance/request-attendance-view/",
            "https://aris-api.goml.io/i18n/setlang/",
            "http://aris-api.goml.io/asset/asset-request-allocation-view/",
            "https://aris-api.goml.io/forgot-password",
            "http://aris-api.goml.io/employee/employee-profile/",
            "http://aris-api.goml.io/helpdesk/faq-view/4/",
            "http://aris-api.goml.io/payroll/view-payslip/",
            "https://aris-api.goml.io/attendance/late-come-early-out-view/",
            "https://aris-api.goml.io/employee/edit-profile",
            "http://aris-api.goml.io/leave/",
            "http://aris-api.goml.io/helpdesk/ticket-view/",
            "https://aris-api.goml.io/helpdesk/faq-view/2/",
            "http://aris-api.goml.io/attendance/view-my-attendance/",
            "http://aris-api.goml.io/employee/organisation-chart/",
            "http://aris-api.goml.io/pms/",
            "http://aris-api.goml.io/employee/view-policies/",
            "http://aris-api.goml.io/helpdesk/faq-category-view/",
            "http://aris-api.goml.io/employee/work-type-request-view/",
            "http://aris-api.goml.io/payroll/",
            "http://aris-api.goml.io/payroll/view-reimbursement/",
            "http://aris-api.goml.io/attendance/attendance-overtime-view/?year=2024",
            "https://aris-api.goml.io/attendance/attendance-activity-view/",
            "https://aris-api.goml.io/helpdesk/ticket-view/",
            "https://aris-api.goml.io/configuration/company-leave-view",
            "http://aris-api.goml.io/leave/user-request-view/",
            "https://aris-api.goml.io/pms/feedback-view/",
            "https://aris-api.goml.io/leave/leave-allocation-request-view/",
            "https://aris-api.goml.io/attendance/request-attendance-view/",
            "https://aris-api.goml.io/change-password"
        ]
        """
        messages=[
            {"role":"system","content":prompt}
        ]
        from pydantic import BaseModel

        class Urlname(BaseModel):
            url:str
        class Findurl(BaseModel):
            route_list:list[Urlname]

        list_data=openai_response_structured(messages=messages,max_tokens=200,stream=False,output_model=Findurl,temperature=0.8)

        route_list = list_data.route_list

        # Extract the URLs from the route_list
        url_list = [urlname.url for urlname in route_list]
        # print(url_list)
        st.subheader("Urls to test:")
        for i in url_list:
            st.write(i)
        st.divider()
        st.subheader("Cleaned HTML of the page:")
        def clean_html_from_json_file(key_name,file_path="scraped_data.json"):
        # Read the JSON file
            with open(file_path, 'r') as file:
                json_data = json.load(file)

            # Retrieve the HTML string from the JSON data
            html_code = json_data.get(key_name, '')
            messages=[
            {
                "role":"user",
                "content":f"Clean this html code and return only the elements need solve this test case:\n{query}\n\n so it would be easy for me to write selinium code to automate the testcase, kindly please help me. this is the link of the page {i} and \n the html {html_code}"
            }
        ]
            response = non_stream_get_response_openai_preview(messages=messages,max_tokens=4096,model="o1-mini",stream=False,temperature=0.8)
            # return html_code
            # Parse the HTML code
            # soup = BeautifulSoup(html_code, 'html.parser')
            return response
            # # Remove script and style elements
            # for script_or_style in soup(['script', 'style']):
            #     script_or_style.decompose()

            # # Define clickable elements
            # clickable_tags = ['a', 'button', 'input', 'select', 'form', 'textarea']

            # # Extract clickable elements with their class names and tags
            # clickable_elements = []
            # for tag in clickable_tags:
            #     elements = soup.find_all(tag)
            #     for element in elements:
            #         element_info = {
            #             'tag': element.name,
            #             'class': element.get('class', []),
            #             'id': element.get('id', ''),
            #             'name': element.get('name', ''),
            #             'type': element.get('type', ''),
            #             'value': element.get('value', ''),
            #             'href': element.get('href', ''),
            #             'text': element.get_text(strip=True)
            #         }
            #         clickable_elements.append(element_info)

            # return clickable_elements
        html_info={}
        for i in url_list:
            cleaned_text = clean_html_from_json_file(i)

            # Print the cleaned text
            print("\n\n",cleaned_text,"\n\n")
            st.write(cleaned_text["response"])
            html_info[i]=cleaned_text

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
        - Refer to the following for test-specific instructions: `{query}`

        7. **HTML Content**:
        - Utilize the following HTML content to extract exact element positions: `{html_info}`

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
        response = non_stream_get_response_openai_preview(messages=messages,max_tokens=4096,model="o1-preview",stream=False,temperature=0.8)
        # response = {'response': '```python\nfrom selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.common.keys import Keys\nimport time\n\n# Initialize the Chrome driver\ndriver = webdriver.Chrome()\n\n# Open the login page\ndriver.get("http://3.83.24.72:8000/")\n\n# Find the username and password fields and enter the credentials\nusername_field = driver.find_element(By.NAME, "username")\npassword_field = driver.find_element(By.NAME, "password")\n\nusername_field.send_keys("user")\npassword_field.send_keys("letuserpass")\n\n# Find the login button and click it\nlogin_button = driver.find_element(By.XPATH, "//button[@type=\'submit\']")\nlogin_button.click()\n\n# Wait for the page to load\ntime.sleep(3)\n\n# Navigate to the Attendance section\nattendance_link = driver.find_element(By.LINK_TEXT, "Attendance")\nattendance_link.click()\n\n# Wait for the page to load\ntime.sleep(3)\n\n# Test the Check-In feature\ncheck_in_button = driver.find_element(By.XPATH, "//button[contains(text(), \'Check-In\')]")\ncheck_in_button.click()\n\n# Wait for the action to complete\ntime.sleep(2)\n\n# Test the Check-Out feature\ncheck_out_button = driver.find_element(By.XPATH, "//button[contains(text(), \'Check-Out\')]")\ncheck_out_button.click()\n\n# Wait for the action to complete\ntime.sleep(2)\n\n# Close the browser\ndriver.quit()\n```'}
        # print(response)
        st.divider()
        st.subheader("Prepared Selenium Code")
        # st.code(response)
        import re
        import contextlib
        pattern = r'```(.*?)```'
        match = re.search(pattern, response["response"], re.DOTALL)

        if match:
            python_code = match.group(1).strip().replace("python", "")
            print("Extracted Python Code:")
            print(python_code)
            st.code(python_code)

            output_file_path = "execution_output.txt"

            # Redirect stdout and stderr to the output file
            output_capture = io.StringIO()
            error_capture = io.StringIO()
            with open(output_file_path, 'w') as output_file:
                with contextlib.redirect_stdout(output_file), contextlib.redirect_stderr(output_file):
                    # Execute the extracted Python code
                    exec(python_code)

            # Read and display the contents of the output file
            with open(output_file_path, 'r') as output_file:
                execution_output = output_file.read()

            st.divider()
            st.subheader("Execution result")
            st.text(execution_output)  # Display the output as plain text
            captured_output = output_capture.getvalue()
            captured_error = error_capture.getvalue()

            # Close the StringIO objects
            output_capture.close()
            error_capture.close()

            # Store the captured output and error in variables
            output_result = captured_output
            error_result = captured_error

            # Print the captured output and error
            st.write("Captured Output:")
            st.write(output_result)
            st.write("Captured Error:")
            st.write(error_result)
            st.write(f"Execution output saved to {output_file_path}")
        else:
            print("No Python code block found in the response.")

        # print(response)

        # python_code = response["response"]

        # # Remove the Markdown code block syntax
        # python_code = python_code.replace('```python', '').replace('```', '').strip()

        # # Print the extracted Python code
        # print("Extracted Python Code:")
        # print(python_code)

        # # Execute the extracted Python code
        # exec(python_code)

    except Exception as e:
        raise e