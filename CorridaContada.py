# Corrida Contada - Edição Python
import pygame, time, random, os, threading
_lock = threading.Lock()
mainClock = pygame.time.Clock()

# Configurações da tela - Roubado do PythonFigther
pygame.init()
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 360
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Corrida Contada Remake")

# Configuração de áudio - Roubado do PythonFighter
pygame.mixer.init()
pygame.mixer.music.load("music/intro.mp3")  # .mp3/.wav
pygame.mixer.music.set_volume(0.1)  # Volume entre 0.0 e 1.0
pygame.mixer.music.play(-1)  # -1 = loop infinito

class MathGenerationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Timer:
    def __init__(self, isInfinite, objective):
    # Creates a clock that can count up or down.
    # isInfinite is the flag to set up a cronometer.
    # objective is the offset in seconds from the current timestamp
    
        self.shouldCount = isInfinite
        if isInfinite:
            self.start = time.time()
        else:
            Time = time.time()
            self.end = Time + objective
    
    def update(self):
        Time = time.time()
        if self.shouldCount:
            self.current = Time - self.start
        else:
            self.current = self.end - Time
            return Time>=self.end # If the objective is met, return True!
            
    def get(self):
        timestamp = round(self.current*100)/100 # Truncates the Timestamp down to 2 decimal digits
        down_timestamp = str(timestamp).split('.')
        dec_timestamp = int(down_timestamp[1]) # Gets the truncated decimal part of the timestamp
        down_timestamp = int(down_timestamp[0]) # Gets the integer part of the timestamp
        
        ms = str(int(dec_timestamp))
        sec = str(down_timestamp % 60) # Modules the timestamp with 60. Resulting in a number from 0 to 59.
        down_min = str(down_timestamp/60).split('.')
        min = str(int(down_min[0]) % 60) # Gets the integer part of the "minutestamp"
        
        # Avoid 1-digit numbers:
        if len(ms) < 2:
            ms = "0" + str(ms)
        if len(sec) < 2:
            sec = "0" + str(sec)
        if len(min) < 2:
            min = "0" + str(min)
        
        return f"{min}'{sec}''{ms}" # Should be MM'SS''MS
    
class Math: # Note to self: this can nuke the frikin' computer with a bad setting
    def gen_core(op, ops, n_range):
        # op = Number of operators
        # ops = What operators should be used
        # n_range = Minium and Maxium value. ex: n_range = 500, the range is -250 to 250.
        
        global Equation, Result
        Equation = "" # Initiating variable.
        
        eq = [random.randint(-n_range, n_range)]
        if eq[0]<0:
            Equation = "(" + str(eq[0]) + ") "
        else:
            Equation = str(eq[0]) + " "
        num = 1
        while num<=op: # Equation Generator
            
            operator = ops[random.randint(0, len(ops)-1 ) ]
            num2 = random.randint(-n_range, n_range)
            
            if num2<0:
                Equation = Equation + operator + " (" + str(num2) + ") "
            else:
                Equation = Equation + operator + " " + str(num2) + " "
            
            eq.append(operator)
            eq.append(num2)
                
            num += 1
        
        # Get answer
        Equation = Equation.strip()
        try:
            Result = eval(Equation) # Since this doesn't run untrusted code, why not use it?
            if str(Result)[-2:] == ".0": # From a non-programmer POV, it's redundant, but from a programmer POV it's completly diffrent things.
                Result = round(Result)
        except ZeroDivisionError:
                Result = "ZeroDivisionError"
        Equation = Equation.replace("/",":") # My teachers prefer ":" as the symbol for divison.
        Equation = Equation.replace("*","x") # Same logic for "x" as the symbol for multiplication.
    
    def gen(op, ops, nrange):
        # Tries to avoid Zero divisions, big decimal and big integer numbers.
        IsInvalidNumber = True
        tryID = 0
        print("-- MathGen System ---")
        print(f"Current configuration:\n {MathGen[0]+1} Numbers / {MathGen[1]} Valid Operators / {MathGen[2]} Range.")
        if MathGen[0]>6:
            print("Unstable Territory! Too much operations!")
        if MathGen[0]>999:
            print("Unstable Territory! Big numbers!")
        while IsInvalidNumber and tryID<1000:
            print(f"Generating Equation #{tryID}")
            Math.gen_core(MathGen[0],MathGen[1],MathGen[2])
            IsInvalidNumber = Result == "ZeroDivisionError"
            if not IsInvalidNumber:
                number = str(Result).split(".")
                try:
                    if eqs<20:
                        if len(number[1])>0:
                            IsInvalidNumber = True
                            print(f"Has Decimal! : {Result}")
                    else:
                        if len(number[1])>3:
                            IsInvalidNumber = True
                            print(f"Big Decimal! : {Result}")
                        
                except IndexError:
                    IsInvalidNumber = False
                if eqs<20:
                    if len(number[0])>3:
                        IsInvalidNumber = True
                        print(f"Big Integer! : {Result}")
                else:
                    if len(number[0])>4:
                        IsInvalidNumber = True
                        print(f"Big Integer! : {Result}")
            else:
                print("ZeroDivisionError!")
            tryID +=1
            
        
        if tryID>999:
            raise MathGenerationError("Could not generate a valid expression in 1000 tries.")
        else:
            print("Equation Generated!")

