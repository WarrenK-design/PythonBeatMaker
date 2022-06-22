## House Keeping 
# Github - WarrenKDesign 
# 1:05 mins in 

### Imports ###
# pygame - 
# mixer 
import pygame
from pygame import mixer 

pygame.init() 

### Variables ###
# Screen Size 
width  = 1400
height = 800

# Colours 
black = (0,0,0)
white = (255, 255, 255)
gray  = (128,128,128)
green = (0,255,0)
gold  = (212, 175, 55)
blue  = (0, 255, 255)
dark_grey = (50, 50, 50)


# Create the screen 
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption('Beat Maker')
# Set the font style and size
label_font = pygame.font.Font('freesansbold.ttf', 32)
medium_font = pygame.font.Font('freesansbold.ttf', 24)
# Frames per second 
fps = 60
# Timer for refresh rate 
timer = pygame.time.Clock()
# beats per minute - 240 is 4 beats per second roughly, 240ms 
bpm = 240 
# playing - i.e music not paused 
playing = True 
# active_length - How long the current beat has been playing 
active_lenght = 0
# active_beat - The number of activated beats 
active_beat = 0 
# beat_changed  - Flag for tellling when beat has changed 
beat_changed = True 

# beats - How many beats we have 
# instrments - Number of sounds 
beats = 8 
instruments = 6 

# boxes   - An array of boxes where each element will be a tuple containg a rectangle object and coords 
# clicked - Array which keeps track of which beats have been clicked for each instrument, -1 means not clicked 
boxes   = [] 
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)] 

### Load in sounds ###
hi_hat = mixer.Sound('sounds/hi hat.WAV')
clap = mixer.Sound('sounds/clap.WAV')
crash = mixer.Sound('sounds/crash.WAV')
bass = mixer.Sound('sounds/kick.WAV')
snare = mixer.Sound('sounds/snare.WAV')
tom = mixer.Sound('sounds/tom.WAV')

# Increase the number of channels music can be played from 
pygame.mixer.set_num_channels(instruments*3)


#### Functions ####
def play_notes():
    '''
    Plays the notes for the instruments 
    '''
    for i in range(len(clicked)):
        # If clciked at i being the row and active beat being column = 1 then its clciked 
        if clicked[i][active_beat] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                bass.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()


