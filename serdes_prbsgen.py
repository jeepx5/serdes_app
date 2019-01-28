import numpy as np
from pyecharts import Line
import pandas as pd
from pyecharts.engine import create_default_environment

class prbs_gen:
    def __init__(self, seed):
        self.seed = seed

    def prbs7(self):
        if len(self.seed) != 7:
            print("wrong input of seed or num")

        # x^7+x^6+1
        seq = self.seed
        while len(seq) <= 127:
            seq.insert(0, seq[5] ^ seq[6])
        return seq*2

    def prbs15(self):
        if len(self.seed) != 15:
            print("wrong input of seed or num")

        # x^15+x^14+1
        seq = self.seed
        while len(seq) <= 2 ** 15 - 1:
            seq.insert(0, seq[13] ^ seq[14])
        return seq

    def prbs_ext(self, din, n):
        dintmp=np.array(din)
        dintmplst=dintmp.T.repeat(n)
        print(dintmplst)
        return dintmplst

if __name__ == '__main__':
    seed = [0, 1, 0, 0, 1, 0, 1]
    prbsgen = prbs_gen(seed)
    dig1b = prbsgen.prbs7()
    bitNum = np.array(range(len(dig1b)))
    print(dig1b)
    line = Line('PRBS7')
    line.add('dig1bit', bitNum, dig1b)
    line.show_config()
    env = create_default_environment("html")
    env.render_chart_to_file(line, path="./plot/prbs_dig1b.html")
