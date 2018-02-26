#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt

trendNames = {'2cel.csv':'2-Coev' ,'2cel-rs.csv':'2-Coev-RS','cel-rs.csv':'1-Coev-RS','cel.csv':'1-Coev','rsel.csv':'1-Evol-RS' }

class Result:
	def __init__(self,games,avgs,generation,fname):
		self.games=games
		self.avgs=avgs
		self.fname=trendNames[fname]
		self.generation=generation
def castListToFloat(strList): #Przerabia listę Stringów na listę floatów 
	floatList = []
	for i in range(len(strList)):
		floatList.append(float(strList[i]))
	return floatList
def getAvg(floatList): #liczenie średniej
	return sum(floatList)/len(floatList)
	
def generatePlotData(filename): #Odczytuje dane z pojedynczego pliku
	tab=[];games=[];avgs=[];gen=[];
	with open(filename) as f:
		for line in f:
			tab.append(line.split(','))
	for i in range(1,len(tab)):	
	 	avg=getAvg(castListToFloat(tab[i][2:]))
	 	games.append(int(tab[i][1])/1000)
	 	gen.append(int(tab[i][0]))
	 	avgs.append(avg*100)
	return Result(games,avgs,gen,os.path.basename(filename)) 
	 
def readData():
	data = []
	for f in os.listdir('dane'):
		data.append(generatePlotData('dane/'+f))
	drawPlot(data)

def linePlot(data):
	colors=['r','g','b','c','m','y']
	shapes =['s','D','o','x','v','1']
	ax1=plt.subplot(121) #Wskazanie połówki wykresu
	for i in range(len(data)): #Wczytywanie danych do wykresu 
		plt.plot(data[i].games,data[i].avgs, c=colors[i],label=data[i].fname,marker=shapes[i],markevery=[0,0])
	plt.legend() #Dodanie legendy
	plt.legend(loc=4) #Ustalenia pozycji legendy
	plt.grid(True) #Dodanie siatki
	plt.axis([0.0,500.0,60,100])#Ustalenie zakresów osi X i Y 
	for i in range(len(data)):  #Utworzenie wykresu punktowego
		plt.scatter(data[i].games[::20],data[i].avgs[::20],c=colors[i],marker=shapes[i],linewidths=3)
	plt.ylabel('Odsetek wygranych gier [%]') #Dodanie opisiu osi Y
	plt.xlabel('Rozegranych gier (x1000)') #Dodanie opisiu osi X
	ax12=ax1.twiny() # Dodanie przedziałek osi X do góry
	ax12.set_xticks([0,40,80,120,160,200]) #Ustalenie górnych przediałek
	ax12.set_xlabel('Pokolenie')# Dodanie opisu do górnych przedziałek

def boxPlot(data):
	datalist = [];namelist = [];
	for i in range(len(data)):#Tworzy dane do wykresu
		datalist.append(data[i].avgs)
		namelist.append(data[i].fname)
	ax2=plt.subplot(122)#Wskazanie połówki wykresu
	ax2.yaxis.set_ticks_position('right') # ustwia pozycje przedziałek na osi Y
	plt.boxplot(datalist,labels=namelist,notch=True,whis=1.5,showmeans=True)
	plt.grid(True)#Dodanie siatki
	
def drawPlot(data):
	plt.figure(figsize=(15, 10))
	linePlot(data)
	boxPlot(data)
	plt.show()
	plt.close() 

readData()


