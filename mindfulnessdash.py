def write():
    import streamlit as st
    #datetime is imported so that the user's [entry, date] pair can be saved
    from datetime import datetime
    import nltk as nltk
    import joblib
    #I think math is imported to compute ceiling of polarization heuristic. Will delete that and this import soon. 
    import math as math
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    import pandas as pd
    sid = SentimentIntensityAnalyzer()
    #Might have to remove the following three lines too. A lot will be deleted unless I find some ML use case for it.
    import scipy
    import torch
    import re
    #import sklearn
    from scipy import spatial
    from sentence_transformers import SentenceTransformer
    @st.cache(allow_output_mutation=True)
    def load_my_model():
        model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        return model
    #As mentioned before, this should be deleted soon
    #Gotta revise this ML code. Need to upload the saved GradientBoostedClassifier.
    #Even this code is not optimized. We should have 75-85 percent accuracy but: a) 10-15 percent of the training data has incorrect sentiment scores, b) I just picked the first
    #model that got to 85 percent accuracy, the model can be improved by having a higher cutoff and doing cross validation and grid search to find the most optimal hyperparameters
    @st.cache
    def analysis(sentence):
        model = load_my_model()
        lis = list()
        m = sid.polarity_scores(sentence)
        score = m['compound']
        a = re.split("[.!?;\n]", sentence)
        if len(a) > 2:
            b = a[len(a)-2]+". " +a[len(a)-1]
            c = sid.polarity_scores(b)
            score = c['compound']
        if len(a) > 3:
            b = a[len(a)-3] + a[len(a)-2] +"."+a[len(a)-1]
            c = sid.polarity_scores(b)
            score2 = c['compound']
        else:
            score2 = 0
        EHS = pd.read_csv("EHS.csv")
        sentence_embeddings = EHS.values.tolist()
        OPTO = pd.read_csv("OPTO.csv")
        optimistic_embeddings = OPTO.values.tolist()
        #should check what happens when i do .values.tolist() a nd why i do it
        isear = pd.read_csv("isear_embed.csv")
        isear = isear.drop("index", axis = 1)
        isear_list = isear.values.tolist()
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
        for j in range(len(a_embeddings)):
            for i in range(len(optimistic_embeddings)):
              result = 1 - spatial.distance.cosine(optimistic_embeddings[i], a_embeddings[j])
              if result > .8:
                  booleon = booleon + 1
                  break
        rent = (booleon/len(a_embeddings))
        isear_feature = 0
        for j in range(len(a_embeddings)):
            for i in range(len(isear_list)):
                result = 1 - spatial.distance.cosine(isear_list[i], a_embeddings[j])
                if result >= .8:
                  isear_feature = isear_feature - 1
                  break

        lis.append([rent, isear_feature, score, score2])
        return lis    

    sentence = st.text_area("what's on your mind?")
    #button = st.button()
    #the reason score is compute here and not inside st.button("analysis") is because now it'll be saved rather than refreshed if another button gets pressed
    #basically, variables inside a button aren't available outside of them.
    #need to append more than that to the list to get meaningful data out of this.
    if len(sentence) > 1:
        if sentence.count(".") == 0:
            st.write("Write more!")
        else:
            df = analysis(sentence)
            df = pd.DataFrame(df)
            df.columns = ["rent", "isear_feature", "score", "score3"]
            loaded_model = joblib.load("GradientBoostedClassifier85_7.sav")
            result = loaded_model.predict(df)
            if result[0] == 0:
                score = "pessimistic"
            if result[0] == 1:
                score = "neutral"
            if result[0] == 2:
                score = "optimistic"
            #try:
            #    lis.append([df[0]])
            #except:
            #    lis = list()
            #    lis.append([df[0]])
    #need to revise output. Output should be a page of resources with a gif on top.
    if st.button('Analysis'):
        #gonna change this to if sentence.count(x) + count(y) .... < 5, then ask them to write more.
        #the model does poorly on samples less than 5 sentences
        if len(sentence) > 1:
            if sentence.count(".") + sentence.count("!") + sentence.count("?") == 0:
                st.write("Write more!")
            else:
                st.write("you're feeling :" + score)
                #if booleon <  -2:
                #    st.write("You sound sad. That's fine. Let it all out.")
                #    st.markdown("![Alt Text](https://media.tenor.com/images/ff4a60a02557236c910f864611271df2/tenor.gif)")
                #    st.markdown("[Click here if you need extra help](https://suicidepreventionlifeline.org/chat/)")
                #if booleon > 2:
                #    st.write("You are a ray of sunshine today! Keep it up playa!")
                #    st.markdown("![Alt Text](https://media.tenor.com/images/2aa9b6f3a7d832c2ff1c1a406d5eae73/tenor.gif)")
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
