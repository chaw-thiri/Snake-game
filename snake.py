import re
from tkinter import messagebox
from tkinter import *
import random
import pygame


pygame.mixer.init()

# variable for the game
GAME_WIDTH = 540
GAME_HEIGHT = 600
SPEED =200       # initial snake's speed, the smaller the faster(millisecond)
SPACE_SIZE =  30  # size of each unit of the snake body and the food
BODY_PARTS = 2

#color codes()
snake_color_range=['#698362',"#3c793d",'#FAC81B','#FAA21B','#F6881F','#404040','#E56925','#8D54A2','#0C793D']
food_color_range=['#F8B195','#F67280','#C06C84','#28083D']
SNAKE_COLOR = random.choice(snake_color_range)
FOOD_COLOR = random.choice(food_color_range)   
CANVAS_BGCOLOR = "#000000" # black
WINDOW_BGCOLOR='#240504'    


window = Tk()
window_icon=PhotoImage(file='halloween emoji.png')
window.iconphoto(True,window_icon)
window.title("Hungry Snake")
window.geometry('700x700')
window.config(background=WINDOW_BGCOLOR)
window.resizable(True, True)
song_on_image=PhotoImage(file='sound_on.png')
song_off_image=PhotoImage(file='sound_off.png')

class Snake: 
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        #location for the snake
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0]) 
        #place the snake
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE     # -1 bc exclusive, space_size bc pixels
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y,x+SPACE_SIZE,y+SPACE_SIZE,fill=FOOD_COLOR,tag="food") 

#....................................................................................................................................

def songon():
    pygame.mixer.music.load('double trouble.mp3')
    pygame.mixer.music.play(loops=10)
def songoff():
    pygame.mixer.music.stop()    
def turn(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right': #to prevent 180deg turn 
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction
def hit(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH: # touch left or right border 
        return True
    elif y < 0 or y >= GAME_HEIGHT:   # touch upper or lower border 
        return True

    for body_part in snake.coordinates[1:]: # 1: represent every part after the head of the snake
        if x == body_part[0] and y == body_part[1]: # touch its body parts
            return True
    return False
def play(snake, food):
    x, y = snake.coordinates[0] # head of the snake
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    #locate the snake
    snake.coordinates.insert(0, (x, y))   #at index 0, add x,y
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    #eating the food
    if x == food.coordinates[0] and y == food.coordinates[1]: #int
        global score
        global SPEED
        score += 1
        SPEED-=2   #the longer the snake, the faster it is
        label.config(text=f"Score:{score}")
        canvas.delete("food")
        food = Food()
    else:
        canvas.delete(snake.squares[-1]) #move
        del snake.squares[-1]
        del snake.coordinates[-1]   #delete the last segment of the snake
        
    #collision check
    if hit(snake):
        game_over()
    else:
        window.after(SPEED, play, snake, food)   # to update the snake after every move
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                        font=('Chiller',60), text="GAME OVER ", fill='red', tag="gameover_text")   
def game():
    start_button.config(state="disabled")
    global cover_image
    canvas.delete(cover_image)
    snake = Snake()
    food = Food()
    play(snake, food)
def help():
    messagebox.showinfo(title="Game Controls",message="Click 'w' or '⬆' to go up. \n Click 's' or '⬇' to go down. \n Click 'a' or '⬅' to go left.\n Click 'd' or '➡' to go right. \n Click START button to begin. \n Click EXIT to leave the game.  ")    
def exit():
    window.quit()

#....................................................................................................................................

score = 0
direction = 'right'   # initial direction

canvas_background=PhotoImage(file='canvas background.png')
canvas = Canvas(window,bg=CANVAS_BGCOLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
cover_image= canvas.create_image(180,220,image=canvas_background)
canvas.pack()


#score label
label=Label(window,text=f'Score:{score}',font=("impact",30),fg='white',bg=CANVAS_BGCOLOR,padx=15)
label.pack(side=LEFT,fill=X)


#sound on and off
song_on_button=Button(window,image=song_on_image,fg='white',command=songon,borderwidth=0)
song_on_button.pack(side=LEFT)
song_off_button=Button(window,image=song_off_image,fg='white',command=songoff,borderwidth=0)
song_off_button.pack(side=LEFT)

start_button=Button(window,text='Start',font=("impact",30),fg='white',bg=CANVAS_BGCOLOR,command=game,padx=15    )
start_button.pack(side=RIGHT)
exit_button=Button(window,text='Exit',font=("impact",30),fg='white',bg=CANVAS_BGCOLOR,command=exit,padx=15)
exit_button.pack(side=RIGHT)
help_button=Button(window,text='Help',font=("impact",30),fg='white',bg=CANVAS_BGCOLOR,command=help,padx=15)
help_button.pack(side=RIGHT)

window.update()
#placing the game in the middle of the screen.
window_width = window.winfo_width()
window_height = window.winfo_height() 
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}-{x}-{y}")  
window.config

#buttons
window.bind('<Left>', lambda x: turn('left'))
window.bind('<Right>', lambda x: turn('right'))
window.bind('<Up>', lambda x: turn('up'))
window.bind('<Down>', lambda x: turn('down'))

window.bind('<a>', lambda x: turn('left'))
window.bind('<d>', lambda x: turn('right'))
window.bind('<w>', lambda x: turn('up'))
window.bind('<s>', lambda x: turn('down'))

songon()

window.mainloop()






