def write():
    import streamlit as st
    import matplotlib.pyplot as plt
    import pandas as pd
    import wordcloud
    #write is smart...it stops you from loading the whole page when you import

    username = st.text_input("Enter username here:")

    audio_file = open('songonthebeach.ogg', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    df = pd.read_csv("rastaman.csv")
    df = pd.DataFrame(df)
    #str = random.choice(quote_list)
    #st.write(str)
    df = df.dropna()
    df = df.dropna()
    df.columns = ["score", "date"]
    score = df["score"]

    recent = score[len(score)-1]

    if recent >= 5:
        st.write("You're doing well today. I hope you keep up the progress.")
    if recent < 5 and recent > 3:
        st.write("You're not feeling so great today, and that's okay. Know I'll always care about you.")
    if recent <= 3:
        st.write("Days like these come, and it's perfectly fine to be upset when difficulties arise. What you should remember is that days like these pass too, and that even when these times are dark, you still have friends, family, external resources to reach out too. Check out the resources tab for ways you can improve now.")

    #code where if the last five have been super happy play Photograph


    col1, col2, col3 = st.beta_columns(3)
    with col1:
        df = df.dropna()
        df.columns = ["score", "date"]
        #df["date"] = pd.to_datetime(df["date"])
        fig, ax = plt.subplots()
        right_side = ax.spines["right"]
        right_side.set_visible(False)
        top_side = ax.spines["top"]
        top_side.set_visible(False)
        ax.plot(df["date"], df["score"], 'o')
        st.pyplot(fig)

    with col2:
        LJE = pd.read_csv("Labelled_Journal_Entries.csv")
        #LJE = LJE[LJE["score"] < 4]
        from wordcloud import WordCloud
        wordcloud2 = WordCloud(background_color='white').generate(' '.join(LJE['entry']))
        fig, ax = plt.subplots()
        plt.imshow(wordcloud2)
        plt.axis("off")
        st.pyplot(fig)
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