def display(size, text, color, pos):
    screen.blit(pygame.font.Font(None, size).render(text, True, color), pos)

#Splash Screen
logoCC = pygame.image.load(f"images/logo.png").convert_alpha()
logoCC = pygame.transform.scale(logoCC, (300, 220))
logoCC_rect = logoCC.get_rect(center=(SCREEN_WIDTH/2,120))
welcome = pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 26).render(f"< PRESS ENTER >", True, (255,255,255))
welcome_rect = welcome.get_rect(center=(SCREEN_WIDTH/2, 320))
DT = 0
FPS = 69
fpsAvgInstant = 60
ShellLikeTextIndicatorFlashTime = 0
StopRunning = False
while not StopRunning:
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
                StopRunning = True
            
            if event.key == pygame.K_PAGEUP:
                vol = min(pygame.mixer.music.get_volume() + 0.05, 1.0)
                pygame.mixer.music.set_volume(vol)
                
            if event.key == pygame.K_PAGEDOWN:
                vol = max(pygame.mixer.music.get_volume() - 0.05, 0.05) # Avoid the music to be stopped.
                pygame.mixer.music.set_volume(vol)
                
    if ShellLikeTextIndicatorFlashTime%30<15:
        screen.blit(welcome,welcome_rect)
    screen.blit(logoCC, logoCC_rect)
    
    if DT>0:
        FPS = 1000/DT
        
    fpsAvgInstant = (fpsAvgInstant + FPS) /2
    #display(20, f"FPS: {round(FPS)}fps / {DT}ms / {round(fpsAvgInstant)}avg", (255,255,255),(0,200))
    pygame.display.flip()
    DT = mainClock.tick(60)
    ShellLikeTextIndicatorFlashTime += 1
    
StopRunning = False
EnterPress = 0
confirm = pygame.font.Font("fonts/Octarine.otf", 22).render(f"Did you actually read it?", True, (255,255,255))
confirm_rect = confirm.get_rect(center=(SCREEN_WIDTH/2, 335))
title = pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 30).render(f"How to play", True, (255,255,255))
title_rect = title.get_rect(center=(SCREEN_WIDTH/2, title.get_height()/2+2))
while not StopRunning:
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
                EnterPress += 1
                
            if event.key == pygame.K_PAGEUP:
                vol = min(pygame.mixer.music.get_volume() + 0.05, 1.0)
                pygame.mixer.music.set_volume(vol)
                
            if event.key == pygame.K_PAGEDOWN:
                vol = max(pygame.mixer.music.get_volume() - 0.05, 0.05) # Avoid the music to be stopped.
                pygame.mixer.music.set_volume(vol)
    
    screen.blit(title, title_rect)
    display(20, f"""
    
    Corrida Contada Remake is a game about math (if you didn't notice). 
    The game's objective is to do 20 math equations in less than 5 minutes.
    Your Rank is based off EquaPoints. Get the answer right and quickly for
    a bunch of EquaPoints. If you miss, you LOSE EquaPoints.
    
    The game gets progressively harder as you get more answers right.
    Do note that equations can contain:
        + Addition            ex: 10 + (-5)
        - Subtraction        ex: 9 - 2
        : Divison              ex: 12 - (-3) / 2
        x Multiplication    ex: 17 x 9
    
    If you're quick enough, you can enter the Bonus Mode for extra 
    EquaPoints, but at what cost?
    
    """, (255,255,255), (-9,0))
    
    if EnterPress==1:
        screen.blit(confirm,confirm_rect)
    if EnterPress>1:
        StopRunning = True
    
    if ShellLikeTextIndicatorFlashTime%30<15:
        screen.blit(welcome,welcome_rect)
    
    if DT>0:
        FPS = 1000/DT
        
    fpsAvgInstant = (fpsAvgInstant + FPS) /2
    #display(20, f"FPS: {round(FPS)}fps / {DT}ms / {round(fpsAvgInstant)}avg", (255,255,255),(0,200))
    pygame.display.flip()
    DT = mainClock.tick(60)
    ShellLikeTextIndicatorFlashTime += 1


