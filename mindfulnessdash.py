import streamlit as st
#datetime is imported so that the user's [entry, date] pair can be saved
from datetime import datetime
import math as math
import pandas as pd
from openai import OpenAI

openai_key = st.secrets["openai"]


def write():    
    
    def analysis(sentence):
       
        hugscore = 0
        classifier = pipeline('sentiment-analysis')
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
            client = OpenAI(api_key = openai_key)
            
            # Create a chat completion using the new interface
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Specify the model you wish to use
                messages=[
                    {"role": "system", "content": "You are an autonomous agent."},
                    {
                        "role": "user",
                        "content": (
                            "Based on 'Learned Optimism' by Martin Seligman, classify the following journal entry as either "
                            "pessimistic, optimistic, or neutral. Return only a single number: 0 for pessimistic, 1 for neutral, "
                            "and 2 for optimistic.\n\n"
                            f"Journal Entry: {sentence}"
                        )
                    }
                ],
                max_tokens=1  # Expecting a single number as output
            )
            result = int(response.choices[0].message.content.strip())

            if result == 0:
                score = "pessimistic"
                booleon = -3
            if result == 1:
                score = "neutral"
                booleon = 0
            if result == 2:
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
            elif sentence.count("..") + sentence.count("!!") > 2:
                st.write("I can't analyze entries right now that have abnormal punctuation. Feel free to change your punctuation and try again.")
                st.markdown("![Alt Text](https://media1.tenor.com/images/59f338103063f0c10ee1163d48b4dd14/tenor.gif?itemid=17312786)")
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
    today = datetime.now().strftime("%Y-%m-%d")
    #st.text_input doesn't work inside the st.button()....gotta figure out why
    #^above is an old note, i know why now, I just keep it there to remind me that inside button actions are way diff than outside button actions
    if st.button('Save my score'):
        fields= [score, sentence, today]
        import pymysql
        st.write(st.secrets["pymysql"])
        connection = pymysql.connect(
            **st.secrets["pymysql"]
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (score INT, username VARCHAR(255), date DATE);
            """)
            connection.commit()
            query = f"INSERT INTO users (score, username, date) VALUES ('{score}', '{username}', '{today}')"
            cursor.execute(query)

        print("Table created successfully!")
        


        
        '''
        connection = st.connection(

            "sql" # Secrets must include host, port, database, user, password
        )

        '''
        st.success("Data inserted successfully!")

        connection.close()


