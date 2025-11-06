# Corrida Contada - Edição Python
import pygame, time, random, os, sys
mainClock = pygame.time.Clock()

# Configurações da tela - Roubado do PythonFigther
pygame.init()
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 360
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Corrida Contada Remake")

ABORT_CODE_EXECUTION = False
# English / Portuguese toggle.
PRESS_ENTER = "< PRESS ENTER >"
MENU_CONFIRM_READ = "Did you actually read it?"
TUTORIAL_HOWTO = "How to play"
TUTORIAL_TEXT = """

    Corrida Contada Remake is a game about math (if you didn't notice). 
    The game's objective is to do at least 20 math equations in 5 minutes.
    
    Your Rank is based off EquaPoints. Get the answer right and quickly for
    a bunch of EquaPoints. If you miss, you LOSE EquaPoints.
    
    The game gets progressively harder as you get more answers right.
    Do note that equations can contain:
        + Addition            ex: 10 + (-5)
        - Subtraction        ex: 9 - 2
        : Divison              ex: 12 - (-3) / 2
        x Multiplication    ex: 17 x 9
    
    If you're quick enough, you can enter the Bonus Mode for extra 
    EquaPoints, but do note that the game gets hard instantly.

"""
LOADING = "Loading..."
LOADING_SUBTEXT = "Waiting 'fadeout' operation to end..."
HUD_WRONG = "Wrong"
HUD_RIGHT = "Right"
HUD_ACCURACY = "Accuracy"
BONUS_TIME = "BONUS TIME!!"
CORRECT_ANSWER = "Nice answer!"
WRONG_ANSWER = "Wrong answer buddy!"
ANSWER_SUGGESTION = "Considering your answer as"
GAMER_OVER = "GAMER OVER!"
EQUAPOINTS = "EquaPoints"
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
NEW_RECORD = "NEW RECORD!"
COMBO_RECORD_BEAT = "Combo to beat"
if len(sys.argv)>1:
    if sys.argv[1]=="--pt-br":
        PRESS_ENTER = "< TECLE ENTER >"
        MENU_CONFIRM_READ = "Você realmente leu?"
        TUTORIAL_HOWTO = "Como Jogar"
        TUTORIAL_TEXT = """
    
    Corrida Contada Remake é um jogo sobre matemática. 
    O objetivo do jogo é fazer pelo menos 20 equações em 5 minutos.
    
    Seu Rank é baseado em EquaPontos. Ache a resposta certa rapidamente 
    e ganhe um monte de EquaPontos. Se errar, você PERDE EquaPontos.
    
    A Cada equação respondida corretamente, o jogo fica cada vez mais difí-
    cil. Saiba que as equações poderam ter:
        + Adição              ex: 10 + (-5)
        - Subtracão          ex: 9 - 2
        : Divisão              ex: 12 - (-3) / 2
        x Multiplicação     ex: 17 x 9
    
    Se for rápido suficiente, podes entrar no Modo Bônus para EquaPontos
    extras, mas saiba que o jogo complica de uma vez.
    
    """
        LOADING = "Carregando..."
        LOADING_SUBTEXT = "Esperando o 'fadeout' acabar..."
        HUD_WRONG = "Erros"
        HUD_RIGHT = "Acertos"
        HUD_ACCURACY = "de Acerto"
        BONUS_TIME = "HORA DO BÔNUS!!"
        CORRECT_ANSWER = "Acertou!"
        WRONG_ANSWER = "Errou, parçeiro!"
        ANSWER_SUGGESTION = "Considerando sua resposta como"
        GAMER_OVER = "FIM DE JOGO!"
        EQUAPOINTS = "EquaPontos"
        RankNames = {
            "T":"Terrível", 
            "F":"Fracasso", 
            "D":"Decente", 
            "C":"Competente", 
            "B":"Bombástico", 
            "A":"Ágil!", 
            "S":"Sábio!", 
            "S+":"Sábio Premium!!",
            "SS":"Super Sábio!!", 
            "SS+":"Super Sábio Premium!!!", 
            "SSS":"Stupidamente Super Sábio!!!", 
            "SSS+":"Stupidamente Super Sábio Premium!!!!"
        }
        NEW_RECORD = "NOVO RECORDE!"
        COMBO_RECORD_BEAT = "de Combo é o recorde"

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
            
            if len(str(eq[num-1]))>2:
                operator = ops[random.randint(0, 1) ]
            else:
                operator = ops[random.randint(0, len(ops)-1) ]
            if operator == "*":
                num2 = random.randint(-10, 10)
            elif operator == "/":
                num2 = random.randint(-20, 20)
                if num2==0:
                    num2=-1
            else:
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
    
    def gen():
        # Tries to avoid Zero divisions, big decimal and big integer numbers and hard to solve equations.
        diff = min(eqs//5, 10)
        
        numrange = 10 + diff*5
        n_operators = 1 + diff//2
        
        operators = "+-"
        if eqs>20:
            operators = "+-*/"
        elif eqs>10:
            operators = "+-*"
        
        IsInvalid = True
        while IsInvalid:
            Math.gen_core(n_operators, operators, numrange)
            if Result != "ZeroDivisionError":
                if not "." in str(Result):
                    IsInvalid = False

def display(size, text, color, pos):
    screen.blit(pygame.font.Font(None, size).render(text, True, color), pos)

def reload():
    # Pre-load all stuff
    global BSOD, logoCC_raw, logoCC, logoCC_rect, logoCC1, logoCC1_rect, welcome, welcome_rect, ShellLikeTextIndicatorFlashTime, EnterPress, confirm, confirm_rect, title0, title0_rect, loadin, loadin_rect, subtitleload, subtitleload_rect # HOLY SHIT!
    BSOD = pygame.image.load(f"images/bsod.png") # Preloading!
    logoCC_raw = pygame.image.load(f"images/logo.png").convert_alpha()
    logoCC = pygame.transform.scale(logoCC_raw, (300, 220))
    logoCC_rect = logoCC.get_rect(center=(SCREEN_WIDTH/2,120))
    logoCC1 = pygame.transform.scale(logoCC_raw, (200, 146))
    logoCC1_rect = logoCC1.get_rect(midright=(SCREEN_WIDTH-20,120))
    welcome = pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 26).render(PRESS_ENTER, True, (255,255,255))
    welcome_rect = welcome.get_rect(center=(SCREEN_WIDTH/2, 320))
    ShellLikeTextIndicatorFlashTime = 0
    EnterPress = 0
    confirm = pygame.font.Font("fonts/Octarine.otf", 22).render(MENU_CONFIRM_READ, True, (255,255,255))
    confirm_rect = confirm.get_rect(center=(SCREEN_WIDTH/2, 335))
    title0 = pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 30).render(TUTORIAL_HOWTO, True, (255,255,255))
    title0_rect = title0.get_rect(center=(SCREEN_WIDTH/2, title0.get_height()/2+2))
    loadin = pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 32).render(LOADING, True, (255,255,255))
    loadin_rect = loadin.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    subtitleload = pygame.font.Font("fonts/Octarine.otf", 15).render(LOADING_SUBTEXT, True, (255,255,255))
    subtitleload_rect = subtitleload.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+20))

