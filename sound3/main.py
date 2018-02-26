from scipy import *
from scipy.signal import *
import scipy.io.wavfile
#File list
from os import listdir
from os.path import isfile, join

def getFrequency(signal,fs):
    try:
        signal = [s[0] for s in signal]  # Tylko pierwszy kanał
    except:
        return -1
    x = abs(fft(signal))
    x = log(x)
    x[:60] = 0
    y=x.copy()
    for h in arange(2, 6):
        dec=decimate(x, h)
        y[:len(dec)] += dec
    xmax = argmax(y)
    f0=fs*xmax/len(signal)
    return f0

def getData(path):
    freqs = []
    predictions = []
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        print(join(path, f))
        w, signal = scipy.io.wavfile.read(join(path, f))
        f0=getFrequency(signal,w)
        if(f0!=-1):
            freqs.append(f0)
            if (f.endswith("M.wav") == True):
                predictions.append("M")
            else:
                predictions.append("K")
    return {'freqs':freqs,'preds' :predictions}


data = getData("train")
freqs =data['freqs']
print(len(freqs))
predictions=data['preds']
try_anwser = []
for i in range(len(freqs)):
    if(freqs[i]<160):
        try_anwser.append("M")
    else:
        if (freqs[i] > 180):
            try_anwser.append("K")
        else:
            nearMan = abs(160-freqs[i])
            nearWoman = abs(180 - freqs[i])
            if(nearMan>nearWoman):
                try_anwser.append("K")
            else:
                try_anwser.append("M")
count=0
for i in range(len(predictions)):
    if(try_anwser[i]==predictions[i]):
        count+=1

print(count/len(predictions))


