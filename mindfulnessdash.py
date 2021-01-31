def write():
    import streamlit as st
    #datetime is imported so that the user's [entry, date] pair can be saved
    from datetime import datetime
    import nltk as nltk
    import joblib
    import math as math
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    import pandas as pd
    sid = SentimentIntensityAnalyzer()
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
    from transformers import pipeline
    @st.cache(allow_output_mutation=True)
    def load_classifier():
        classifier = pipeline('sentiment-analysis')
        return classifier
    @st.cache(allow_output_mutation = True)
    def load_isear():
      isear = pd.read_csv("isear_embed.csv")
      isear = isear.drop("index", axis = 1)
      return isear
    
    @st.cache
    def analysis(sentence):
        model = load_my_model()
        lis = list()
        m = sid.polarity_scores(sentence)
        score = m['compound']
        a = re.split("[.!?;\n]", sentence)
        if len(a) > 2:
            b = a[len(a)-2]+ ". " +a[len(a)-1]
            c = sid.polarity_scores(b)
            score = c['compound']
        if len(a) > 3:
            b = a[len(a)-3] + ". " + a[len(a)-2] + ". " +a[len(a)-1]
            c = sid.polarity_scores(b)
            score2 = c['compound']
        else:
            score2 = 0
        EHS = pd.read_csv("EHS.csv")
        sentence_embeddings = EHS.values.tolist()
        OPTO = pd.read_csv("OPTO.csv")
        optimistic_embeddings = OPTO.values.tolist()
        #should check what happens when i do .values.tolist() a nd why i do it
        isear = load_isear()
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
        hugscore = 0
        classifier = load_classifier()
        if len(a) > 3:
          for i in range(0, len(a)):
            result = classifier(a[i])
            result = pd.DataFrame(result)
            if str(result["label"]).count("POS") > 0:
              hugscore = hugscore + result['score']
            if str(result["label"]).count("NEG") > 0:
              hugscore = hugscore - result['score']
        hugscore = hugscore / len(a)
        hugscore = float(hugscore)
        lis.append([rent, isear_feature, score, score2, hugscore])
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
            df.columns = ["rent", "isear_feature", "score", "score3", "hugscore"]
            loaded_model = joblib.load("GradientBoostedClassifier90CV.sav")
            result = loaded_model.predict(df)
            if result[0] == 0:
                score = "pessimistic"
                booleon = -3
            if result[0] == 1:
                score = "neutral"
                booleon = 0
            if result[0] == 2:
                score = "optimistic"
                booleon = 3
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
            if sentence.count(".") + sentence.count("!") + sentence.count("?") < 5:
                st.write("I'm not smart enough to analyze this without more sentences :(")
                st.markdown("![Alt Text](https://media1.tenor.com/images/cedbc086995947a3e2c239f13a3661b4/tenor.gif?itemid=11992490)")
            else:
                st.write("you're feeling : " + score)
                if score == "pessimistic":
                    st.write("That's fine. Let it all out.")
                    st.markdown("![Alt Text](https://media.tenor.com/images/ff4a60a02557236c910f864611271df2/tenor.gif)")
                    st.write("Check out the resources tab to see how you can 'learn' optimism")
                    st.markdown("[Click here if you need extra help](https://suicidepreventionlifeline.org/chat/)")
                if score == "neutral":
                    st.write("You're just chilling. Waiting on some stuff to play out. It be like that sometimes.")
                    st.markdown("![Alt Text](https://media1.tenor.com/images/0fbf51f99bccd97a825d11cb4487ce85/tenor.gif?itemid=11015213)")
                if score == "optimistic":
                    st.write("You are a ray of sunshine today! Keep it up!")
                    st.markdown("![Alt Text](https://media.tenor.com/images/2aa9b6f3a7d832c2ff1c1a406d5eae73/tenor.gif)")
    #st.header("Insert your username below to save your score")
    username = st.text_input("Username (required for you to save your score & see your day-to-day changes): ")
    today = datetime.now()
    #st.text_input doesn't work inside the st.button()....gotta figure out why
    if st.button('Save my score (press this twice if a new user)'):
        try:
            import csv
            fields= [result[0], sentence, today]
            with open(username + ".csv", 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
        except FileNotFoundError:
            scored = list()
            scored.append([result[0], sentence, today])
            score = pd.DataFrame(scored)
            score.to_csv(username + ".csv")