reload()
pygame.mixer.init()
while not ABORT_CODE_EXECUTION:
    pygame.mixer.music.stop() 
    pygame.mixer.music.load("music/intro.mp3") 
    pygame.mixer.music.set_volume(0.1) 
    pygame.mixer.music.play(-1) 
    global MathGen
    MathGen = [1, "+-", 20]
    eqs = 0
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
    Math.gen()
    EquaPointLimiter = 33150 # This is actually the maxium value you can get... without entering Bonus Mode.
    oldEquation = "-69"
    previousTime = 300
    diff = 0
    title1 = pygame.font.Font("fonts/Octarine.otf", 30).render(GAMER_OVER, True, (255,90,0))
    title1_rect = title1.get_rect(center=(SCREEN_WIDTH/2, title1.get_height()/2+3))
    SmoothEPIncreaser = 0
    epSuf = pygame.font.Font(None, 25).render(EQUAPOINTS, True, (255,255,255))
    epSuf_rect = epSuf.get_rect(midleft=(10, SCREEN_HEIGHT/4+16))
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
    Down = "Undefined"
    GameState = 0
    ShakeLevel = 0
    ShakeTicks = 0
    Combo_record = 1
    DebugMode = False
    StopRunning = False
    while not StopRunning and not ABORT_CODE_EXECUTION:
        screen.fill((0,0,0))
        AutoCheat = False
        if DebugMode:
            keys = pygame.key.get_pressed()
            AutoCheat = keys[pygame.K_c]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_INSERT:
                    if DebugMode:
                        DebugMode = False
                    else:
                        DebugMode = True
                if event.key == pygame.K_ESCAPE:
                    if GameState==2:
                        GameState+=1
                    else:
                        exit()
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
                    if GameState==0:
                        GameState+=1
                    elif GameState==1:
                        EnterPress+=1
                    elif GameState==4:
                        StopRunning=True
                
                if event.key==pygame.K_r and DebugMode:
                    reload()
                    
                if event.key==pygame.K_DELETE and DebugMode:
                    reload()
                
                if GameState==2:
                    # Input
                    if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        USERINPUT = USERINPUT + "0"
                    
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
                    
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or AutoCheat:
                        if suggest != "-":
                            USERINPUT = suggest
                        if AutoCheat:
                            USERINPUT = str(Result)
                        if USERINPUT == str(Result):
                            eqs += 1
                            print("User got the answer right")
                            feedback = 1
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
                            pygame.mixer.Sound("sound/correct.mp3").play()
                        else:
                            EquaPoints -= 600 # I know that the player can have -690000000 score.
                            print("User got the answer wrong")
                            print(f"-{600} = {EquaPoints}")
                            feedback = -1
                            if Combo>Combo_record:
                                Combo_record = Combo
                            Combo = 0
                            ShakeTicks = 30
                            pygame.mixer.Sound("sound/wrong.mp3").play()
                        print(f"Answered in {diff}s!")
                        feedback_ticks = 30
                        CurrentEquation += 1
                        USERINPUT = ""
                        try:
                            Math.gen()
                        except MathGenerationError:
                            print("MathGenerationError: Couldn't generate a valid equation that followed the game's conditions.")
                            screen.blit(BSOD, (0,0))
                            pygame.display.flip()
                            pygame.mixer.music.stop()
                            while not ABORT_CODE_EXECUTION:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        ABORT_CODE_EXECUTION = True
                        previousTime = Down.current
                    try:
                        if event.key == pygame.K_BACKSPACE:
                            USERINPUT = USERINPUT[:-1]
                    except:
                        USERINPUT = ""
                        
                if event.key == pygame.K_PAGEUP:
                    vol = min(pygame.mixer.music.get_volume() + 0.05, 1.0)
                    pygame.mixer.music.set_volume(vol)
                    
                if event.key == pygame.K_PAGEDOWN:
                    vol = max(pygame.mixer.music.get_volume() - 0.05, 0.05) # Avoid the music to be stopped.
                    pygame.mixer.music.set_volume(vol)
                    
                if event.key == pygame.K_END:
                    Down.current = -69
                    
        if GameState==0:
            if ShellLikeTextIndicatorFlashTime%30<15:
                screen.blit(welcome,welcome_rect)
            screen.blit(logoCC, logoCC_rect)
            
        if GameState==1:
            screen.blit(title0, title0_rect)
            display(20, TUTORIAL_TEXT, (255,255,255), (-9,0))
            if ShellLikeTextIndicatorFlashTime%30<15:
                screen.blit(welcome,welcome_rect)
            
            if EnterPress==1:
                screen.blit(confirm,confirm_rect)
            if EnterPress>1:
                GameState=2
                
        if GameState==2 and not ABORT_CODE_EXECUTION:
            screen.fill((0,0,0))
            if Down=="Undefined":
                screen.blit(loadin,loadin_rect)
                screen.blit(subtitleload,subtitleload_rect)
                pygame.display.flip()
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("music/speedrunning.mp3") # This is actually Dream Speedrunning music. 5 minutes and 21 seconds long. PERFECT!
                pygame.mixer.music.play()
                Down = Timer(False,300)
            StopRunning = Down.update()
            if Down.current <= 0:
                GameState=3
            
            if ShakeTicks>0:
                if ShakeTicks%4<3:
                    ShakeLevel = -ShakeTicks/5
                else:
                    ShakeLevel = ShakeTicks/5
                ShakeTicks -= 1
            else:
                ShakeLevel = 0
            
            if oldEquation != Equation:
                EquaRenderSize = 35
                EquaRenderWidth = 999
                while EquaRenderWidth>SCREEN_WIDTH:
                    EquaRender = pygame.font.Font(None, EquaRenderSize).render(f"{Equation} = ?", True, (255,255,255))
                    EquaRenderWidth = EquaRender.get_width()
                    EquaRenderSize -= 1
                oldEquation = Equation
            screen.blit(EquaRender, (ShakeLevel,ShakeLevel))
            if DebugMode:
                display(32,f">{USERINPUT}{"_" if ShellLikeTextIndicatorFlashTime % 30 < 15 else ""}", (255, 255, 0), (ShakeLevel,40+ShakeLevel))
            else:
                display(32,f">{USERINPUT}{"_" if ShellLikeTextIndicatorFlashTime % 30 < 15 else ""}", (255, 255, 255), (ShakeLevel,40+ShakeLevel))
            if CurrentEquation==0:
                eqscorinfofont_surf = pygame.font.Font("fonts/Octarine.otf", 15).render(f"0 {HUD_WRONG} / 0 {HUD_RIGHT} / 0% {HUD_ACCURACY}", True, (255,255,255))
            else:
                eqscorinfofont_surf = pygame.font.Font("fonts/Octarine.otf", 15).render(f"{CurrentEquation - eqs} {HUD_WRONG} / {eqs} {HUD_RIGHT} / {round(eqs/CurrentEquation*100)}% {HUD_ACCURACY}", True, (255,255,255))
                
            for rank, score in sorted(EquaRanks.items(), key=lambda x: x[1]):
                if EquaPoints/EquaPointLimiter > score:
                    EquaRank = rank
            
            # Making Right-To-Left text (cuz why not?)
            eqscorfont_surf = pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 50).render(EquaRank, True, (255,255,255)) 
            eqscorindfont_surf = pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 25).render("RANK", True, (255,255,255)) 
            EquaScoreTxT = pygame.font.Font(None, 25).render(f"{round(EquaPoints)} EP", True, (255,255,255)) 
            screen.blit(eqscorinfofont_surf, (SCREEN_WIDTH - eqscorinfofont_surf.get_width() - 10 + ShakeLevel, 301+ShakeLevel))
            screen.blit(EquaScoreTxT, (SCREEN_WIDTH - EquaScoreTxT.get_width() - 10 + ShakeLevel, 286+ShakeLevel))
            screen.blit(eqscorfont_surf, (SCREEN_WIDTH - eqscorfont_surf.get_width() - 10 + ShakeLevel, 320+ShakeLevel))
            screen.blit(eqscorindfont_surf, (SCREEN_WIDTH - eqscorfont_surf.get_width() - eqscorindfont_surf.get_width() - 13 + ShakeLevel, 330+ShakeLevel))
            
            if Combo<=Combo_record and Combo_record>1:
                        screen.blit(pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 15).render(f"{Combo_record} {COMBO_RECORD_BEAT}", True, (255,255,255)), (ShakeLevel,245+ShakeLevel))
                
            if Combo>1:
                if ShellLikeTextIndicatorFlashTime%10<5:
                    screen.blit(pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 25).render(f"x{Combo} COMBO!", True, (255,255,255)), (ShakeLevel,260+ShakeLevel))
                    if Combo>Combo_record:
                        screen.blit(pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 20).render(NEW_RECORD, True, (255,255,0)), (ShakeLevel,240+ShakeLevel))
                
            if eqs>19:
                if ShellLikeTextIndicatorFlashTime%20<10:
                    screen.blit(pygame.font.Font("fonts/Octarine.otf", 25).render(BONUS_TIME, True, (255,200,0)), (ShakeLevel,200+ShakeLevel))
                    
            color = (255, 0, 0) if Down.current < 60 else (255, 255, 255)
            if Down.current>=60 or ShellLikeTextIndicatorFlashTime%30<15:
                screen.blit(pygame.font.Font("fonts/HelNeuLTStdBlkExt.otf", 23).render(f"{Down.get()}", True, color), (ShakeLevel,335+ShakeLevel))
            
            if feedback_ticks>0:
                if feedback == -1:
                    screen.blit(pygame.font.Font(None, 20).render(WRONG_ANSWER, True, (255, 0, 0)), (ShakeLevel,150+ShakeLevel)) 
                if feedback == 1:
                    screen.blit(pygame.font.Font(None, 20).render(CORRECT_ANSWER, True, (0, 255, 0)), (ShakeLevel,150+ShakeLevel))
                feedback_ticks -= 1
            else:
                feedback = 0
            
            if "/" in USERINPUT:
                userfract = USERINPUT.split("/")
                try:
                    suggest = int(userfract[0])/int(userfract[1])
                    screen.blit(pygame.font.Font(None, 20).render(f"{ANSWER_SUGGESTION} {suggest}", True, (255, 255, 255)), (ShakeLevel,60+ShakeLevel))
                except Exception as e:
                    print(e)
                    suggest = "-"
        
        if GameState==3 and not ABORT_CODE_EXECUTION:
            screen.blit(loadin,loadin_rect)
            screen.blit(subtitleload,subtitleload_rect)
            pygame.display.flip()
            pygame.mixer.music.fadeout(1000)
            if eqs>19:
                pygame.mixer.music.load("music/bronzeLicense.mp3") # This is actually GT4's Bronze License music.
            else:
                pygame.mixer.music.load("music/gameOver.mp3") # This is actually Sonic CD's Japanese Game Over song.
            pygame.mixer.music.play()
            RankName = RankNames["T"]
            GameState=4
            
        if GameState==4:
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
            rankName_rect = rankName.get_rect(midleft=(10, SCREEN_HEIGHT/2+16))
            
            screen.blit(title1, title1_rect)
            screen.blit(point, point_rect)
            screen.blit(epSuf, epSuf_rect)
            screen.blit(rank, rank_rect)
            screen.blit(rankName, rankName_rect)
            screen.blit(logoCC1, logoCC1_rect)
            
            SmoothEPIncreaser += (EquaPoints-SmoothEPIncreaser)/20
            
            if ShellLikeTextIndicatorFlashTime%30<15:
                screen.blit(welcome,welcome_rect)
            
        pygame.display.flip()
        mainClock.tick(60)
        ShellLikeTextIndicatorFlashTime += 1