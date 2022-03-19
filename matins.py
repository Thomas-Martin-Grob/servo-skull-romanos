###########################################
# This script compiles texts for matins.  #
#      Glory to God in the Highest        #
###########################################
from fpdf import FPDF
import datetime

# Page design elements
class PDF(FPDF):
    def header(self):
        self.image('frame.jpg',0,0,148)
        self.set_margins(20,30,20)
        self.set_y(1.5)
        self.set_font('IMFell','',9)
        self.set_text_color(0,0,0)
        self.cell(0,10,stitle,0,0,'C')
        self.set_y(20)
        #self.ln()

    def footer(self):
        self.set_y(-12)
        self.set_font('IMFell','',9)
        self.set_text_color(0,0,0)
        self.cell(0,10,str(self.page_no()),0,0,'C')

    def chapter_title(self,label):
        h = 4
        # Break page if chapter title would be at the bottom
        ypos = self.get_y()
        if ypos > 150 :
            h = 185-ypos
            self.ln(h)
        self.set_font('Gothic','',16)
        self.set_text_color(128,0,0)
        self.cell(0,7,label,0,1,'C')
        self.ln(4)

# Get the date for upcoming sunday
def getNextSunday() :
    nxt = ''
    current = datetime.date.today()
    delta = 6-datetime.date.weekday(current)
    nextsunday = current+datetime.timedelta(days=delta)
    print('***************************')
    if delta != 0 : print('The day is '+current.strftime ('%d.%m.%Y')+', the next Sunday will be '+nextsunday.strftime('%d.%m.%Y.'))
    if delta == 0 : print('The day is Sunday, '+current.strftime ('%d.%m.%Y.'))
    nxt = nextsunday.strftime('%d %m %Y')
    return nxt