screen.fill((0,0,0))
loadin = pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 32).render(f"Loading...", True, (255,255,255))
loadin_rect = loadin.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
subtitleload = pygame.font.Font("fonts/Octarine.otf", 26).render(f"Waiting fadeout operation to end...", True, (255,255,255))
subtitleload_rect = subtitleload.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+20))
screen.blit(loadin,loadin_rect)
screen.blit(subtitleload,subtitleload_rect)
pygame.display.flip()
pygame.mixer.music.fadeout(1000)
pygame.mixer.music.load("music/speedrunning.mp3") # This is actually Dream Speedrunning music. 5 minutes and 21 seconds long. PERFECT!
pygame.mixer.music.play()

global MathGen
MathGen = [1, "+-", 20]

eqs = 0
StopRunning = False
USERINPUT = ""
suggest = "-"
EquaRanks = {"T":-1, "F":0, "D":0.15, "C":0.4, "B":0.6, "A":0.8, "S":1, "S+":1.3, "SS":1.6, "SS+":2, "SSS":3.5, "SSS+":5}
EquaRank = "T"
feedback = 0
feedback_ticks = 0
ShellLikeTextIndicatorFlashTime = 0
CurrentEquation = 0
Combo = 0
EquaPoints = 0
Math.gen(MathGen[0],MathGen[1],MathGen[2])
EquaPointLimiter = 33150 # This is actually the maxium value you can get... without entering Bonus Mode.
oldEquation = "-69"
previousTime = 300
diff = 0
Down = Timer(False,300)
while not StopRunning:
    StopRunning = Down.update()
    
    screen.fill((0,0,0)) # Epic frame refresher
    if oldEquation != Equation:
        EquaRenderSize = 35
        EquaRenderWidth = 999
        while EquaRenderWidth>SCREEN_WIDTH:
            EquaRender = pygame.font.Font(None, EquaRenderSize).render(f"{Equation} = ?", True, (255,255,255))
            EquaRenderWidth = EquaRender.get_width()
            EquaRenderSize -= 1
        oldEquation = Equation
    screen.blit(EquaRender, (0,0))
    display(32,f">{USERINPUT}{"_" if ShellLikeTextIndicatorFlashTime % 30 < 15 else ""}", (255, 255, 255), (0,40))
    if CurrentEquation==0:
        eqscorinfofont_surf = pygame.font.Font("fonts/Octarine.otf", 15).render("0 Wrong / 0 Right / 0% Accuracy", True, (255,255,255))
    else:
        eqscorinfofont_surf = pygame.font.Font("fonts/Octarine.otf", 15).render(f"{CurrentEquation - eqs} Wrong / {eqs} Right / {round(eqs/CurrentEquation*100)}% Accuracy", True, (255,255,255))
        
    for rank, score in sorted(EquaRanks.items(), key=lambda x: x[1]):
        if EquaPoints/EquaPointLimiter > score:
            EquaRank = rank
    
    # Making Right-To-Left text (cuz why not?)
    eqscorfont_surf = pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 50).render(EquaRank, True, (255,255,255)) 
    eqscorindfont_surf = pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 25).render("RANK", True, (255,255,255)) 
    EquaScoreTxT = pygame.font.Font(None, 25).render(f"{round(EquaPoints)} EP", True, (255,255,255)) 
    screen.blit(eqscorinfofont_surf, (SCREEN_WIDTH - eqscorinfofont_surf.get_width() - 10, 286))
    screen.blit(EquaScoreTxT, (SCREEN_WIDTH - EquaScoreTxT.get_width() - 10, 301))
    screen.blit(eqscorfont_surf, (SCREEN_WIDTH - eqscorfont_surf.get_width() - 10, 320))
    screen.blit(eqscorindfont_surf, (SCREEN_WIDTH - eqscorfont_surf.get_width() - eqscorindfont_surf.get_width() - 13, 330))
    
    #display(20, f"CHEAT: {Result}", (255,255,255), (0,150))
    if Combo>1:
        if ShellLikeTextIndicatorFlashTime%10<5:
            screen.blit(pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 25).render(f"x{Combo} COMBO!", True, (255,255,255)), (0,260))
        else:
            if eqs>19:
                screen.blit(pygame.font.Font("fonts/Octarine.otf", 25).render(f"BONUS TIME!!", True, (255,200,0)), (0,260))
            
    color = (255, 0, 0) if Down.current < 60 else (255, 255, 255)
    if Down.current>=60 or ShellLikeTextIndicatorFlashTime%30<15:
        screen.blit(pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 23).render(f"{Down.get()}", True, color), (0,335))

    
    if feedback_ticks>0:
        if feedback == -1:
            screen.blit(pygame.font.Font(None, 20).render(f"THAT'S WRONG!", True, (255, 0, 0)), (0,220)) 
        if feedback == 1:
            screen.blit(pygame.font.Font(None, 20).render(f"THAT'S RIGHT!", True, (0, 255, 0)), (0,220))
        feedback_ticks -= 1
    else:
        feedback = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            StopRunning = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                StopRunning = True
            
            if event.key == pygame.K_PAGEUP:
                vol = min(pygame.mixer.music.get_volume() + 0.05, 1.0)
                pygame.mixer.music.set_volume(vol)
                
            if event.key == pygame.K_PAGEDOWN:
                vol = max(pygame.mixer.music.get_volume() - 0.05, 0.05) # Avoid the music to be stopped.
                pygame.mixer.music.set_volume(vol)
            
            # Input
            
            if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                USERINPUT = USERINPUT + "0"
                # EquaPoints = 168000 # Cheetaahh!!
            
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                USERINPUT = USERINPUT + "1"
            
            if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                USERINPUT = USERINPUT + "2"
            
            if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                USERINPUT = USERINPUT + "3"
            
            if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                USERINPUT = USERINPUT + "4"
            
            if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                USERINPUT = USERINPUT + "5"
            
            if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                USERINPUT = USERINPUT + "6"
            
            if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                USERINPUT = USERINPUT + "7"
            
            if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                USERINPUT = USERINPUT + "8"
            
            if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                USERINPUT = USERINPUT + "9"
                
            if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                USERINPUT = USERINPUT + "-"
                
            if event.key == pygame.K_SLASH or event.key == pygame.K_KP_DIVIDE:
                USERINPUT = USERINPUT + "/" # For fractions (ex 1/3, so the user doesnt need to type 0.333333333333333333...)
                
            if event.key == pygame.K_PERIOD or event.key == pygame.K_KP_PERIOD:
                USERINPUT = USERINPUT + "." # Maybe we get decimals. Who knows?
            
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if suggest != "-":
                    USERINPUT = suggest
                if USERINPUT == str(Result):
                    eqs += 1
                    print("User got the answer right")
                    feedback = 1
                    MathGen[2] += 10
                    if eqs%10 == 0:
                        if MathGen[0]<8: # Avoid MASSIVE expressions that is very hard to calculate.
                            MathGen[0] += 1
                    if eqs%6 == 0:
                        if not "*" in MathGen[1]:
                            MathGen[1] = MathGen[1] + "*" # This fella and...
                        elif not "/" in MathGen[1]:
                            MathGen[1] = MathGen[1] + "/" # ... This fella makes the generator go KABUM.
                    Combo += 1
                    diff = previousTime-Down.current
                    if diff<5:
                        EquaPoints += 1500 * ((Combo-1)/100+1)
                        print(f"+{1500 * ((Combo-1)/100+1)} = {EquaPoints}")
                    elif diff<15:
                        EquaPoints += 750 * (Combo/100+1)
                        print(f"+{750 * ((Combo-1)/100+1)} = {EquaPoints}")
                    else:
                        EquaPoints += 300 * (Combo/100+1)
                        print(f"+{300 * ((Combo-1)/100+1)} = {EquaPoints}")
                else:
                    EquaPoints -= 600 # I know that the player can have -690000000 score.
                    print("User got the answer wrong")
                    print(f"-{600} = {EquaPoints}")
                    feedback = -1
                    Combo = 0
                print(f"Answered in {diff}s!")
                feedback_ticks = 30
                CurrentEquation += 1
                USERINPUT = ""
                Math.gen(MathGen[0],MathGen[1],MathGen[2])
                previousTime = Down.current
            try:
                if event.key == pygame.K_BACKSPACE:
                    USERINPUT = USERINPUT[:-1]
            except:
                USERINPUT = ""
    if "/" in USERINPUT:
        userfract = USERINPUT.split("/")
        try:
            suggest = int(userfract[0])/int(userfract[1])
            screen.blit(pygame.font.Font(None, 20).render(f"Considering your answer as {suggest}", True, (255, 255, 255)), (0,60))
        except Exception as e:
            print(e)
            suggest = "-"
            
    # USERINPUT = str(Result) # cheetahh!11
    
    if DT>0:
        FPS = 1000/DT
    fpsAvgInstant = (fpsAvgInstant + FPS) /2
    #display(20, f"FPS: {round(FPS)}fps / {DT}ms / {round(fpsAvgInstant)}avg", (255,255,255),(0,200))
    pygame.display.flip()
    DT = mainClock.tick(60)
    ShellLikeTextIndicatorFlashTime += 1

