import numpy as np
import pandas as pd
from control import *
from control.matlab import *
import matplotlib.pyplot as plt

class serdes_tx:

    def __init__(self, din, dr, sampleRate):
        self.din = din #input list
        self.dr = dr
        self.sampleRate = sampleRate

    def dataGen(self, tap):
        tap.append(0)
        #tap is a list from -1, 0, 1, 2 ...
        df = pd.DataFrame(self.din)
        sampleRate = self.sampleRate
        #gen FFE output
        df2 = pd.DataFrame(self.din)

        for i in range(0, len(tap)-1):
            if i == 0:
                pass
            else:
                df.insert(i, i, tap[i]*df2[0])
                df[i] = df[i].shift(i)
            df.fillna(0)
            df[0] = df[0] * tap[0]

        df2 = pd.DataFrame(df.apply(lambda x: x.sum(), axis=1))
        df = df2/sum(tap)
        print(df)
        #extend dig data to samplerate
        for i in range(0,sampleRate):
            if i == 0:
                pass
            else:
                df.insert(i, i, df[0])


        df = df.stack()
        return df

    def anaTXout(self, cap, anaData):
        rout = 100
        dr = self.dr
        swing = 0.4
        tt = np.linspace(0, len(anaData), len(anaData))
        pole = 1/rout/1.2/cap/2/np.pi
        sampleRate = self.sampleRate
        dt = 1 / sampleRate
        normpole = 2 * np.pi * pole*1 / dr
        normtxpole2 = 2 * np.pi * pole*2 / dr
        normtxpole1 = 2 * np.pi * pole*4  / dr
        normtxzero = 2 * np.pi * pole*10  / dr

        num = [1]
        den = [1 / normpole / normpole, 1 / normpole * 2, 1]
        numtx = [swing / normtxzero, 1]
        # numtx = [1]
        dentx = [1 / normtxpole1 / normtxpole2, 1 / normtxpole1 + 1 / normtxpole2, 1]
        # dentx=[1]

        sys = tf(numtx, dentx)
        sys2 = tf(num, den)
        syst = series(sys, sys2)
        tt = tt * dt
        # t, y=step(sys)
        y, t, x = lsim(syst, anaData, tt)
        return y, t, x




