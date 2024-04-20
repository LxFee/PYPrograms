import os
import sys

def prework(s : str):
    t = []
    ignore = False
    for ch in s:
        if ch == '[':
            ignore = True
        if ch == ']':
            ignore = False
        if ignore:
            continue
        t.append(ch)
    return str(t)

# s和t的相似度，越大越相似
def calcDis(s : str, t : str):
    pos = []
    mxlen = []
    s = prework(s)
    t = prework(t)
    d = 0
    for ch in s:
        p = t.find(ch)
        if p < 0:
            continue
        l = 1
        for i in range(0, len(pos)):
            if p > pos[i]:
                l = max(l, mxlen[i] + 1)
        mxlen.append(l)
        pos.append(p)
        d = max(d, l)
    return d

def splitFilename(s : str):
    p = s.rfind('.')
    if p < 0:
        return s,""
    return s[0:p],s[p:]

if __name__ == '__main__':

    workspace = sys.argv[1]
    
    files = os.listdir(workspace)

    nfoNames = []
    vedioNames = []

    for file in files:
        if file.endswith('nfo'):
            nfoNames.append(file)
        elif file.endswith('mp4') or file.endswith('mkv'):
            vedioNames.append(file)
    print('{}:{}'.format(len(vedioNames), len(nfoNames)))
    
    for vedioName in vedioNames:
        value = 0
        mostSimilarNfoName = ""
        
        vedioNamePart = splitFilename(vedioName)[0]
        vedioExt = splitFilename(vedioName)[1]
        
        for nfoName in nfoNames:
            nfoNamePart = splitFilename(nfoName)[0]
            d = calcDis(vedioNamePart, nfoNamePart)
            if d > value:
                value = d
                mostSimilarNfoName = nfoNamePart
        
        newVedioName = mostSimilarNfoName + vedioExt
        isOk = input('Similar: {}\t ok?[y]/n| "{}" => "{}"'.format(value, vedioName, newVedioName))
        if isOk == 'n':
            continue
        
        os.rename(os.path.join(workspace, vedioName), os.path.join(workspace, newVedioName))
        
        try:
            os.rename(os.path.join(workspace, vedioNamePart + ".chs.ass"), os.path.join(workspace, mostSimilarNfoName + ".chs.ass"))
        except:
            print("chs file not exist!")
        
        try:
            os.rename(os.path.join(workspace, vedioNamePart + ".cht.ass"), os.path.join(workspace, mostSimilarNfoName + ".cht.ass"))
        except:
            print("cht file not exist!")
        