screen.fill((0,0,0))
screen.blit(loadin,loadin_rect)
screen.blit(subtitleload,subtitleload_rect)
pygame.display.flip()
pygame.mixer.music.fadeout(1000)
if eqs>19:
    pygame.mixer.music.load("music/bronzeLicense.mp3") # This is actually GT4's Bronze License music.
else:
    pygame.mixer.music.load("music/gameOver.mp3") # This is actually Sonic CD's Japanese Game Over song.
pygame.mixer.music.play()

title = pygame.font.Font("fonts/Octarine.otf", 30).render(f"Game Over!", True, (255,90,0))
title_rect = title.get_rect(center=(SCREEN_WIDTH/2, title.get_height()/2+3))
SmoothEPIncreaser = 0
epSuf = pygame.font.Font(None, 25).render("EquaPoints", True, (255,255,255))
epSuf_rect = epSuf.get_rect(midleft=(10, SCREEN_HEIGHT/4+12))
RankNames = {
    "T":"Terrible", 
    "F":"Failure", 
    "D":"Decent", 
    "C":"Cool", 
    "B":"Better", 
    "A":"Amazing!", 
    "S":"Splendid!", 
    "S+":"Premium Splendid!!",
    "SS":"Super Splendid!!", 
    "SS+":"Premium Super Splendid!!!", 
    "SSS":"Stupidly Super Splendid!!!", 
    "SSS+":"Premium Stupidly Super Splendid!!!!"
}
RankColors = {
    "T":(175, 33, 33),
    "F":(255, 31, 47),
    "D":(255, 113, 47),
    "C":(255, 170, 85),
    "B":(178, 255, 74),
    "A":(0, 255, 97),
    "S":(232, 255, 66),
    "S+":(255, 255, 124),
    "SS":(255, 170, 163),
    "SS+":(255, 105, 178),
    "SSS":(151, 113, 209),
    "SSS+":(105, 167, 255)
}
RankName = "Terrible"
StopRunning = False
logoCC = pygame.transform.scale(logoCC, (200, 146))
logoCC_rect = logoCC.get_rect(midright=(SCREEN_WIDTH-20,120))
while not StopRunning:
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
                StopRunning = True
    for rank, score in sorted(EquaRanks.items(), key=lambda x: x[1]):
        if SmoothEPIncreaser/33150 > score:
            EquaRank = rank
            RankName = RankNames[rank]
            RankColor = RankColors[rank]
    
    point = pygame.font.Font("fonts/Octarine.otf", 25).render(str(round(SmoothEPIncreaser*100)/100), True, (255,255,255))
    point_rect = point.get_rect(midleft=(10, SCREEN_HEIGHT/4))
    rank = pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 25).render(f"Rank {EquaRank}", True, RankColor)
    rank_rect = rank.get_rect(midleft=(10, SCREEN_HEIGHT/2))
    rankName = pygame.font.Font(None, 25).render(RankName, True, RankColor)
    rankName_rect = rankName.get_rect(midleft=(10, SCREEN_HEIGHT/2+12))
    
    screen.blit(title, title_rect)
    screen.blit(point, point_rect)
    screen.blit(epSuf, epSuf_rect)
    screen.blit(rank, rank_rect)
    screen.blit(rankName, rankName_rect)
    screen.blit(logoCC, logoCC_rect)
    
    SmoothEPIncreaser += (EquaPoints-SmoothEPIncreaser)/20
    
    if ShellLikeTextIndicatorFlashTime%30<15:
        screen.blit(welcome,welcome_rect)
    
    if DT>0:
        FPS = 1000/DT
        
    fpsAvgInstant = (fpsAvgInstant + FPS) /2
    #display(20, f"FPS: {round(FPS)}fps / {DT}ms / {round(fpsAvgInstant)}avg", (255,255,255),(0,200))
    pygame.display.flip()
    DT = mainClock.tick(60)
    ShellLikeTextIndicatorFlashTime += 1