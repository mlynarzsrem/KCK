#!/usr/bin/env python
# -*- coding: utf -*-
from __future__ import division
from pylab import *
from numpy import *
from scipy import *

import scipy.io.wavfile
w, signal = scipy.io.wavfile.read('err.wav')
signal = [s[0] for s in signal]
signal =signal[::10]
subplot(211)
plot(signal)
sampCount=len(signal)
#linspace(0, w, n, endpoint=False)
freqs = np.fft.fftfreq(sampCount)
signal1 =fft(signal)
signal1 = abs(signal1)
subplot(212)
plot(freqs,signal1)
yscale('log')
show()