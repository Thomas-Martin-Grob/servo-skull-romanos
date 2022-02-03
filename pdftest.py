from fpdf import FPDF
# Page design elements
class PDF(FPDF):
    def header(self):
        self.set_font('IMFell','',10)
        w = self.get_string_width(stitle) + 6
        self.set_x((150 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w,9,stitle,1,1,'C',1)
        # Line break
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('IMFell','',10)
        self.set_text_color(0,0,0)
        self.cell(0,10,str(self.page_no()),0,0,'C')

    def chapter_title(self,label):
        self.set_font('Gothic','',16)
        self.set_text_color(128,0,0)
        self.cell(0,7,label,0,1,'C')
        self.ln(4)

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
    txt = readSection('Books/vcs_horologion.txt',section).split('[')
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
    return

# Compile 'Lord I call'
def printLordICall() :
    tone = 1
    date = '02.03'
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
    'Most és mindenkor és mindörökön örökké. Ámin.']
    ### Print intro
    printSection('Uram Tehozzád kiáltottam','Lord I Call',tone)
    ### Read verses from Octoechos
    okay = False
    n = 0
    with open('Books/lic_octoechos.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if okay == True and '[/]' in line :
                break
            if okay == True :
                if '[D]' in line : verses[10] = line[3:]
                if '[M]' in line : verses[11] = line[3:]
                if '[D]' not in line and '[M]' not in line :
                    verses[n] = line
                    n += 1
            if '[Tone '+str(tone)+']' in line : okay = True
    ### Read verses from Menaion
    okay = False
    mvers = []
    with open('Books/lic_menea.txt','rb') as file :
        while True :
            line = file.readline().decode('utf8')
            if not line :
                break
            if okay == True and '[/]' in line :
                break
            if okay == True :
                if '[D]' in line : verses[10] = line[3:]
                if '[M]' in line : verses[11] = line[3:]
                if '[D]' not in line and '[M]' not in line :
                    mvers.append(line)
            if '['+date+']' in line : okay = True
    m = 10-len(mvers)
    n = 0
    while m < 10 :
        verses[m] = mvers[n]
        n += 1
        m += 1
    ### Print the compiled verses
    n = 0
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
    return

### MAIN LOOP ###
pdf = PDF(orientation='P', unit='mm', format='A5')
stitle = 'Vecsernye'
pdf.add_font('Gothic','','PfefferSimpelgotisch-SemiBold.ttf',True)
pdf.add_font('IMFell','','IMFeENrm29P.ttf',True)
#pdf.set_title(title)
pdf.set_author('Servo Skull Romanos')
# Add content
pdf.add_page()
printSection('Bevezetés','Intro')
printSection('103. zsoltár','Psalm 103')
printSection('Békességes ekténia','Litany of Peace')
printSection('Boldog az a férfiú','Blessed Is the Man')
printLordICall()
printSection('Derűs világossága','Joyful Light')
pdf.output('test.pdf')