def draw_grid(clicks,beat):
    '''
    Inputs:
        clicked - An array which keeps track of which beat has been clciked, 1 denotes clciked, -1 not clicked 
        beat    - The current active beat 
    '''
    # left box will be for instruments, starts at top left 0,0 coords, 200 width and height of screen, 5 makes hollow object 
    left_box = pygame.draw.rect(screen, gray, [0,0,200,height-200],5)
    # bottom_box - For controls 
    bottom_box = pygame.draw.rect(screen, gray, [0, height -200, width, 200], 5)
    # boxes - For the beat display 
    boxes = [] 
    colours = [gray, white, gray]
    ## Create the texts 
    hi_hat_text = label_font.render('Hi Hat', True, white)
    snare_text  = label_font.render('Snare', True, white)
    bass_text  = label_font.render('Bass Drum', True, white)
    crash_text  = label_font.render('Crash', True, white)
    clap_text  = label_font.render('Clap', True, white)
    floor_text  = label_font.render('Floor Tom', True, white)
    # Write the text to screen 
    screen.blit(hi_hat_text,(15,30))
    screen.blit(snare_text,(15,130))
    screen.blit(bass_text,(15,230))
    screen.blit(crash_text,(15,330))
    screen.blit(clap_text,(15,430))
    screen.blit(floor_text,(15,530))
    # Draw lines between instrument labels 
    for i in range(instruments):
        # Inputs are screen, colour, start pos, end pos and line thicness
        pygame.draw.line(screen, gray, (0, (i*100) + 100), (200,(i*100) + 100), 3)

    for i in range(beats):
        for j in range(instruments):
            # Check if the current rectangle has been clicked 
            if clicks[j][i] == -1:
                colour = gray
            else:
                colour = green
            # Draw the rectangles around the beates part of the screen, will be 8 beats to start per instruments  
            rect = pygame.draw.rect(screen, colour, [i*((width-200) //beats) + 205, (j*100)+5, 
                                    ((width-200) // beats) - 10, ((height-200)//instruments) - 10],0,3)

            pygame.draw.rect(screen, gold, [i*((width-200) //beats) + 200, (j*100), 
                                    ((width-200) // beats), ((height-200)//instruments)], 5,5)

            pygame.draw.rect(screen, black, [i*((width-200) //beats) + 200, (j*100), 
                                    ((width-200) // beats), ((height-200)//instruments)], 2,5)
            # boxes - The recatangle for each beat and the coords of it 
            boxes.append((rect, (i,j)))

    # active - This is the moving rectangle which shows which beat is currently active 
    active = pygame.draw.rect(screen,blue, [beat*((width-200)//beats) + 200, 0, ((width - 200) // beats), instruments * 100], 5, 3)
    # This is the grid for the beats, returned as we need to know if any beats have been clicked     
    return boxes 




run = True 
while run:
    # While run is true, execute this code at the frame rate 
    timer.tick(fps)
    # Screen background colour 
    screen.fill(black)
    # Draw the screen  - Returns boxes which will be used to see if any of the beat boxes have been clicked
    boxes = draw_grid(clicked,active_beat)
    # Lower menu buttons 
    play_pause = pygame.draw.rect(screen, gray, [50, height - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (60, height -130))
    if playing:
        play_sub_text = medium_font.render('Playing', True, dark_grey)
    else:
        play_sub_text = medium_font.render('Paused', True, dark_grey)
    screen.blit(play_sub_text, (100, height -100))
    ### BPM - Displays the current BPM ###
    bpm_rect = pygame.draw.rect(screen, gray, [300, height-150, 215, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text,(308, height-130))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2,(370, height-100))
    ### Add/Sub BPM 
    bpm_add_rect = pygame.draw.rect(screen, gray, [525, height - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [525, height - 100, 48, 48], 0, 5) 
    add_text     = medium_font.render('+5',True, white) 
    sub_text     = medium_font.render('-5',True, white)
    screen.blit(add_text,(535, height-140))
    screen.blit(sub_text,(535,height-90))


    # See if the beat has changed -> Will change once per loop 
    if beat_changed:
        play_notes()
        beat_changed = False
    # Checks the events 
    for event in pygame.event.get():
        # Quite event - quit the game 
        if event.type == pygame.QUIT:
            run = False 
        # Clicked mouse down but haent released it 
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Iterate through each of the beat boxes 
            for i in range(len(boxes)):
                # [i][0] will be the acutaul rectange object, if the event collides withthis then its a click 
                if boxes[i][0].collidepoint(event.pos):
                    # Get the x and y coords for the box 
                    coords = boxes[i][1]
                    # Set the clciked box from -1 to 1 
                    clicked[coords[1]][coords[0]] *= -1
        # Mouse has been clciked and released 
        if event.type == pygame.MOUSEBUTTONUP:
            # Clicking of the play//pause button 
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True 
            # Add/Sub the bpm 
            elif bpm_add_rect.collidepoint(event.pos):
                bpm+=5
            elif bpm_sub_rect.collidepoint(event.pos) and bpm != 5:
                bpm-=5


    # beat_lenght - The lenght of each beat 
    beat_length = (fps*60) // bpm 

    # Music is not paused 
    if playing:
        # Active length is the lenght the current beat has been playing 
        if active_lenght < beat_length:
            # Add one the beat is playing 
            active_lenght += 1
        else: # The beat has reached how long it should be playing 
            active_lenght = 0 
            if active_beat < beats -1: # We are not yet at the end of all the beats 
                # Increment the active beat 
                active_beat += 1
                # Set the beat changed flag 
                beat_changed = True
            else: # At the end of the loop 
                active_beat = 0 
                beat_changed = True  


    # Display the game 
    pygame.display.flip()

pygame.quit()

