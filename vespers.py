###########################################
# This script compiles texts for vespers. #
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
    return nom

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
    txt = readSection('Books/vsp_horologion.txt',section).split('[')
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

# Compile Aposticha
def printAposticha() :
    pdf.chapter_title('Aposzticha')
    pdf.set_font('IMFell','',12)
    pdf.set_text_color(0,0,0)
    tone = weekly
    verses = ['','','','','','','']
    post = ['','','','','Dicsőség az Atyának és Fiúnak és Szent Léleknek.','Most és mindenkor és mindörökkön örökké. Ámin.','']
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
                if '[D]' in line : verses[5] = line[3:]
                if '[M]' in line : verses[6] = line[3:]
                if '[E]' in line :
                    post[n] = line[3:]
                    n += 1
                if '[D]' not in line and '[M]' not in line and not '[E]' in line :
                    verses[n] = line
            if '[Tone '+str(tone)+']' in line : okay = 1
            if '[APO]' in line and okay == 1 : okay = 2
    ### Reset verses if there is a full aposticha in Menaion
    okay = 0
    with open('Books/vsp_menea.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 and '[T' in line[0:2] :
                verses = ['','','','','','','']
                post = ['','','','','Dicsőség az Atyának és Fiúnak és Szent Léleknek.','Most és mindenkor és mindörökkön örökké. Ámin.','']
                break
            if '['+menea+']' in line : okay = 1
            if '[APO]' in line and okay == 1 : okay = 2
    ### Read verses from Menaion
    okay = 0
    n = 0
    with open('Books/vsp_menea.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[D]' in line : verses[5] = line[3:]
                if '[M]' in line : verses[6] = line[3:]
                if '[E]' in line :
                    post[n] = line[3:]
                    n += 1
                if '[D]' not in line and '[M]' not in line and not '[E]' in line :
                    verses[n] = line
            if '['+menea+']' in line : okay = 1
            if '[APO]' in line and okay == 1 : okay = 2
    ### Reset verses if there is a full aposticha in Triodion
    okay = 0
    with open('Books/vsp_triodion.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 and '[T' in line[0:2] :
                verses = ['','','','','','','']
                post = ['','','','','Dicsőség az Atyának és Fiúnak és Szent Léleknek.','Most és mindenkor és mindörökkön örökké. Ámin.','']
                break
            if '['+nomen+']' in line : okay = 1
            if '[APO]' in line and okay == 1 : okay = 2
    ### Read verses from Triodion
    okay = 0
    n = 0
    with open('Books/vsp_triodion.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                if '[D]' in line : verses[5] = line[3:]
                if '[M]' in line : verses[6] = line[3:]
                if '[E]' in line :
                    post[n] = line[3:]
                    n += 1
                if '[D]' not in line and '[M]' not in line and not '[E]' in line :
                    verses[n] = line
            if '['+nomen+']' in line : okay = 1
            if '[APO]' in line and okay == 1 : okay = 2
    ### Compile verses
    n = 0
    oldtone = 0
    tone = 0
    while n < len(verses) :
        #print('Verse: '+verses[n])
        #print('Post: '+post[n])
        if '[T' in verses[n] :
            oldtone = tone
            tone = int(verses[n][2])
            verses[n] = verses[n][4:]
        if oldtone == tone :
            txt = verses[n]
            if len(post[n]) > 3 : txt += '\n'+post[n]
            if len(txt) > 3 :
                pdf.multi_cell(0,6,txt)
                pdf.ln()
        if oldtone != tone :
            pdf.set_text_color(128,0,0)
            pdf.multi_cell(0,6,'('+str(tone)+'. hang)')
            pdf.set_text_color(0,0,0)
            txt = verses[n]
            if len(post[n]) > 3 : txt += '\n\n'+post[n]
            if len(txt) > 3 :
                pdf.multi_cell(0,6,txt)
                pdf.ln()
            oldtone = tone
        n += 1
    print('    Compiled Aposticha.')
    return

# Compile troparia and theotokion
def printTroparion() :
    pdf.chapter_title('Tropárionok')
    pdf.set_font('IMFell','',12)
    pdf.set_text_color(0,0,0)
    tone = weekly
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
                tone = line[2]
                txt = line[4:]
                pdf.set_text_color(128,0,0)
                pdf.multi_cell(0,6,'('+str(tone)+'. hang)')
                pdf.set_text_color(0,0,0)
                pdf.multi_cell(0,6,txt)
                pdf.ln()
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
                tone = line[2]
                txt = line[4:]
                pdf.set_text_color(128,0,0)
                pdf.multi_cell(0,6,'('+str(tone)+'. hang)')
                pdf.set_text_color(0,0,0)
                pdf.multi_cell(0,6,txt)
                pdf.ln()
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
                tone = line[2]
                txt = line[4:]
                pdf.set_text_color(128,0,0)
                pdf.multi_cell(0,6,'('+str(tone)+'. hang)')
                pdf.set_text_color(0,0,0)
                pdf.multi_cell(0,6,txt)
                pdf.ln()
            if '['+nomen+']' in line : okay = 1
            if '[TRP]' in line and okay == 1 : okay = 2
    ### Read troparion of the church
    okay = False
    with open('Books/trp_church.txt','rb') as file :
        line = file.readline().decode('utf8')
        tone = line[2]
        txt = line[4:]
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(0,6,'Dicsőség az Atyának és Fiúnak és Szent Léleknek.')
        pdf.ln()
        pdf.set_text_color(128,0,0)
        pdf.multi_cell(0,6,'('+str(tone)+'. hang)')
        pdf.set_text_color(0,0,0)
        pdf.multi_cell(0,6,txt+'\n\nMost és mindenkor és mindörökkön örökké. Ámin.')
        pdf.ln()
    ### Read theotokion from Octoechos
    tone = weekly
    okay = 0
    with open('Books/vsp_octoechos.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if (okay == 2 and '[/]' in line) or (okay > 0 and '[//]' in line) :
                break
            if okay == 2 :
                tone = line[2]
                txt = line[4:]
                pdf.set_text_color(128,0,0)
                pdf.multi_cell(0,6,'('+str(tone)+'. hang)')
                pdf.set_text_color(0,0,0)
                pdf.multi_cell(0,6,txt)
                pdf.ln()
            if '[Tone '+str(tone)+']' in line : okay = 1
            if '[THT]' in line and okay == 1 : okay = 2
    print('    Compiled Troparia.')
    return

### MAIN LOOP ###
print('***************************')
print('*      GREAT VESPERS      *')
print('***************************')
print(' ')
print('Lord Jesus Christ, Son of God, have mercy on us, sinners.')
print(' ')
pdf = PDF(orientation='P', unit='mm', format='A5')
nsun = getNextSunday().split()
curryear = int(nsun[2])
menea = nsun[1]+'.'+nsun[0]
weekly = getWeeklyTone()
nomen = getNominal()
dayname = getDayName()
if dayname != '' : stitle = 'Vecsernye - '+dayname
if dayname == '' : stitle = 'Vecsernye - '+menea
pdf.add_font('Gothic','','Fonts/PfefferSimpelgotisch-SemiBold.ttf',True)
pdf.add_font('IMFell','','Fonts/IMFeENrm29P.ttf',True)
#pdf.set_title(title)
pdf.set_author('Servo Skull Romanos')
# Add content
print('***************************')
print('Compiling Vespers for Sunday:')
pdf.add_page()
printSection('Bevezetés','Intro')
printSection('103. zsoltár','Psalm 103')
printSection('Békességes könyörgés','Litany of Peace')
printSection('Boldog az a férfiú','Blessed Is the Man')
printSection('Kis könyörgés','Little Litany')
printLordICall()
printSection('Derűs világossága','Joyful Light')
printSection('Prokimen','Prokeimenon')
printSection('Állhatatos könyörgés','Triple Litany')
printSection('Add Urunk','Vouchsafe O Lord')
printSection('Kérő könyörgés','Litany of Supplication')
printAposticha()
printSection('Most bocsásd el','Now Lettest')
printSection('Háromszorszent','Trisagion')
printTroparion()
printSection('Elbocsátás','Dismissal')
print('***************************')
print('Building PDF.')
pdf.output('Builds/vespers_'+menea.replace('.','')+'.pdf')
print('    The machine spirit is willing.')
print('***************************')
print('Glory to Thee oh Lord, glory to Thee.')
