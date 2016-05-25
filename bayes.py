import sys
import collections

""" get the symptoms organized corresponding to patient """
def getFofP(symptoms):
    # n: number of diseases; k: number of patients
    result = []
    tmpc = 0
    for i in range(k):
        tmp = []
        for j in range(n):
            tmp.append(symptoms[tmpc])
            tmpc += 1
        result.append(tmp)
    return result

""" READ THE INPUT FILE """
import os
fi = sys.argv[2]
head, tail = os.path.split(fi)
filename = os.path.splitext(tail)[0]
fileextension = os.path.splitext(tail)[1]
inputFile = open(sys.argv[2])

count = 0
c2 = 1
diseases = []
findings = []   # name of the symptoms
p1 = []
p2 = []
pd = [] # probability of a disease
symptoms = []   # symptoms for each patient
for line in inputFile:
    if count == 0:
        spl = line.strip().split(' ')
        n = int(spl[0])  # n: number of diseases
        k = int(spl[1])  # k: number of patients
        limit1 = n * 4
        limit2 = n * k + limit1
        count += 1
    elif count <= limit1:
        # Next 4*n lines will have the details about the diseases and their findings/symptoms, 4 lines for each disease
        if count % 4 == 1:
            spl = line.strip().split(' ')
            name = spl[0]   # the name of the disease (Cancer, Hepatitis, etc)
            m = spl[1]  # its number of findings/symptoms (m)
            p = spl[2]  # the priori probability of the disease P(D)
            diseases.append(name)
            pd.append(p)
            count += 1 
        elif count % 4 == 2:
            # The second line will contain a python list of m finding/symptom names for the disease
            l = eval(line.strip())
            #findings[name] = l
            findings.append(l)
            count += 1 
        elif count % 4 == 3:
            # The third line will contain a python list of m elements giving the probability of the findings/symptoms to be present (true) if the disease is present
            l = eval(line.strip())
            #p1[name] = l
            p1.append(l)
            count += 1 
        else:
            # The forth line will contain a python list of m elements giving the probability of the findings/symptoms to be present(true) if the disease is not present.
            l = eval(line.strip())
            #p2[name] = l 
            p2.append(l)
            count += 1  
    elif count <= limit2:
        symptoms.append(eval(line.strip()))
patients = getFofP(symptoms)

def getProbability(disease, p, pf1, pf2):
    d1 = p  # dividee
    d21 = p  # divider
    d22 = 1 - p
    for i in range(len(disease)):
        if disease[i] == 'T':
            d1 *= pf1[i]
            d21 *= pf1[i]
            d22 *= pf2[i]
        elif disease[i] == 'F':
            d1 *= (1 - pf1[i])
            d21 *= (1 - pf1[i])
            d22 *= (1 - pf2[i])
        elif disease[i] == 'U':
            pass
    d2 = d21 + d22
    #return float(("%.4f" % (d1 / d2))) #round(d1 / d2, 4)   # probability of the disease
    return float(d1 / d2)

"""Question-1:
For each of the diseases, what is the probability that the patient has the disease?
patients, diseases as list; return dict
 p(d|f1,f2)=p(d,f1,f2)/p(f1,f2)=p(f1,f2|d)p(d)/p(f1,f2)=p(f1|d)p(f2|d)p(d)/[p(d)p(f1|d)p(f2|d)+p(nd)p(f1|nd)p(f2|nd)]
"""
def getPofD(patients, diseases):
    result = []
    k = len(patients)   #number of patients
    n = len(diseases)   #number of diseases
    for i in range(k):
        rst = {}
        patient = patients[i]  # symptoms of all diseases of the patient i
        for j in range(n):
            name = diseases[j] # name of disease
            p = float(pd[j]) # probability of the disease
            pf1 = p1[j] # list of probability of the finding present in disease
            pf2 = p2[j]
            disease = patient[j] # findings of symptoms of disease j existing in patient i
            #rst[name] = getProbability(disease, p, pf1, pf2)
            rst[name] = ("%.4f" % getProbability(disease, p, pf1, pf2))
        result.append(rst)
    return result

""" get unkown list """
def getUnkown(test):
    unkown = []
    for i in range(len(test)):
        if test[i] == 'U':
            unkown.append(i)
    return unkown

def getCPT(test):
    result = []
    unkown = getUnkown(test)
    ulen = len(unkown)
    import itertools
    t = list(itertools.product(['F', 'T'], repeat = ulen))
    for i in range(len(t)):
        assign = t[i]
        tmp = []
        cnt = 0
        for i in range(len(test)):
            if i in unkown:
                tmp.append(assign[cnt])
                cnt += 1
            else:
                tmp.append(test[i])
        result.append(tmp)
    return result

