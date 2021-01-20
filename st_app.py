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
        "The model requires at least 5 sentences to be accurate. Current accuracy is 86 percent, so that means it's possible for it to mess up sometimes!"
        " Reporting mistakes greatly helps me predict better in the future. As of right now, I do not have access to any user data (I'd have to guess your usernames for that)."
        " So if you'd like to help me, please fill out the google form linked on the resources page with your journal entry and what you feel the model should have output. Thank you!"
    )
    st.sidebar.title("Credits")
    st.sidebar.info(
        "Thank you to Marc Skov Madsen for creating awesome_streamlit, the library that allowed us to easily create this nav bar\nThank you to Kevin Northover for introducing me to streamlit, last year at a New Jersey Data Science Meetup\nThank you to UKPLab for creating sentence-bert, Stanford for the open pessimist/optimist tweet data, the isear dataset curators and google's colab creators for giving us the platform we needed to generate our complex features and model"
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
