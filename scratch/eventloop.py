import pyttsx

txt = '''

Our deepest fear is not that we are inadequate. 
Our deepest fear is that we are powerful beyond measure. 
It is our light, not our darkness that most frightens us. 
We ask ourselves, Who am I to be brilliant, gorgeous, talented, fabulous? Actually, who are you not to be? You are a child of God. 
Your playing small does not serve the world. 
There is nothing enlightened about shrinking so that other people won't feel insecure around you. 
We are all meant to shine, as children do. 
We were born to make manifest the glory of God that is within us. 
It's not just in some of us; it's in everyone. 
And as we let our own light shine, we unconsciously give other people permission to do the same. 
As we are liberated from our own fear, our presence automatically liberates others

'''

def onStart(name):
    print 'starting', name

def onWord(name, location, length):
    print txt[location: location+length],

def onEnd(name, completed):
    print 'finishing', name, completed
    engine.endLoop()

engine = pyttsx.init()

rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)

engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)
engine.say(txt)
engine.startLoop()