"""Question-2:
search the values for the unknown tests that would produce the maximum and minimum probabilities for each disease."""
def getMofD(patients, diseases):
    result = []
    k = len(patients)   #number of patients
    n = len(diseases)   #number of diseases
    for i in range(k):
        rst = {}    # result for [min, max]
        patient = patients[i]  # symptoms of all diseases of the patient i
        for j in range(n):
            name = diseases[j] # name of disease
            tmp = []
            p = float(pd[j]) # probability of the disease
            pf1 = p1[j] # list of probability of the finding present in disease
            pf2 = p2[j]
            disease = patient[j] # findings of symptoms of disease j existing in patient 
            cpt = getCPT(disease)
            for m in range(len(cpt)):
                assign = cpt[m]
                tmp.append(getProbability(assign, p, pf1, pf2))
            #rst[name] = [min(tmp), max(tmp)]  #[min, max]
            rst[name] = [("%.4f" % min(tmp)), ("%.4f" % max(tmp))]
        result.append(rst)
    return result

""" Set disease[index] = val; index is in unkown list; return new list of disease """
def getValOfUn(disease, index, val):
    result = []
    length = len(disease)
    for i in range(length):
        if i == index:
            result.append(val)
        else:
            result.append(disease[i])
    return result

def getIndex(change, val):
    result = []
    for i in range(len(change)):
        if change[i] == val:
            result.append(i)
    return result

def getAlpha(idlist, sym):
    result = []
    d = {}
    for i in idlist:
        d[sym[i]] = i
    dd = collections.OrderedDict(sorted(d.items()))
    #print dd
    for key, value in dd.iteritems() :
        result.append(value)
    return result

"""Question-3:
which of the tests not done yet for each disease (result either true or false) would produce the biggest increase and which would produce the biggest decrease in the probabilities for that diseases"""
def getMCrease(patients, diseases, findings):
    result = []
    for i in range(len(patients)):
        patient = patients[i]
        rst = {}
        for j in range(len(diseases)):
            disease = patient[j]    # symptoms of the disease
            name = diseases[j]   # disease name
            unkown = getUnkown(disease)
            finding = findings[j]
            p = float(pd[j]) # probability of the disease
            pf1 = p1[j] # list of probability of the finding present in disease
            pf2 = p2[j]
            sym = []    # the unkown symptom which is set
            change = [] # increase or decrease in value
            val = []    # 'T' or 'F' set to the symptom
            origin = getProbability(disease, p, pf1, pf2)   # original probability
            if len(unkown) == 0:
                rst[name] = ['none', 'none', 'none', 'none']
            else:
                for k in range(len(unkown)):
                    symname = finding[unkown[k]]
                    # assign kth unkown symptom to true
                    nd1 = getValOfUn(disease, unkown[k], 'T') # new list of disease
                    c1 = float(("%.4f" % (getProbability(nd1, p, pf1, pf2) - origin)))    
                    #c1 = getProbability(nd1, p, pf1, pf2) - origin # increase or decrease
                    change.append(c1)
                    sym.append(symname)
                    val.append('T')
                    # assign kth unkown symptom to false
                    nd2 = getValOfUn(disease, unkown[k], 'F')
                    c2 = float(("%.4f" % (getProbability(nd2, p, pf1, pf2) - origin)))    #getProbability(nd1, p, pf1, pf2) - origin # increase or decrease        
                    #c2 = getProbability(nd2, p, pf1, pf2) - origin
                    change.append(c2)
                    sym.append(symname)
                    val.append('F')
                #print change
                max_inc = max(change)   # the biggest increase in the probability of the disease
                max_dec = min(change)   # the biggest decrease in the probability for the disease
                tmp = []
                if max_dec == 0 and max_inc == 0:
                    tmp.append('none')
                    tmp.append('none')
                    tmp.append('none')
                    tmp.append('none')
                elif max_inc <= 0 and max_dec < 0:   # all are decreasing
                    tmp.append('none')
                    tmp.append('none')
                    idlist = getAlpha(getIndex(change, max_dec), sym)
                    for x in idlist:
                        tmp.append(sym[x])
                        tmp.append(val[x])
                elif max_dec >= 0 and max_inc > 0:   # all are increasing
                    idlist = getAlpha(getIndex(change, max_inc), sym)
                    for x in idlist:
                        tmp.append(sym[x])
                        tmp.append(val[x])
                    tmp.append('none')
                    tmp.append('none')
                elif max_dec < 0 and max_inc > 0:
                    idlist = getAlpha(getIndex(change, max_inc), sym)
                    for x in idlist:
                        tmp.append(sym[x])
                        tmp.append(val[x])
                    idlist = getAlpha(getIndex(change, max_dec), sym)
                    for x in idlist:
                        tmp.append(sym[x])
                        tmp.append(val[x])
                #print tmp
                rst[name] = tmp
        result.append(rst)
    return result

""" WRITE TO THE OUPUT FILE """
out = filename + "_inference" + fileextension
f = open(out, 'w+')
result = ''
rl = getPofD(patients, diseases)
rl2 = getMofD(patients, diseases)
rl3 = getMCrease(patients, diseases, findings)
for i in range(k):
    result += 'Patient-' + str(i + 1) + ':\n'
    result += str(rl[i]) + '\n'
    result += str(rl2[i]) + '\n'
    result += str(rl3[i]) + '\n'
f.write(result)