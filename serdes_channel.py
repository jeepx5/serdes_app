import pandas as pd
from control import *
import serdes_tx


class serdes_ch(serdes_tx):

    def serdes_ch(self, anaData, pole1, pole2):
        rout = 100
        dr = self.dr
        swing = 0.4
        tt = np.linspace(0, len(anaData), len(anaData))
        pole = 1 / rout / 1.2 / cap / 2 / np.pi
        sampleRate = self.sampleRate
        dt = 1 / sampleRate
        normpole = 2 * np.pi * pole * 1 / dr
        normtxpole2 = 2 * np.pi * pole * 2 / dr
        normtxpole1 = 2 * np.pi * pole * 4 / dr
        normtxzero = 2 * np.pi * pole * 10 / dr

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
