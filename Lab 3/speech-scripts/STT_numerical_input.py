import argparse
import queue
import sys
import sounddevice as sd
import json
import subprocess

from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text
    
def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        pass
        # print(status, file=sys.stderr)
    q.put(bytes(indata))

def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


    
device_info = sd.query_devices(None, "input")
# soundfile expects an int, sounddevice provides a float:
samplerate = int(device_info["default_samplerate"])
    
model = Model(lang="en-us")

with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=1,
        dtype="int16", channels=1, callback=callback):
    print("#" * 80)
    print("Press Ctrl+C to stop the recording")
    print("#" * 80)

    rec = KaldiRecognizer(model, samplerate)
    
    # track recognition success
    print("How old are you?")
    subprocess.check_output('./speech-scripts/googletts_arg.sh "how old are you"', shell=True, stderr=subprocess.PIPE, universal_newlines=True)
    success = False
    age = 0
    while not success:
        data = q.get()
        if rec.AcceptWaveform(data):
            recognition = json.loads(rec.Result())["text"]
            try:
                recognized_int = text2int(recognition)
                age = recognized_int
                
                print(recognized_int)
                success = True
            # print(rec.Result())
            except:
                # print(recognition)
                print('Sorry, Please say a number only.')
    
    reply = f'I got it, your age is {age} !'
    print(f'I got it, your age is {age} !')
    subprocess.check_output(f'./speech-scripts/googletts_arg.sh "{reply}"', shell=True, stderr=subprocess.PIPE, universal_newlines=True)
