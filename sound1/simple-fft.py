#!/usr/bin/env python
# -*- coding: utf -*-
from __future__ import division
from pylab import *
from numpy import *
from scipy import *

w = 20           # częstotliwość próbkowania [Hz]
T = 1           # rozważany okres [s]

n = T * w        # liczba próbek
t = linspace(0, T, n, endpoint=False) # punkty na osi OX [s]
F=1
f = lambda t : sin(2*pi*t)#sin(2*pi*F*t)    # def. funkcji
signal = f(t)                 # funkcja spróbkowana

subplot(211)
plot(t, signal, '*')
xlabel("Czas")
ylabel("Amplituda")
signal1 = fft(signal)
signal1 = abs(signal1)        # moduł
subplot(212)
freqs = linspace(0, w, n, endpoint=False)             # <-- ZACZNIJ TUTAJ. Użyj linspace
stem(freqs, signal1, '-*')
xlabel("Częstotliwość")
ylabel("Amplituda")
#savefig("zad4e1.jpg")

x=random.random(10)
print(x)
print(ifft(fft(x)))

show()
