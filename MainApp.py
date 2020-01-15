import tkinter as tk

import matplotlib.pyplot as plot
from matplotlib.pyplot import savefig
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
from pygame import mixer
from scipy import signal
from scipy.io import wavfile


class MainApp():

    def __init__(self, master):
        master.minsize(1200, 400)
        master.title("Spektrogram")
        self.window(master)
        self.plots(master)
        mixer.init()

    def browse_file(self):
        ftypes = [("wave files", "*.wav")]
        self.filename = tk.filedialog.askopenfilename(initialdir="/", filetypes=ftypes, title="Wybierz plik")

    def play_sound(self):
        try:
            print(self.filename)
            mixer.music.load(self.filename)
            mixer.music.play()
        except NameError:
            tk.messagebox.showerror("Nie znaleziono pliku")

    def pause_sound(self):
        mixer.music.stop()

    def window(self,master):
        self.openFile = tk.Button(text="Wybierz plik", command=self.browse_file)
        self.openFile.grid(row=0, column=0, padx=20)

        self.playButton = tk.Button(text="Play", command=self.play_sound)
        self.playButton.grid(row=0, column=6, padx=20)

        self.stopButton = tk.Button(text="Stop", command=self.pause_sound)
        self.stopButton.grid(row=0, column=7, padx=20)

        self.generateButton = tk.Button(text="Generuj", command=self.t_wykres)
        self.generateButton.grid(row=0, column=5, padx=20)



        # PRÓBKA
        probka = tk.Label(root, text="Próbka")
        probka.grid(row=0, column=1, padx=20)


        wartosciProbki = ['128', '256', '512', '1024', '1024', '2048']
        self.zmiennaProbka = tk.StringVar(root)
        self.zmiennaProbka.set('16')
        self.popupMenu1 = tk.OptionMenu(root, self.zmiennaProbka, *wartosciProbki)
        self.popupMenu1.grid(row=1, column=1, padx=20)

        # ZAKŁADKA
        zakladka = tk.Label(root, text="Długość zakładki")
        zakladka.grid(row=0, column=2, padx=20)


        wartosciZakladki = ["10", "20", "30", "40", "50", "60", "70", "80", "90"]
        self.zmiennaZakladki = tk.StringVar(root)
        self.zmiennaZakladki.set("10")
        self.popupMenu2 = tk.OptionMenu(root, self.zmiennaZakladki, *wartosciZakladki)
        self.popupMenu2.grid(row=1, column=2, padx=20)

        # OKIENKOWANIE
        okienkowanie = tk.Label(root, text="Okienkowanie")
        okienkowanie.grid(row=0, column=3, padx=20)


        wartosciOkienkowania = ["hamming", "triang", "blackman", "hann", "bartlett", "flattop", "bohman", "barthann"]
        self.zmiennaOkienkowanie = tk.StringVar(root)
        self.zmiennaOkienkowanie.set("hamming")
        self.popupMenu3 = tk.OptionMenu(root, self.zmiennaOkienkowanie, *wartosciOkienkowania)
        self.popupMenu3.grid(row=1, column=3, padx=20)



    def t_wykres(self):
        samplingFrequency, signalData = wavfile.read(self.filename)

        if len(signalData.shape) == 2:
            signalData = signalData[:, 0]

        czas = np.arange(len(signalData)) / float(samplingFrequency)

        self.spectogram_ww.clear()
        self.spectogram_ww.grid(True)
        nfft = int(self.zmiennaProbka.get())
        okien = self.zmiennaOkienkowanie.get()
        zakladka = int(self.zmiennaZakladki.get())

        self.spectogram_ww.specgram(signalData, Fs=samplingFrequency, NFFT=nfft, noverlap=zakladka, window=signal.get_window(okien, nfft))
        self.spectogram_ww.set_xlim(xmin=0, xmax=1)
        self.spectCanvas.draw()

        self.amplituda.clear()
        self.amplituda.grid(True)
        self.amplituda.set_xlim(xmin=0, xmax=1)
        self.amplituda.plot(czas, signalData)

        self.waveform_canvas.draw()



    def plots(self, master):
        x = np.zeros(100)
        x1 = np.zeros((100, 2))
        y = [0] * 100
        self.wamp = Figure(figsize=(4, 2), dpi=100)
        self.amplituda = self.wamp.add_subplot(111)
        self.amplituda.grid(True)
        self.amplituda.axhline()
        self.amplituda.set_xlim(xmin=0, xmax=1)
        self.amplituda.plot(x, y)

        self.Wspectogram = Figure(figsize=(4, 2), dpi=100)
        self.spectogram_ww = self.Wspectogram.add_subplot(111)
        self.spectogram_ww.grid(True)
        self.spectogram_ww.specgram(x1, NFFT=256, Fs=2)

        self.spectFrame = tk.Frame(master, relief=tk.RAISED, borderwidth=3)
        self.spectFrame.grid(row=3, column=4)
        title_label_1 = tk.Label(self.spectFrame, text="Spektrogram")
        title_label_1.pack()

        self.spectCanvas = FigureCanvasTkAgg(self.Wspectogram, master=self.spectFrame)
        self.spectogram_ww.set_xlim(xmin=0, xmax=1)
        self.spectCanvas.draw()
        self.spectCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)

        self.waveforms_frame = tk.Frame(master, relief=tk.RAISED, borderwidth=3)
        self.waveforms_frame.grid(row=4, column=4)

        title_label_2 = tk.Label(self.waveforms_frame, text="Fala")
        title_label_2.pack()

        self.waveform_canvas = FigureCanvasTkAgg(self.wamp, master=self.waveforms_frame)
        self.waveform_canvas.draw()
        self.waveform_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    root = tk.Tk()
    my_app = MainApp(root)
    root.mainloop()