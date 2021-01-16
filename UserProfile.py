def write():
    #a possible segway from all of this would be to give people their data and say, go to this Tableau dashboard, input your data and see your personalized User Profile! 
    #might take too much work tho
    #write is smart...it stops you from loading the every page when you import
    #^Above notes are just my musings
    import streamlit as st
    import matplotlib.pyplot as plt
    import pandas as pd
    import wordcloud

    username = st.text_input("Enter username here:")
    #plays song on the beach
    #eventually we should let this personalize
    audio_file = open('songonthebeach.ogg', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')
    #this reads our rastaman, example user csv
    df = pd.read_csv("rastaman.csv")
    df = pd.DataFrame(df)
    #str = random.choice(quote_list)
    #st.write(str)
    df = df.dropna()
    df.columns = ["score", "date"]
    score = df["score"]
    #recent = the most recent score
    recent = score[len(score)-1]
    #below are placeholders for personalized notes. should add functionality for this l8r
    if recent >= 5:
        st.write("You're doing well today. I hope you keep up the progress.")
    if recent < 5 and recent > 3:
        st.write("You're not feeling so great today, and that's okay. Know I'll always care about you.")
    if recent <= 3:
        st.write("Days like these come, and it's perfectly fine to be upset when difficulties arise. What you should remember is that days like these pass too, and that even when these times are dark, you still have friends, family, external resources to reach out too. Check out the resources tab for ways you can improve now.")

    #code where if the last five have been super happy play Photograph


    col1, col2, col3 = st.beta_columns(3)
    
    #need to make this graph look better. should add a time slider too. would be cool if when a person hovers over a point they see the journal entry for it.
    with col1:
        #df["date"] = pd.to_datetime(df["date"])
        fig, ax = plt.subplots()
        right_side = ax.spines["right"]
        right_side.set_visible(False)
        top_side = ax.spines["top"]
        top_side.set_visible(False)
        ax.plot(df["date"], df["score"], 'o')
        st.pyplot(fig)
    #have to take down this labelled_journal_entries csv before we release. If not, we release a lot of people's personal data.
    #need to add a slider for time here. maybe for mood too.
    with col2:
        LJE = pd.read_csv("Labelled_Journal_Entries.csv")
        #LJE = LJE[LJE["score"] < 4]
        from wordcloud import WordCloud
        wordcloud2 = WordCloud(background_color='white').generate(' '.join(LJE['entry']))
        fig, ax = plt.subplots()
        plt.imshow(wordcloud2)
        plt.axis("off")
        st.pyplot(fig)
    #need to add sentiment-dependent emojis to output searches
    with col3:
        LJE = pd.read_csv("Labelled_Journal_Entries.csv")
        word = st.text_input("Input word you want to search for")
        if len(word) > 2:
            entries = ' '.join(LJE['entry'])
            arr = entries.split('.')
            str = " "
            for i in range(0, len(arr)):
                if word in arr[i]:
                    str = arr[i]
                    st.markdown(str)
        #else:
            #st.write("your input is too short!")
