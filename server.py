from flask import Flask, request, jsonify
import speech_recognition as s_r
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import yake
import os

app = Flask(__name__)

@app.route('/')

@app.route('/customer_query', methods=["POST"])
def Customer_Query():
    r = s_r.Recognizer()
    #my_mic = s_r.Microphone(device_index=1) #my device index is 1, you have to put your device index
    audio_file = request.files["file"]
    try:
        with s_r.AudioFile(audio_file) as source:
            print("Say now!!!!")
            r.adjust_for_ambient_noise(source) #reduce noise
            audio = r.listen(source) #take voice input from the microphone
        text = r.recognize_google(audio)
        print(text)
        sentiment =""
        Sentence=[str(text)]
        analyser=SentimentIntensityAnalyzer()
        for i in Sentence:
            v=analyser.polarity_scores(i)
            print(v['compound'])
            if v['compound'] < -0.05:
                sentiment = "Negative"
            elif v['compound'] > 0.05:
                sentiment = "Positive"
            else:
                sentiment ="Neutral"
    except:
        print("Couldn't recognise speech")
    result =""
    try:
        kw_extractor = yake.KeywordExtractor()
        keywords = kw_extractor.extract_keywords(text)
        ke_list = []
        for kw in keywords:
            ke_list.append(kw[0])

        

    
        use_case = ""
        usecase_1 = ["lost","stolen","steal","recovery","fraud","unable","block","not being able",] #card blocking
        usecase_2 = ["credit card","new","card","debit card"] #new card purchase
        usecase_3 = ["information","policy","question","offers"]#information desk
        usecase_4 = ["raising","limit","raise"]#update limit
        usecase_5 = ["loan","home loan","personal loan","mortgage","car loan","bike loan","vehicle loan","gold loan","student loan","education loan"]#loan application
        usecase_6 = ["SIP","systematic investment plan","mutual funds"]#fund management
        usecase_7 = ["demat account","stocks","equity","long term equity plans","stock","stocks advice","fixed deposits","fd","demat"]#capital market
        usecase_8 = ["passbook","transaction history","transactions"]#passbook and transaction 
        usecase_9 = ["insurance","health insurance","life insurance","car insurance","family insurance","medical insurance"]#insurance management
        usecase_10 = ["feedback","complaint","bad service","customer experience","bad","behaviour","lazy","unorganized","complain","unprofessional"]#customer feedback


        if any(word in ke_list for word in usecase_2):
            use_case = "New card purchase"
        elif any(word in ke_list for word in usecase_1):
            use_case = "Card block"
        elif any(word in ke_list for word in usecase_3):
            use_case = "Information desk"
        elif any(word in ke_list for word in usecase_5):
            use_case = "Loan application"
        elif any(word in ke_list for word in usecase_6):
            use_case = "Fund management"
        elif any(word in ke_list for word in usecase_7):
            use_case = "Capital market"
        elif any(word in ke_list for word in usecase_8):
            use_case = "Passbook and transaction "
        elif any(word in ke_list for word in usecase_9):
            use_case = "Insurance management"
        elif any(word in ke_list for word in usecase_10):
            use_case = "Customer feedback"
        elif any(word in ke_list for word in usecase_4):
            use_case = "Update limit"
        else:
            use_case = "None"
        
        result = {"sentiment": sentiment, "usecase":use_case}
    except UnboundLocalError as e:
        print("Please be more specific")
    return jsonify(result)

if __name__ == '__main__':
    app.debug =True
    app.run(host = '0.0.0.0', port = 5000)