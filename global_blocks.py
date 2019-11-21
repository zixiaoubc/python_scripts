import math
import numpy as np

DATABASE_AS = 3
DEG_WIDTH   = int(3600 / DATABASE_AS)
BLOCK_WIDTH = 1024
BLOCK_WIDTH_IN_DEG = BLOCK_WIDTH / DEG_WIDTH

def getLatSplitLine(logPrint = True):
    splitLats =[]
    for i in range(1, 10):
        splitLat = math.acos(1.0 /(2 ** i)) * 180.0 / math.pi
        splitLats.append(splitLat)

    tileNums =[]
    realSplitLats = [0.0]
    for i, v in enumerate(splitLats):
        t_ = (v - realSplitLats[i]) / BLOCK_WIDTH_IN_DEG
        if t_ % 1 < 1.0e-6:
            tileNum = int(math.floor(t_))
        else:
            tileNum = int(math.ceil(t_))
        #In case can't fit one tile
        if tileNum <= 0:
            tileNum = 1
        realSplitLat = realSplitLats[i] + tileNum * BLOCK_WIDTH_IN_DEG

        if realSplitLat >= 90.0:
            break

        realSplitLats.append(realSplitLat)
        tileNums.append(tileNum)

    if logPrint:
        print('split latitude in theory', splitLats[ : len(tileNums)])
        print('real split latitude', realSplitLats[1 : ])
        print('tile num in y direction', tileNums)

    return np.array(tileNums, dtype = np.uint32)


def getLonSplitLine(logPrint = True):
    tn         = getLatSplitLine(False)
    levelN     = len(tn)

    tileWidths = BLOCK_WIDTH * np.array([2 ** i for i in range(levelN)]).astype(int)
    lonWidth   = 180 * DEG_WIDTH
    tns        = lonWidth / tileWidths
    tileNums   = np.array([int(math.floor(n)) for n in tns], dtype = np.uint32)

    if logPrint:
        print('tile num in x direction', tileNums)

    return tileNums

getLatSplitLine(logPrint = True)
getLonSplitLine(logPrint = True)
