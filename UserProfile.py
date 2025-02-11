def write():
    #write is smart...it stops you from loading the every page when you import
    #^Above notes are just my musings
    import streamlit as st
    import matplotlib.pyplot as plt
    import pandas as pd
    import wordcloud
    import seaborn as sea

    username = st.text_input("Enter username here:")
    #plays song on the beach
    #eventually I should let this personalize
    boolean = False
    if len(username) > 0:
        try:
            import pymysql
            connection = pymysql.connect(
                **st.secrets["pymysql"]
            )
    
            with connection.cursor() as cursor:
                query = 'SELECT * FROM users WHERE username = %s'
                cursor.execute(query, (username, ))
                result = cursor.fetchone()
            if result:
                st.write("user exists")
                boolean = True
            else:
                st.write("username doesn't exist! 1")
        except:
            st.write("username doesn't exist!")
    if boolean:
        audio_file = open('songonthebeach.ogg', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/ogg')
        #this reads our rastaman, example user csv
        df = pd.DataFrame(result)
        print(df)
        #str = random.choice(quote_list)
        #st.write(str)
        df = df.dropna()
        df.columns = ["score", "sentence", "date"]
        score = df["score"]
        #recent = the most recent score
        try:
            recent = score[len(score)-1]
            if recent == 0:
                st.write("Days like these come, and it's perfectly fine to be upset when difficulties arise. What you should remember is that days like these pass too, and that even when these times are dark, you still have friends, family, external resources to reach out too. Check out the resources tab for ways you can improve now.") 
        except:
            st.write("Your username exists but we didn't save your score. Sorry about that! Please insert your journal entry again and press save my score again to save it officially. This is a known bug thart occurs when a username is first created, but not after!")
        #below are placeholders for personalized notes. should add functionality for this l8r
        #if recent == 2:
        #    st.write("You're doing well today. I hope you keep up the progress.")
        #if recent == 1:
        #    st.write("You're not feeling so great today, and that's okay. Know I'll always care about you.")
        

        #code where if the last five have been super happy play Photograph


        col1, col2, col3 = st.beta_columns(3)

        #need to make this graph look better. should add a time slider too. would be cool if when a person hovers over a point they see the journal entry for it.
        with col1:
            #df["date"] = pd.to_datetime(df["date"])
            fig, ax = plt.subplots()
            df2 = df[["score", "date"]]
            df2["date"] = pd.to_datetime(df2["date"])
            df2['week_num'] = df2['date'].dt.strftime("%W")
            df2['day_num'] = df2['date'].dt.weekday
            df_wide = df2.pivot_table(index='week_num',columns='day_num',values='score')
            ax = sea.heatmap(df_wide)
            st.pyplot(fig)
        #have to take down this labelled_journal_entries csv before we release. If not, we release a lot of people's personal data.
        #need to add a slider for time here. maybe for mood too.
        with col2:
            #LJE = LJE[LJE["score"] < 4]
            from wordcloud import WordCloud
            wordcloud2 = WordCloud(background_color='white').generate(' '.join(df['sentence']))
            fig, ax = plt.subplots()
            plt.imshow(wordcloud2)
            plt.axis("off")
            st.pyplot(fig)
        #need to add sentiment-dependent emojis to output searches
        with col3:
            word = st.text_input("Input word you want to search for")
            if len(word) > 2:
                entries = ' '.join(df['sentence'])
                arr = entries.split('.')
                str = " "
                for i in range(0, len(arr)):
                    if word in arr[i]:
                        str = arr[i]
                        st.markdown(str)
            #else:
                #st.write("your input is too short!")
