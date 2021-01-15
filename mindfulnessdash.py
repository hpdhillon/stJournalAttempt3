def write():
    import streamlit as st
    #datetime is imported so that the user's [entry, date] pair can be saved
    from datetime import datetime
    import nltk as nltk
    #I think math is imported to compute ceiling of polarization heuristic. Will delete that and this import soon. 
    import math as math
    #Think I'll remove this tokenizer
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    import pandas as pd
    sid = SentimentIntensityAnalyzer()
    #Might have to remove the following three lines too. A lot will be deleted unless I find some ML use case for it.
    import scipy
    import torch
    #import sklearn
    from scipy import spatial
    from sentence_transformers import SentenceTransformer
    @st.cache(allow_output_mutation=True)
    def load_my_model():
        model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        return model
    #As mentioned before, this should be deleted soon
    #Gotta revise this ML code. Need to upload the saved GradientBoostedClassifier.
    @st.cache
    def analysis(sentence):
        m = sid.polarity_scores(sentence)
        score = m['compound']
        a = sentence.split('.')
        a = a[:len(a)-1]
        if len(a) > 2:
            b = a[len(a)-2]+a[len(a)-1]
            c = sid.polarity_scores(b)
            score = c['compound']
        d = polarization_heuristic(sentence)
        EHS = pd.read_csv("EHS.csv")
        sentence_embeddings = EHS.values.tolist()
        OPTO = pd.read_csv("OPTO.csv")
        optimistic_embeddings = OPTO.values.tolist()
        model = load_my_model()
        booleon = 0
        a_embeddings = model.encode(a)
        for j in range(len(a_embeddings)):
            for i in range(len(sentence_embeddings)):
                result = 1 - spatial.distance.cosine(sentence_embeddings[i], a_embeddings[j])
                if result > .8:
                    booleon = booleon - 1
                    #print(a[j])
                    #st.write('You sound helpless, this sentence concerned me:', a[j])
                    break
        if booleon > 0:
            for j in range(len(a_embeddings)):
                for i in range(len(optimistic_embeddings)):
                    result = 1 - spatial.distance.cosine(optimistic_embeddings[i], a_embeddings[j])
                    if result > .8:
                        booleon = booleon + 1
                        break
        rent = (booleon/len(a_embeddings))
        score = 5.1359 * rent + 1.385 * score + 4.5783
        return score, booleon

    sentence = st.text_area("what's on your mind?")
    #button = st.button()
    #the reason score is compute here and not inside st.button("analysis") is because now it'll be saved rather than refreshed if another button gets pressed
    #basically, variables inside a button aren't available outside of them.
    if len(sentence) > 1:
        if sentence.count(".") == 0:
            st.write("Write more!")
        else:
            score, booleon = analysis(sentence)
            try:
                lis.append([score, booleon])
            except:
                lis = list()
                lis.append([score, booleon])
    #need to revise output. Output should be a page of resources with a gif on top.
    if st.button('Analysis'):
        if len(sentence) > 1:
            if sentence.count(".") + sentence.count("!") + sentence.count("?") == 0:
                st.write("Write more!")
        st.write('your score is:', score)
        if booleon <  -2:
            st.write("You sound sad. That's fine. Let it all out.")
            st.markdown("![Alt Text](https://media.tenor.com/images/ff4a60a02557236c910f864611271df2/tenor.gif)")
            st.markdown("[Click here if you need extra help](https://suicidepreventionlifeline.org/chat/)")
        if booleon > 2:
            st.write("You are a ray of sunshine today! Keep it up playa!")
            st.markdown("![Alt Text](https://media.tenor.com/images/2aa9b6f3a7d832c2ff1c1a406d5eae73/tenor.gif)")
    #st.header("Insert your username below to save your score")
    username = st.text_input("Username (required for you to save your score & see your day-to-day changes): ")
    today = datetime.now()
    #st.text_input doesn't work inside the st.button()....gotta figure out why
    if st.button('Save my score'):
        try:
            import csv
            fields= [score, today]
            with open(username + ".csv", 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
        except FileNotFoundError:
            scored = list()
            scored.append([score, today])
            score = pd.DataFrame(scored)
            score.to_csv(username + ".csv")
