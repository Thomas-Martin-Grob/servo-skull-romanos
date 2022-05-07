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
fname = 'menea_5_6'
date = '00.00'
section = ''
ode = 0
tone = ''
### Normalizing
print('+++ '+fname+' is being normalzed. +++')
new = open('Books/'+fname+'_normalized.txt','w',encoding='utf8')
with open('Books/'+fname+'.txt','rb') as file :
    while True :
        line = file.readline().decode('utf8')
        if not line : break
        render = False
        line = line.rstrip('-\r\n')+' '
        if section != '' : render = True
        linedate = checkDate(line)
        newsection = ''
        # Check for section starts
        if checkSimilar('Uram, tehozzád...',line) > 0.6 : newsection = 'LIC'
        if checkSimilar('Előverses sztihirák:',line) > 0.6 : newsection = 'APO'
        if checkSimilar('Tropár. hang.',line) > 0.6 : newsection = 'TRP'
        if checkSimilar('Kathizma:',line) > 0.6 : newsection = 'KTH'
        if checkSimilar('Az első zsoltárcsoport után',line) > 0.6 : newsection = '1ST'
        if checkSimilar('A második zsoltárcsoport után',line) > 0.6 : newsection = '2ST'
        if checkSimilar('. óda.',line) > 0.6 :
            if ode == 1 : ode = 2
            ode += 1
            newsection = 'OD'+str(ode)
        if checkSimilar('Konták:',line) > 0.6 : newsection = 'KNT'
        if checkSimilar('Ikosz.',line) > 0.6 : newsection = 'IKS'
        if checkSimilar('Fényének:',line) > 0.6 : newsection = 'EXA'
        if checkSimilar('Dicséreti sztihirák:',line) > 0.6 : newsection = 'PRS'
        if newsection != '' :
            new.write('[/]\n')
            new.write('['+newsection+']\n')
            if 'OD' in newsection and ode > 1 : new.write('[T'+tone+']')
            section = newsection
            render = False
        # Inline checks
        if 'Theotokion:' in line and 'OD' in section : line = line.replace('Theotokion:','[M]')
        if '. hang.' in line :
            newtone = line[line.find('. hang.')-1]
            if newtone.isnumeric() == True :
                new.write('[T'+newtone+']')
                tone = newtone
                render = False
        # Check for dates
        if linedate != '0' and linedate == date : render = False
        if linedate != '0' and linedate != date :
            date = linedate
            new.write('[//]\n')
            new.write(date+'\n')
            section = ''
            ode = 0
        # Do not copy too short or empty lines    
        if len(line) < 3 : render = False
        # Copy idiom
        if render == True :
            line = line.replace('m ','m') # Typical scanalation error fix attempt
            if line[-2] == '.' or line[-2] == '!' or line[-2] == '?' : line += '\n'
            new.write(line)
new.close()
print('+++ Done. +++')
print(' ')
print('+++ Vespers file for '+fname+' is being built. +++')
section = ''
new = open('Books/vsp_'+fname+'.txt','w',encoding='utf8')
with open('Books/'+fname+'_normalized.txt','rb') as file :
    while True :
        line = file.readline().decode('utf8').rstrip('\r\n')
        if not line : break
        render = False
        newday = False
        newsection = ''
        if section == 'LIC' or section == 'APO' or section == 'TRP' : render = True
        if '[' in line and '/' not in line :
            pos = line.find('[')
            if line[pos+4] == ']' : newsection = line[pos+1:pos+4]
            if line[pos+3] == '.' : newday = True
        if newsection == 'LIC' or newsection == 'APO' or newsection == 'TRP' :
            new.write('['+newsection+']\n')
            section = newsection
            render = False
        if '[/]' in line :
            if section != '' : new.write('[/]\n')
            section = ''
            render = False
        if '[//]' in line :
            new.write('[//]\n')
            section = ''
            render = False
        if newday == True :
            new.write(line+'\n')
            section = ''
            render = False
        if render == True :
            line = line.replace('­ ','')
            new.write(line+'\n')
new.close()
print('+++ Done. +++')
print(' ')
print('+++ Matins file for '+fname+' is being built. +++')
section = ''
new = open('Books/mtn_'+fname+'.txt','w',encoding='utf8')
with open('Books/'+fname+'_normalized.txt','rb') as file :
    while True :
        line = file.readline().decode('utf8').rstrip('\r\n')
        if not line : break
        render = False
        newday = False
        newsection = ''
        if 'OD' in section or 'ST' in section or section == 'KTH' or section == 'KNT' or section == 'IKS' or section == 'EXA' or section == 'PRS' : render = True
        if '[' in line and '/' not in line :
            pos = line.find('[')
            if line[pos+4] == ']' : newsection = line[pos+1:pos+4]
            if line[pos+3] == '.' : newday = True
        if 'OD' in newsection or 'ST' in newsection or newsection == 'KTH' or newsection == 'KNT' or newsection == 'IKS' or newsection == 'EXA' or newsection == 'PRS' :
            new.write('['+newsection+']\n')
            section = newsection
            render = False
        if '[/]' in line :
            if section != '' : new.write('[/]\n')
            section = ''
            render = False
        if '[//]' in line :
            new.write('[//]\n')
            section = ''
            render = False
        if newday == True :
            new.write(line+'\n')
            section = ''
            render = False
        if render == True :
            line = line.replace('­ ','')
            new.write(line+'\n')
new.close()
print('+++ Done. +++')
print(' ')
print('+++ The machine spirit is willing. +++')
