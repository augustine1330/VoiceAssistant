import pyttsx3
engine = pyttsx3.init('sapi5')
print('voices', len(engine.getProperty('voices')))
for v in engine.getProperty('voices')[:5]:
    print(v.id, v.name)
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)
engine.say('hello from test')
engine.runAndWait()
print('done')
