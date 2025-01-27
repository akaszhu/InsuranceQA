import streamlit as st
from url import get_all_routes
from scrap import scrape_pages
from capture import take_screenshots

# Initialize session state variables
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
if "extracted_text" not in st.session_state:
    st.session_state["extracted_text"] = True  # Default value
if "scrap_url" not in st.session_state:
    st.session_state["scrap_url"] = ""
if "scrap_image" not in st.session_state:
    st.session_state["scrap_image"] = ""
if "bt2_clicked" not in st.session_state:
    st.session_state["bt2_clicked"] = False

if "bt3_clicked" not in st.session_state:
    st.session_state["bt3_clicked"] = False

st.subheader("This QA tools will help you to cut-short and help you filing the report🛫")
st.write("Enter Website Credential Details")

# Form for entering API details
if st.session_state["base_url"] == "":
    with st.form(key="api_details_form"):
        base_url = st.text_input("Base URL", "")
        login_url = st.text_input("Login URL", "")
        username = st.text_input("Username", "user")
        password = st.text_input("Password", type="password")

        submit_button = st.form_submit_button(label="Submit")

        # Save form data to session state
        if submit_button:
            st.session_state["base_url"] = base_url
            st.session_state["login_url"] = login_url
            st.session_state["username"] = username
            st.session_state["password"] = password
            st.success("API details have been saved to session state.")

# Display session state details
if st.session_state["base_url"] != "":
    st.write("Session State Details:")
    st.write(f"Base URL: {st.session_state['base_url']}")
    st.write(f"Login URL: {st.session_state['login_url']}")
    st.write(f"Username: {st.session_state['username']}")
    st.write(f"Password: {st.session_state['password']}")

    # Buttons for actions
    bt1 = st.button("Extract URLs")
    bt2 = st.button("Extract HTML")
    bt3 = st.button("Get Webpage Image")

    # Button 1: Extract URLs
    if bt1:
        with st.spinner("Fetching all the routes..."):
            with st.expander("List of all the routes in the given test link"):
                if not st.session_state["scrapped_url"]:
                    # st.write((
                    #     st.session_state["base_url"],
                    #     st.session_state["login_url"],
                    #     st.session_state["username"],
                    #     st.session_state["password"],
                    # ))
                    urls = get_all_routes(
                        st.session_state["base_url"],
                        st.session_state["login_url"],
                        st.session_state["username"],
                        st.session_state["password"],
                    )
                    st.session_state["scrapped_url"] = urls
                    st.write(urls)
                else:
                    st.write(st.session_state["scrapped_url"])

    # Button 2: Extract HTML
    if bt2 or st.session_state["bt2_clicked"]:
        st.session_state["bt2_clicked"] = True  # Set flag
        with st.form(key="scrap_code"):
            scrap_url = st.text_input(
                "URL you want to scrape", value=st.session_state["scrap_url"]
            )
            submit_button_1 = st.form_submit_button(label="Submit")

            if submit_button_1:
                st.session_state["scrap_url"] = scrap_url  # Save input in session state
                with st.spinner("Scraping the HTML code..."):
                    scraped_data = scrape_pages(
                        st.session_state["base_url"],
                        st.session_state["login_url"],
                        st.session_state["username"],
                        st.session_state["password"],
                        [scrap_url],
                    )
                    st.session_state["scraped_data"] = scraped_data  # Store result
    # Display the scraped HTML after submission
    if "scraped_data" in st.session_state:
        st.subheader("Scraped HTML")
        st.code(st.session_state["scraped_data"])

# Button 3: Get Webpage Image
    if bt3 or st.session_state["bt3_clicked"]:
        st.session_state["bt3_clicked"] = True  # Set flag
        with st.form(key="scrap_image"):
            scrap_image = st.text_input(
                "URL to capture webpage image", value=st.session_state["scrap_image"]
            )
            submit_button_2 = st.form_submit_button(label="Submit")

            if submit_button_2:
                # st.session_state["scrap_image"] = scrap_image  # Save input in session state
                with st.spinner("Capturing the webpage image..."):
                    take_screenshots(
                        st.session_state["base_url"],
                        st.session_state["login_url"],
                        st.session_state["username"],
                        st.session_state["password"],
                        [scrap_image],
                    )
                    st.session_state["image_captured"] = True
        # Display confirmation after capturing image
        # if st.session_state.get("image_captured"):
        #     st.success(f"Image captured for {st.session_state['scrap_image']}")

    # Button to reset session state
    clear_bt = st.button("Test New Webpage")
    if clear_bt:
        st.session_state["bt2_clicked"] = False
        st.session_state["bt3_clicked"] = False
        st.session_state["scrapped_url"] = ""
        st.session_state["scrap_url"] = ""
        st.session_state["scrap_image"] = ""
        st.session_state["scraped_data"] = None
        st.session_state["image_captured"] = False
# Warning if BRD is not uploaded
if not st.session_state["extracted_text"]:
    st.warning("You have to upload BRD on the home page.")
