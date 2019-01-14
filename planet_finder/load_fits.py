import pyfits
import matplotlib.pyplot as plt
import os

class FitsTool:
    def __init__(self, target):
        self.target = target
        files = os.listdir('../data')
        self.hdulists = []
        for file in files:
            if target in file:
                self.hdulists.append(pyfits.open('../data/' + file))
        self.delta = []
        self.cadence = []

    def __str__(self):
        temp = ''
        for d in self.delta:
            temp += str(d) + '\n'
        return temp

    def plot(self):
        plt.plot(self.cadence, self.delta)
        plt.xlabel('Cadence')
        plt.ylabel('Change in Flux e-/sec')
        plt.title(self.target)
        plt.show()

    def walk(self):
        for hdulist in self.hdulists:
            data = hdulist[1].data
            last = data[0][7]
            for d in data:
                # print('Cadence:', d[2], 'Flux:', d[7])
                self.cadence.append(d[2])
                self.delta.append(d[7]-last)
                last = d[7]

f = FitsTool('kplr000757076')
f.walk()
# print(f)
f.plot()
