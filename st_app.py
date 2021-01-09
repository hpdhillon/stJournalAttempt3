import streamlit as st

import awesome_streamlit as ast
import UserProfile
import mindfulnessdash

ast.core.services.other.set_logging_format()

PAGES = {
    "Home": mindfulnessdash,
    "Resources": UserProfile,
}


def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.title("Contribute")
    st.sidebar.info(
        "This an open source project and you are very welcome to **contribute** your awesome "
        "comments, questions, resources and apps to me @ harpal.dhillon@rutgers.edu"
    )
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is maintained by Marc Skov Madsen. You can learn more about me on 
        [linkedin](https://www.linkedin.com/in/harpal-dhillon-056016158/)
"""
    )


if __name__ == "__main__":
    main()