# Get the tone of the week
def getWeeklyTone() :
    ### Get date of last Pascha
    current = datetime.date(2022,int(menea.split('.')[0]),int(menea.split('.')[1]))
    pascha = current
    with open('Books/paschalia.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            readnumbers = line.rstrip('\n').split('.')
            readdate = datetime.date(int(readnumbers[0]),int(readnumbers[1]),int(readnumbers[2]))
            diff = (current-readdate).days
            if diff >= 0 : pascha = diff
    ### Calculate tone
    weeks = (pascha//7)-1
    todaystone = (weeks%8)+1
    if weeks < 1 : todaystone = 1
    print('    The tone of the week will be tone '+str(todaystone)+'.')
    return todaystone

# Get the name of a nominal day, if there is any
def getNominal() :
    ### Dictionary of nominal days
    sunday = {-70:'Publican and Pharisee',
              -63:'Prodigal Son',
              -56:'Meatfare',
              -49:'Cheesefare',
              -42:'Orthodoxy',
              -35:'Saint Gregory Palamas',
              -28:'Holy Cross',
              -21:'Saint John Climacus',
              -14:'Saint Mary of Egypt',
              -7:'Palm Sunday',
              0:'Pascha',
              7:'Thomas'
              }
    ### Get dates of previous and next Pascha
    current = datetime.date(curryear,int(menea.split('.')[0]),int(menea.split('.')[1]))
    lastp = -10
    nextp = -356
    with open('Books/paschalia.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            readnumbers = line.rstrip('\n').split('.')
            readdate = datetime.date(int(readnumbers[0]),int(readnumbers[1]),int(readnumbers[2]))
            diff = (current-readdate).days
            if diff >= 0 : lastp = diff
            if diff < 0 and diff > nextp : nextp = diff
    nom = ''
    if lastp in sunday : nom = sunday[lastp]
    if nextp in sunday : nom = sunday[nextp]
    prtr = False
    lnt = False
    if nextp == -70 or nextp == -63 or nextp == -56 : prtr = True
    if nextp > -57 and nextp < 0 : lnt = True
    return [nom,prtr,lnt]

def getDayName() :
    dname = ''
    with open('Books/calendar.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if '['+nomen+']' in line :
                dname = line.lstrip('['+nomen+']').rstrip('\r\n')
                break
            if '['+menea+']' in line :
                dname = line.lstrip('['+menea+']').rstrip('\r\n')
                break
    if dname != '' : print('    This Sunday is '+dname+'.')
    if dname == '' : print('    This Sunday is not a named Sunday.')
    return dname

# Read a text section from a file
def readSection(fname,sname):
    txt = ''
    okay = False
    with open(fname,'rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if okay == True and '[/]' in line :
                break
            if okay == True : txt += line
            if '['+sname+']' in line : okay = True
    return txt

# Print a standard text section from horologion
def printSection(sttl,section,tn=0) :
    pdf.chapter_title(sttl)
    txt = readSection('Books/mtn_horologion.txt',section).split('[')
    for line in txt :
        pdf.set_font('IMFell','',12)
        pdf.set_text_color(0,0,0)
        if 'R]' in line :
            line = line.lstrip('R]')
        if 'I]' in line :
            line = line.lstrip('I]')
            if tn : line = line.replace('%',str(tn))
            pdf.set_font('IMFell','',12)
            pdf.set_text_color(128,0,0)
        if 'P]' in line :
            line = line.lstrip('P]')
            pdf.set_font('Gothic','',12)
            pdf.set_text_color(0,0,0)
        if len(line) > 2 : pdf.multi_cell(0,6,line)
    pdf.ln()
    print('    Printed '+section+'.')
    return

# Print a standard text section from Octoechos
def printOcto(sttl,section,common) :
    pdf.chapter_title(sttl)
    tone = weekly
    pdf.set_font('IMFell','',12)
    pdf.set_text_color(0,0,0)
    okay = 0
    with open('Books/mtn_octoechos.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[T' in line :
                    pdf.set_text_color(128,0,0)
                    pdf.multi_cell(0,6,line[2]+'. hang')
                    line = line[4:]
                    pdf.set_text_color(0,0,0)
                pdf.multi_cell(0,6,line)
            if '[Tone '+str(tone)+']' in line : okay = 1
            if '['+section+']' in line and okay == 1 : okay = 2
    pdf.ln()
    print('    Printed '+common+'.')
    return

# Compile 'Lord I call'
def printLordICall() :
    tone = weekly
    verses = ['','','','','','','','','','','','']
    pre = ['10. Vezesd ki a tömlöcből az én lelkemet, hogy magasztaljam a Te nevedet.',
    '9. Körülvesznek engem az igazak, amikor majd jót teszel velem.',
    '8. A mélységből kiáltottam Hozzád, Uram. Uram, hallgasd meg az én hangomat.',
    '7. Legyenek füleid figyelmesek könyörgésem hangjára.',
    '6. Ha számbaveszed a törvényszegéseket, Uram, Uram, ki állhat meg Előtted? De Tenálad van a könyörület.',
    '5. A Te nevedért vártalak, Uram; várta a lelkem a Te igédet; reménykedett az én lelkem az Úrban.',
    '4. A reggeli őrségváltástól az éjszakáig, a reggeli őrségváltástól reménykedjék Izrael az Úrban.',
    '3. Mert az Úrnál van az irgalom, és nagy Őnála a szabadítás, és Ő szabadítja meg Izraelt annak minden vétkeitől.',
    '2. Dicsérjétek az Urat minden nemzetek, magasztaljátok Őt minden népek.',
    '1. Mert nagy volt az Ő irgalma mirajtunk, és az Ő igazsága mindörökké megmarad.',
    'Dicsőség az Atyának és Fiúnak és Szent Léleknek.',
    'Most és mindenkor és mindörökkön örökké. Ámin.']
    ### Print intro
    printSection('Uram Tehozzád kiáltottam','Lord I Call',tone)
    ### Read verses from Octoechos
    okay = 0
    n = 0
    with open('Books/vsp_octoechos.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[D]' in line : verses[10] = line[3:]
                if '[M]' in line : verses[11] = line[3:]
                if '[D]' not in line and '[M]' not in line :
                    verses[n] = line
                    n += 1
            if '[Tone '+str(tone)+']' in line : okay = 1
            if '[LIC]' in line and okay == 1 : okay = 2
    ### Read verses from Menaion
    okay = 0
    mvers = []
    with open('Books/vsp_menea.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[D]' in line : verses[10] = line[3:]
                if '[M]' in line : verses[11] = line[3:]
                if '[D]' not in line and '[M]' not in line :
                    mvers.append(line)
            if '['+menea+']' in line : okay = 1
            if '[LIC]' in line and okay == 1 : okay = 2
    ### Read verses from Triodion
    okay = 0
    tvers = []
    with open('Books/vsp_triodion.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[D]' in line : verses[10] = line[3:]
                if '[M]' in line : verses[11] = line[3:]
                if '[D]' not in line and '[M]' not in line :
                    tvers.append(line)
            if '['+nomen+']' in line : okay = 1
            if '[LIC]' in line and okay == 1 : okay = 2
    ### Combine verses
    m = len(mvers)
    t = len(tvers)
    if m+t > 10 : mvers = mvers[0:(10-t)]
    mvers += tvers
    m = 10-len(mvers)
    n = 0
    while m < 10 :
        verses[m] = mvers[n]
        n += 1
        m += 1
    ### Print the compiled verses
    n = 0
    tone = weekly
    oldtone = tone
    while n < len(verses) :
        if '[T' in verses[n] :
            oldtone = tone
            tone = int(verses[n][2])
            verses[n] = verses[n][4:]
        if oldtone == tone :
            txt = pre[n]+'\n\n'+verses[n]
            pdf.multi_cell(0,6,txt)
            pdf.ln()
        if oldtone != tone :
            txt = pre[n]+'\n\n'+verses[n]
            pdf.multi_cell(0,6,pre[n])
            pdf.ln()
            pdf.set_text_color(128,0,0)
            pdf.multi_cell(0,6,'('+str(tone)+'. hang)')
            pdf.set_text_color(0,0,0)
            pdf.multi_cell(0,6,verses[n])
            pdf.ln()
            oldtone = tone
        n += 1
    print('    Compiled Lord I Call.')
    return

# Compile kathismata
def printKathisma(ctit,mark) :
    pdf.chapter_title(ctit)
    pdf.set_font('IMFell','',12)
    pdf.set_text_color(0,0,0)
    tone = weekly
    trp = ['','','']
    ### Read kathismata from Octoechos
    okay = 0
    with open('Books/mtn_octoechos.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[D]' not in line and '[M]' not in line : trp[0] = line
                if '[D]' in line : trp[1] = line[3:]
                if '[M]' in line : trp[2] = line[3:]
            if '[Tone '+str(tone)+']' in line : okay = 1
            if '['+mark+']' in line and okay == 1 : okay = 2
    ### Read kathismata from Menaion
    okay = 0
    with open('Books/mtn_menea.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[D]' not in line and '[M]' not in line : trp[0] = line
                if '[D]' in line : trp[1] = line[3:]
                if '[M]' in line : trp[2] = line[3:]
            if '['+menea+']' in line : okay = 1
            if '['+mark+']' in line and okay == 1 : okay = 2
    ### Read kathismata from Triodion
    okay = 0
    with open('Books/mtn_triodion.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[D]' not in line and '[M]' not in line : trp[0] = line
                if '[D]' in line : trp[1] = line[3:]
                if '[M]' in line : trp[2] = line[3:]
            if '['+nomen+']' in line : okay = 1
            if '['+mark+']' in line and okay == 1 : okay = 2
    # Print full kathisma
    n = 0
    while n < len(trp) :
        if n == 1 :
            pdf.set_text_color(0,0,0)
            pdf.multi_cell(0,6,'Dicsőség az Atyának és Fiúnak és Szent Léleknek')
            pdf.ln()
        if n == 2 :
            pdf.set_text_color(0,0,0)
            pdf.multi_cell(0,6,'Most és mindenkor és mindörökkön örökké. Ámin.')
            pdf.ln()
        if trp[n] != '' :
            if '[T' in trp[n] :
                tone = trp[n][2]
                txt = trp[n][4:]
                pdf.set_text_color(128,0,0)
                pdf.multi_cell(0,6,'('+str(tone)+'. hang)')
            if '[T' not in trp[n] : txt = trp[n]
            pdf.set_text_color(0,0,0)
            pdf.multi_cell(0,6,txt)
            pdf.ln()
        n += 1
    print('    Compiled kathismata('+mark+').')
    return

def getIrmos(tone,mark) :
    okay = 0
    mark = 'OD'+mark
    with open('Books/mtn_octoechos.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[T' in line :
                    pdf.set_text_color(128,0,0)
                    pdf.multi_cell(0,6,'('+line[2]+'. hang)')
                    pdf.set_text_color(0,0,0)
                    pdf.multi_cell(0,6,line[4:])
                    pdf.ln()
            if '[Tone '+str(tone)+']' in line : okay = 1
            if '['+mark+']' in line and okay == 1 : okay = 2

# Compile canon
def printCanon(no) :
    if no == '1' : pdf.chapter_title('Kánon')
    pdf.set_font('IMFell','',12)
    pdf.set_text_color(0,0,0)
    tone = weekly
    mark = 'OD'+no
    ### Read ode from Octoechos
    okay = 0
    with open('Books/mtn_octoechos.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[T' in line :
                    pdf.set_text_color(128,0,0)
                    pdf.multi_cell(0,6,'('+line[2]+'. hang)')
                    pdf.set_text_color(0,0,0)
                    pdf.multi_cell(0,6,line[4:])
                    pdf.ln()
                if '[T' not in line and '[M]' not in line :
                    pdf.set_text_color(0,0,0)
                    pdf.multi_cell(0,6,'Dicsőség Néked Istenünk, dicsőség Néked.\n\n'+line)
                    pdf.ln()
                if '[M]' in line :
                    pdf.set_text_color(0,0,0)
                    pdf.multi_cell(0,6,'Dicsőség az Atyának és Fiúnak és Szent Léleknek most és mindenkor és mindörökkön örökké. Ámin.\n\n'+line[3:])
                    pdf.ln()
            if '[Tone '+str(tone)+']' in line : okay = 1
            if '['+mark+']' in line and okay == 1 :
                pdf.set_text_color(128,0,0)
                pdf.multi_cell(0,6,no+'. óda (a soros hang szerint)')
                okay = 2
    ### Read ode from Menaion
    okay = 0
    with open('Books/mtn_menea.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[T' in line :
                    getIrmos(line[2],no)
                    pdf.set_text_color(0,0,0)
                    pdf.multi_cell(0,6,'Dicsőség Néked Istenünk, dicsőség Néked.\n\n'+line[4:])
                    pdf.ln()
                if '[T' not in line and '[M]' not in line :
                    pdf.set_text_color(0,0,0)
                    pdf.multi_cell(0,6,'Dicsőség Néked Istenünk, dicsőség Néked.\n\n'+line)
                    pdf.ln()
                if '[M]' in line :
                    pdf.set_text_color(0,0,0)
                    pdf.multi_cell(0,6,'Dicsőség az Atyának és Fiúnak és Szent Léleknek most és mindenkor és mindörökkön örökké. Ámin.\n\n'+line[3:])
                    pdf.ln()
            if '['+menea+']' in line : okay = 1
            if '['+mark+']' in line and okay == 1 :
                pdf.set_text_color(128,0,0)
                pdf.multi_cell(0,6,no+'. óda (a ménea szerint)')
                okay = 2
    ### Read ode from Triodion
    okay = 0
    with open('Books/mtn_triodion.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[T' in line :
                    getIrmos(line[2],no)
                    pdf.set_text_color(0,0,0)
                    pdf.multi_cell(0,6,'Dicsőség Néked Istenünk, dicsőség Néked.\n\n'+line[4:])
                    pdf.ln()
                if '[T' not in line and '[M]' not in line :
                    pdf.set_text_color(0,0,0)
                    pdf.multi_cell(0,6,'Dicsőség Néked Istenünk, dicsőség Néked.\n\n'+line)
                    pdf.ln()
                if '[M]' in line :
                    pdf.set_text_color(0,0,0)
                    pdf.multi_cell(0,6,'Dicsőség az Atyának és Fiúnak és Szent Léleknek most és mindenkor és mindörökkön örökké. Ámin.\n\n'+line[3:])
                    pdf.ln()
            if '['+nomen+']' in line : okay = 1
            if '['+mark+']' in line and okay == 1 :
                pdf.set_text_color(128,0,0)
                if pretrio == True or lent == True : pdf.multi_cell(0,6,no+'. óda (a Triódion szerint)')
                if pretrio == False and lent == False : pdf.multi_cell(0,6,no+'. óda (a Pentekosztárion szerint)')
                okay = 2
    getIrmos(tone,no)
    print('    Compiled ode '+no+' of the canon.')
    return

# Compile troparia
def printTroparion() :
    pdf.chapter_title('Tropárionok')
    pdf.set_font('IMFell','',12)
    pdf.set_text_color(0,0,0)
    tone = weekly
    trp = []
    ### Read troparion from Octoechos
    okay = 0
    with open('Books/vsp_octoechos.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                trp.append(line)
            if '[Tone '+str(tone)+']' in line : okay = 1
            if '[TRP]' in line and okay == 1 : okay = 2
    ### Read troparion from Menaion
    okay = 0
    with open('Books/vsp_menea.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                trp.append(line)
            if '['+menea+']' in line : okay = 1
            if '[TRP]' in line and okay == 1 : okay = 2
    ### Read troparion from Triodion
    okay = 0
    with open('Books/vsp_triodion.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                trp.append(line)
            if '['+nomen+']' in line : okay = 1
            if '[TRP]' in line and okay == 1 : okay = 2
    # Print every troparion
    n = 0
    while n < len(trp) :
        if n == len(trp)-2 :
            pdf.set_text_color(0,0,0)
            pdf.multi_cell(0,6,'Dicsőség az Atyának és Fiúnak és Szent Léleknek')
            pdf.ln()
        if n == len(trp)-1 :
            pdf.set_text_color(0,0,0)
            pdf.multi_cell(0,6,'Most és mindenkor és mindörökkön örökké. Ámin.')
            pdf.ln()
        tone = trp[n][2]
        txt = trp[n][4:]
        pdf.set_text_color(128,0,0)
        pdf.multi_cell(0,6,'('+str(tone)+'. hang)')
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(0,6,txt)
        pdf.ln()
        n += 1
    print('    Compiled Troparia.')
    return

# Compile kontakia and ikos
def printKontakion() :
    pdf.chapter_title('Kontákionok')
    pdf.set_font('IMFell','',12)
    pdf.set_text_color(0,0,0)
    tone = weekly
    ### Read kontakion from Octoechos
    okay = 0
    with open('Books/mtn_octoechos.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 3 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                tone = line[2]
                txt = line[4:]
                pdf.set_text_color(128,0,0)
                pdf.multi_cell(0,6,'('+str(tone)+'. hang)')
                pdf.set_text_color(0,0,0)
                pdf.multi_cell(0,6,txt)
                pdf.ln()
            if okay == 3 :
                pdf.set_text_color(0,0,0)
                pdf.multi_cell(0,6,line)
                pdf.ln()
            if '[Tone '+str(tone)+']' in line : okay = 1
            if '[KNT]' in line and okay == 1 : okay = 2
            if '[IKS]' in line and okay == 2 : okay = 3
    ### Read kontakion from Menaion
    okay = 0
    with open('Books/mtn_menea.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 3 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                tone = line[2]
                txt = line[4:]
                pdf.set_text_color(128,0,0)
                pdf.multi_cell(0,6,'('+str(tone)+'. hang)')
                pdf.set_text_color(0,0,0)
                pdf.multi_cell(0,6,txt)
                pdf.ln()
            if okay == 3 :
                pdf.set_text_color(0,0,0)
                pdf.multi_cell(0,6,line)
                pdf.ln()
            if '['+menea+']' in line : okay = 1
            if '[KNT]' in line and okay == 1 : okay = 2
            if '[IKS]' in line and okay == 2 : okay = 3
    ### Read kontakion from Triodion
    okay = 0
    with open('Books/mtn_triodion.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 3 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                tone = line[2]
                txt = line[4:]
                pdf.set_text_color(128,0,0)
                pdf.multi_cell(0,6,'('+str(tone)+'. hang)')
                pdf.set_text_color(0,0,0)
                pdf.multi_cell(0,6,txt)
                pdf.ln()
            if okay == 3 :
                pdf.set_text_color(0,0,0)
                pdf.multi_cell(0,6,line)
                pdf.ln()
            if '['+nomen+']' in line : okay = 1
            if '[KNT]' in line and okay == 1 : okay = 2
            if '[IKS]' in line and okay == 2 : okay = 3
    print('    Compiled Kontakia and ikoi.')
    return

### MAIN LOOP ###
print('***************************')
print('*      GREAT MATINS       *')
print('***************************')
print(' ')
print('Lord Jesus Christ, Son of God, have mercy on us, sinners.')
print(' ')
pdf = PDF(orientation='P', unit='mm', format='A5')
nsun = getNextSunday().split()
curryear = int(nsun[2])
menea = nsun[1]+'.'+nsun[0]
weekly = getWeeklyTone()
nomen = getNominal()[0]
pretrio = getNominal()[1]
lent = getNominal()[2]
dayname = getDayName()
if dayname != '' : stitle = 'Utrenye - '+dayname
if dayname == '' : stitle = 'Utrenye - '+menea
pdf.add_font('Gothic','','Fonts/PfefferSimpelgotisch-SemiBold.ttf',True)
pdf.add_font('IMFell','','Fonts/IMFeENrm29P.ttf',True)
#pdf.set_title(title)
pdf.set_author('Servo Skull Romanos')
# Add content
print('***************************')
print('Compiling Matins for Sunday:')
pdf.add_page()
printSection('Bevezetés','Intro')
printSection('A Szent Kereszt himnuszai','Hymns of the Holy Cross')
printSection('Kis állhatatos könyörgés','Little triple litany')
printSection('A hat zsoltár','Exapsalmos')
printSection('Békességes könyörgés','Litany of Peace')
printSection('Isten az Úr','God is the Lord')
printTroparion()
printSection('Kis könyörgés','Little Litany 1')
printKathisma('Első sztichológia utáni kathizma','1ST')
printSection('Kis könyörgés','Little Litany 2')
printKathisma('Második sztichológia utáni kathizma','2ST')
printSection('Polieleosz','Polyeleos')
if pretrio == True : printSection('Babilon folyóinál','Waters of Babylon')
printSection('Feltámadási himnuszok','Hymns of Resurrection')
printSection('Kis könyörgés','Little Litany 3')
printOcto('Ypakoi','YPA','Ypakoi')
printOcto('Lépcsőének','GRD','Graduale')
printOcto('Prokimen','PRK','Prokeimenon')
printSection('Evangélium','Gospel')
printSection('Látván Krisztus feltámadását','Having Beheld')
printSection('50. zsoltár','Psalm 50')
if pretrio == True or lent == True : printSection('Bűnbánati versek','After Psalm Triodion')
if pretrio == False and lent == False : printSection('Feltámadási versek','After Psalm Sunday')
printSection('Közbenjáró imádság','Intercession')
printCanon('1')
printCanon('3')
printSection('Kis könyörgés','Little Litany 4')
printKathisma('Kánoni kathizma','KTH')
printCanon('4')
printCanon('5')
printCanon('6')
printSection('Kis könyörgés','Little Litany 5')
printKontakion()
printCanon('7')
printCanon('8')
printSection('Szűz Mária dicsérőéneke','Magnificat')
printCanon('9')
printSection('Kis könyörgés','Little Litany 6')
printKathisma('Fényének','EXA')
printSection('Dicséreti versek','Praises')
printSection('Doxológia','Doxology')
if weekly%2 == 0 : printSection('Elbocsátó tropárion','Final Troparion Even')
if weekly%2 != 0 : printSection('Elbocsátó tropárion','Final Troparion Odd')
print('***************************')
print('Building PDF.')
pdf.output('Builds/matins_'+menea.replace('.','')+'.pdf')
print('    The machine spirit is willing.')
print('***************************')
print('Glory to Thee oh Lord, glory to Thee.')
