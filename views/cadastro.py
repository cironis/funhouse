
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Define a custom function that will be triggered on search
def search_function(query):
    # Simulate search operation or custom logic
    st.write(f"Searching for: {query}")
    # Example: Return search results or perform some operation
    search_results = [f"Result {i}" for i in range(1, 6)]
    st.write("Search Results:")
    for result in search_results:
        st.write(result)

# Access the signature key from st.secrets
signature_key = st.secrets["credentials"]["signature_key"]

# Load credentials from the config.yaml file
with open('config/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    'the_cookie',           # Replace with your cookie name
    signature_key,         # Replace with your signature key
    cookie_expiry_days=30
)

# Login widget
name, authentication_status, username = authenticator.login('main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f'Welcome *{name}*')
    # Main application code
    st.title('Cadastrar Jogos')

    # Create a search box
    search_query = st.text_input("Enter your search query", "")

    # Create a button to trigger the search
    search_button = st.button("Search")

    # Trigger the search function when the button is clicked or Enter is pressed
    if search_button or search_query:
        if search_query:
            search_function(search_query)
        else:
            st.error("Please enter a search query.")


elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
