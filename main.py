import os
from fileinput import filename
from tkinter import *
import tkinter as tk
from tkinter import filedialog

import numpy as np
from matplotlib.figure import Figure
from pygame import mixer
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.title("Spektogram")
root.minsize(1300, 500)

mixer.init()


# przycisk i funkcja otwieranie pliku


def file_open():
    ftypes = [("wave files", "*.wav")]
    root.file1 = filedialog.askopenfile(initialdir="/", filetypes=ftypes, title="Open file")
    return root.file1


openFile = tk.Button(text="Wybierz plik", command=file_open)
openFile.grid(row=0, column=0, padx=20)

# menu - tekst oraz przyciski

# PRÓBKA
probka = tk.Label(root, text="Próbka")
probka.grid(row=0, column=1, padx=20)

zmiennaProbka = tk.StringVar(root)
wartosciProbki = ['16', '32', '64', '128', '256', '512', '1024', '1024', '2048']
zmiennaProbka.set('16')
popupMenu1 = tk.OptionMenu(root, zmiennaProbka, *wartosciProbki)
popupMenu1.grid(row=1, column=1, padx=20)

# ZAKŁADKA
zakladka = tk.Label(root, text="Długość zakładki")
zakladka.grid(row=0, column=2, padx=20)

zmiennaZakladki = tk.StringVar(root)
wartosciZakladki = ["10", "20", "30", "40", "50", "60", "70", "80", "90"]
zmiennaZakladki.set("10")
popupMenu2 = tk.OptionMenu(root, zmiennaZakladki, *wartosciZakladki)
popupMenu2.grid(row=1, column=2, padx=20)

# OKIENKOWANIE
okienkowanie = tk.Label(root, text="Okienkowanie")
okienkowanie.grid(row=0, column=3, padx=20)

zmiennaOkienkowanie = tk.StringVar(root)
wartosciOkienkowania = ["hamming", "triang", "blackman", "hann", "bartlett", "flattop", "bohman", "barthann"]
zmiennaOkienkowanie.set("hamming")
popupMenu3 = tk.OptionMenu(root, zmiennaOkienkowanie, *wartosciOkienkowania)
popupMenu3.grid(row=1, column=3, padx=20)


# przycisk oraz funkcja odtwarzajaca dźwięk
def play_sound():
    try:
        print(root.file1)
        mixer.music.load(root.file1)
        mixer.music.play()
    except NameError:
        tk.messagebox.showerror("File not found")


playButton = tk.Button(text="Play", command=play_sound)
playButton.grid(row=0, column=6, padx=20)


# przycisk oraz funkcja zatrzymująca dźwięk
def stop_sounds():
    mixer.music.stop()


stopButton = tk.Button(text="Stop", command=stop_sounds)
stopButton.grid(row=0, column=7, padx=20)

x = np.zeros(100)
x1 = np.zeros((100, 2))
y = [0] * 100
waveform_figure = Figure(figsize=(4, 2), dpi=100)
waveform_axes = waveform_figure.add_subplot(111)
waveform_axes.grid(True)
waveform_axes.axhline()
waveform_axes.set_xlim(xmin=0)
waveform_axes.plot(x, y)

xval = np.zeros(1000)
yval = [0] * 1000


def plot():
    figure = Figure(figsize=(4, 2), dpi=100)
    axes = figure.add_subplot(111)
    axes.grid(True)
    axes.axhline()
    axes.set_xlim(left=0)
    axes.plot(xval, yval)
    return figure


# wykres fali
frame_plot = tk.Frame(root, relief=RAISED, borderwidth=3)
frame_plot.grid(row=3, column=4)
title_label = tk.Label(root, text="Wykres fali", font=("Times", "15", "bold"))
title_label.grid(row=2, column=4)
figure_wave = plot()
canvas_wave = FigureCanvasTkAgg(figure_wave, frame_plot)
canvas_wave.draw()
canvas_wave.get_tk_widget().grid(row=3)

# spektogram fali
spectogram_figure = Figure(figsize=(4, 2), dpi=100)
spectogram_axes = spectogram_figure.add_subplot(111)
spectogram_axes.grid(True)
spectogram_axes.specgram(x1, NFFT=256, Fs=2)

spectrums_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=3)
spectrums_frame.grid(row=5, column=4)

title_label_2 = tk.Label(text="Spektogram fali", font=("Times", "15", "bold"))
title_label_2.grid(row=4, column=4)

spectogram_canvas = FigureCanvasTkAgg(spectogram_figure, spectrums_frame)
spectogram_canvas.draw()
spectogram_canvas.get_tk_widget().grid(row=6)


def generate_plots():
    samplingFrequency, signalData = wavfile.read(root.file1)

    if len(signalData.shape) == 2:
        signalData = signalData[:, 0]

    time = np.arange(len(signalData)) / float(samplingFrequency)

    waveform_axes.clear()
    waveform_axes.grid(True)
    waveform_axes.set_xlim(xmin=0)
    waveform_axes.plot(time, signalData)
    canvas_wave.draw()

    spectogram_axes.clear()
    spectogram_axes.grid(True)
    print(type(signalData))


    overlap_temp = int(zmiennaZakladki.get()) / 100
    spectogram_axes.specgram(signalData, Fs=samplingFrequency, NFFT=int(zmiennaProbka.get()),
                             window=signal.get_window(zmiennaOkienkowanie.get(), int(wartosciProbki.get())),
                             noverlap=overlap_temp)
    spectogram_canvas.draw()


generateButton = tk.Button(text="Generuj", command=generate_plots)
generateButton.grid(row=0, column=5, padx=20)

root.mainloop()
