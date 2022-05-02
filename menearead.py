###############################################
# This script reads and converts the menaion. #
#        Glory to God in the Highest          #
###############################################
import re

months = ['JANUÁR','FEBRUÁR','MÁRCIUS','ÁRPILIS','MÁJUS','JÚNIUS','JÚLIUS','AUGUSZTUS','SZEPTEMBER','OKTÓBER','NOVEMBER','DECEMBER']

# Check if there is a date in the line
def checkDate(st) :
    result = '0'
    i = 0
    for i in months :
        if i in st :
            mth = str(months.index(i)+1).rstrip()
            if int(mth) < 10 : mth = '0'+mth
            day = re.sub('[^0-9]','',st.split(i)[1])
            if day != '' :
                if int(day) < 10 : day = '0'+day
                result = '['+mth+'.'+day+']'
    return result

def replaceHungarian(st) :
    st = st.replace(' ','')
    st = st.replace('á','a')
    st = st.replace('é','e')
    st = st.replace('í','i')
    st = st.replace('ó','o')
    st = st.replace('ö','o')
    st = st.replace('ő','o')
    st = st.replace('ú','u')
    st = st.replace('ü','u')
    st = st.replace('ű','u')
    st = st.replace('Á','A')
    st = st.replace('É','E')
    st = st.replace('Í','I')
    st = st.replace('Ó','O')
    st = st.replace('Ö','O')
    st = st.replace('Ő','O')
    st = st.replace('Ú','U')
    st = st.replace('Ü','U')
    st = st.replace('Ű','U')
    return st

# Check similarity between strings
def checkSimilar(template,st) :
    ratio = 0.0
    template = replaceHungarian(template)
    st = replaceHungarian(st)
    maxmatch = 0
    tmp = template
    i = len(tmp)
    while i > 2 :
        i = len(tmp)
        if tmp in st and i > maxmatch : maxmatch = i
        tmp = tmp[1:]
    tmp = template
    i = len(tmp)
    while i > 2 :
        i = len(tmp)
        if tmp in st and i > maxmatch : maxmatch = i
        tmp = tmp[:-1]
    ratio = maxmatch/len(template)    
    return ratio

# Main loop
date = '00.00'
section = ''
new = open('Books/menea_5_6_normalized.txt','w',encoding='utf8')
with open('Books/menea_5_6.txt','rb') as file :
    while True :
        line = file.readline().decode('utf8')
        if not line : break
        render = False
        line = line.rstrip('-\r\n')+' '
        if section != '' : render = True
        linedate = checkDate(line)
        # Check for section starts
        if checkSimilar('Uram, tehozzád...',line) > 0.6 :
            new.write('[/]\n')
            new.write('[LIC]\n')
            section = 'LIC'
        if checkSimilar('Előverses sztihirák:',line) > 0.6 :
            new.write('[/]\n')
            new.write('[APO]\n')
            section = 'APO'
        if checkSimilar('Tropár. hang.',line) > 0.6 :
            new.write('[/]\n')
            new.write('[TRP]\n')
            section = 'TRP'
        if checkSimilar('Az első zsoltárcsoport után',line) > 0.6 :
            new.write('[/]\n')
            new.write('[ST1]\n')
            section = 'ST1'
        if checkSimilar('A második zsoltárcsoport után',line) > 0.6 :
            new.write('[/]\n')
            new.write('[ST2]\n')
            section = 'ST2'
        if checkSimilar('. óda.',line) > 0.6 :
            new.write('[/]\n')
            new.write('[ODX]\n')
            section = 'ODX'
        if checkSimilar('Kathizma:',line) > 0.6 :
            new.write('[/]\n')
            new.write('[KTH]\n')
            section = 'KTH'
        if checkSimilar('Konták:',line) > 0.6 :
            new.write('[/]\n')
            new.write('[KNT]\n')
            section = 'KNT'
        if checkSimilar('Ikosz.',line) > 0.6 :
            new.write('[/]\n')
            new.write('[IKS]\n')
            section = 'IKS'
        if checkSimilar('Fényének:',line) > 0.6 :
            new.write('[/]\n')
            new.write('[EXA]\n')
            section = 'EXA'
        if checkSimilar('Dicséreti sztihirák:',line) > 0.6 :
            new.write('[/]\n')
            new.write('[PRS]\n')
            section = 'PRS'
        # Check for dates
        if linedate != '0' and linedate == date : render = False
        if linedate != '0' and linedate != date :
            date = linedate
            new.write('[//]\n')
            new.write(date+'\n')
            section = ''
        # Do not copy too short or empty lines    
        if len(line) < 3 : render = False
        # Copy idiom
        if render == True :
            if line[-2] == '.' or line[-2] == '!' or line[-2] == '?' : line += '\n'
            new.write(line)

new.close()