import streamlit as st
#*need to add FAQ answers on sidebar*
import awesome_streamlit as ast
import UserProfile
import mindfulnessdash
import Resources
ast.core.services.other.set_logging_format()

PAGES = {
    "Home": mindfulnessdash,
    "User Profile": UserProfile,
    "Resources" : Resources
}


def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.title("FAQ")
    st.sidebar.info(
        "The app requires proper punctuation to work, multiple punctuation marks like '!!' or '...' muddy feature generation. A patch to fix this is being worked on.  \n"
        "The model requires at least 5 sentences to be accurate. Current LOOCV test accuracy is 95 percent, so that means it's possible for it to mess up sometimes!  \n"
        "Reporting mistakes greatly helps me predict better in the future. I do not have access to any user data, so if you'd like to help me, please fill out the google form linked on the resources page with your journal entry and what you feel the model should have output.  \n"
        "UserProfile is best viewed in wide mode. Select the toolbar in the upper right and then settings to switch to wide mode."
    )
    st.sidebar.title("Credits")
    st.sidebar.info(
        "A big thanks to:  \n"
        "Marc Skov Madsen for creating awesome_streamlit, the library that allowed me to easily create this nav bar  \n"
        "Kevin Northover for introducing me to streamlit  \n" 
        "UKPLab for creating sentence-bert, Stanford for the open pessimist/optimist tweet data, the isear dataset curators and google's colab creators for giving me the platform I needed to generate the complex features and model"
    )


    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is maintained by Harpal Dhillon. You can learn more about me on
        [linkedin](https://www.linkedin.com/in/harpal-dhillon-056016158/)
"""
    )


if __name__ == "__main__":
    main()
