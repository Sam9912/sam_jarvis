import pyttsx3
import os
import json
import time
import wolframalpha
from urllib.request import urlopen
import pyautogui
import datetime
import wikipedia
import webbrowser
import speech_recognition as sr
import smtplib
import psutil
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak("the current time is: ")
    speak(time)
def date_():
    year=datetime.datetime.now().year
    month=datetime.datetime.now().month
    date= datetime.datetime.now().day
    speak("the current date is:")
    speak(date)
    speak(month)
    speak(year)
def cpu():
    usage=str(psutil.cpu_percent())
    speak('CPU usage is'+usage+'percent')
    battery_info=psutil.sensors_battery()
    speak(f'Battery percentage is {battery_info} ')

def wishme():
    """"""
    hours=int(datetime.datetime.now().hour)
    if hours >=0 and hours<=12:
        speak("Good Morning Sam")
        time_()
        date_()
    elif hours >= 12 and hours <18:
        speak("Good Afternoon Sam")
        time_()
        date_()
    elif  hours >=18 and hours<=24:
        speak("Good Evening Sam")
        time_()
        date_()

    speak("i am Jarvis! your personal AI Assistant. How may i help you?")
def takeuserinput():
    '''this function is to take user input  through microphone'''
    r=sr.Recognizer()
    with sr.Microphone(device_index=1) as source:

        print('listening...')

        r.adjust_for_ambient_noise(source)
        audio=r.listen(source)
        # r.energy_threshold = 50
        r.pause_threshold = 1
    try:
        print('Recognizing...')
        query=r.recognize_google(audio,language='en-IN')
        print(f"user said: {query} \n")
    except Exception as e:
        print(e)
        print("Pardon! Say that Again Please")
        return 'None'
    return query
def sendemail(to,content):
    """ fuction for sending email using smtplib"""
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('username@gmail.com','abc123')
    server.sendmail('username@gmail.com',to,content)
    server.close()

def notes():
    speak('what do u want to note down?')
    f=open('notes.txt','a')
    unote = takeuserinput()
    speak('do you want to write date and time?')
    rep=takeuserinput()
    if 'yes' in rep or 'sure' in rep:
        strtime= datetime.datetime.now().strftime("%H:%M:%S")
        f.write(f'\n {strtime}')
        f.write(':- ')
        f.write(unote)
        speak('noted with date and time')
        f.close()
    elif 'no' in rep:
        f.write(unote)
        speak('noted without date and time')
        f.close()
def shownote():
    try:
        f = open('notes.txt', 'r')
        data=f.read()
        print(data)
        speak(data)

    except Exception as e:
       speak('no note exists')
       print(e)

def removenote():
    if os.path.exists('notes.txt'):
        os.remove('notes.txt')
        speak('notes removed sucessfully')
    else:
        speak('no notes exist')
def takescreenshot():
    ss=pyautogui.screenshot()
    ss.save('C:/Users/DELL/Desktop/sam/python/jarvis/screenshots/ss.png')
def remember():
    speak('what should i remember ?')
    cmd=takeuserinput()
    speak('you asked me to remember that'+cmd)
    rem=open('remember.txt','w')
    rem.write(cmd)
    rem.close()

def news():
    try:
        jsonobj=urlopen("http://newsapi.org/v2/top-headlines?country=us&category=general&apiKey=37b44802b2f34795b72d95bc94ffefd9")
        data=json.load(jsonobj)
        i=1
        speak('here are some top headlines ')
        print("=========TOP HEADLINES========="+ '\n')
        for items in data['articles']:
            print(str(i)+'.' + items['title'] + '\n')
            print(items['description']+'\n')
            speak(items['title'])
            i+=1
    except Exception as e:
        print(e)

def showremember():
    if os.path.exists('remember.txt'):
        remb=open('remember.txt','r')
        speak('you asked me to remember that: '+remb.read())
        remb.close()
    else:
        speak('there is nothing to remember')
if __name__ == '__main__':

    # for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    wishme()
    # speak(takeuserinput())
    while True:
        query=takeuserinput().lower()
        if 'wikipedia' in query:
            speak('searching wikipedia...')
            query=query.replace('wikipedia','')
            result=wikipedia.summary(query,sentences='2')
            speak('According to Wikipedia')
            print(result)
            speak(result)

        elif 'open youtube' in query:
            # speak('opening youtube...')
            # webbrowser.open("www.youtube.com")
            speak('what should i search?')
            # response=takeuserinput()
            # # engine.runAndWait()
            # if 'yes' in response:
            #     speak('what should i search')
            search=takeuserinput().lower()
            # search.replace(' ','')
            webbrowser.open(f'https://www.youtube.com/results?search_query={search}')
            # elif 'no' in response:
            #     continue
        elif 'open google' in query:
            # speak('opening google...')
            speak('what should i search?')
            search = takeuserinput().lower()
            speak('searching google...')
            webbrowser.open("https://www.google.com/search?q="+search)
        elif 'open stack overflow' in query:
            speak('opening stackoverflow...')
            webbrowser.open("www.stackoverflow.com")
        elif 'open facebook' in query:
            speak('opening facebook...')
            webbrowser.open("www.facebook.com")
        elif 'send email' in query:
            try:
                speak('what should i say')
                content=takeuserinput()
                print(content)
                speak('whom should i send')
                reciever= input('enter recivers email here: ')
                to=reciever
                sendemail(to,content)
                speak('email has been sent sucessfully')

            except Exception as e:
                print(e)
                speak('unable to send email')
        elif 'time'  in query:
            time_()
        elif 'date' in query:
            date_()

        elif 'cpu info' in query:
            cpu()
        elif 'ms word' in query:
            speak("opening MS word...")
            ms_word=r'C:\Program Files\Microsoft Office\Office16\WINWORD.EXE'
            os.startfile(ms_word)

        elif 'take note' in query:
            notes()
        elif 'show note' in query:
            shownote()
        elif 'screenshot' in query:
            takescreenshot()
        elif 'remove notes' in query:
            removenote()
        elif 'remember that' in query:
            remember()
        elif 'do you remember anything' in query:
            showremember()
        elif 'news' in query:
            news()
        elif 'where is' in query:
            query=query.replace('where is','')
            location=query
            speak('user asked for location'+location)
            webbrowser.open_new_tab('https://www.google.com/maps/place/'+location)
        elif 'calculate' in query:
           try:
                client=wolframalpha.Client('R6KQ9T-5E69ELVQGJ')
                index=query.lower().split().index('calculate')
                query=query.split()[index+1:]
                res=client.query(''.join(query))
                answer=next(res.results).text
                print('The Answer is: '+answer)
                speak('The Answer is: '+answer)
           except Exception as e:
               print(e)
               speak('please check your question')


        elif 'stop listening' in query:
            speak('For How many seconds you want me to stop listening?')
            ans=int(takeuserinput())
            print(ans)
            speak(f'sleeping for {ans} seconds ')
            time.sleep(ans)

        elif 'log out' in query:
            os.system('shutdown -1')
        elif 'restart' in query:
            os.system('shutdown /r /t 1')
        elif 'shut down' in query:
            os.system('shutdown /s /t 1')

        elif 'what is'  in query:
            try:
                client = wolframalpha.Client('R6KQ9T-5E69ELVQGJ')
                resp=client.query(query)
                print(next(resp.results).text)
                speak(next(resp.results).text)
            except Exception as e:
                print(e)
                speak('sorry! no result found')

        elif 'turn off' in query:
            speak('Have a Great day Sam')
            exit()


