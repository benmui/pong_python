# Pong assignment in CodeSkulptor for Coursera Intro to Interactive Programming in Python
# Ben - 4/27/2019

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = 0
paddle2_pos = 0
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2
    ball_vel[1] = -1 * random.randrange(60,180) // 60
    if direction:
        # right-ward moving spawn
        ball_vel[0] = random.randrange(120,240) // 60
    else:
        # left-ward moving spawn
        ball_vel[0] = -1 * random.randrange(120,240) // 60


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    # reset the paddle positions and the score, and spawn a ball going right
    paddle1_pos = 0
    paddle2_pos = 0
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT - HEIGHT/2) and \
       (paddle1_pos + paddle1_vel <= HEIGHT/2 - HALF_PAD_HEIGHT):
        paddle1_pos += paddle1_vel
    if (paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT - HEIGHT/2) and \
       (paddle2_pos + paddle2_vel <= HEIGHT/2 - HALF_PAD_HEIGHT):
        paddle2_pos += paddle2_vel

    
    # draw paddles
    canvas.draw_polygon([[0,         HEIGHT / 2 - HALF_PAD_HEIGHT + paddle1_pos], \
                         [PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT + paddle1_pos], \
                         [PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT + paddle1_pos], \
                         [0,         HEIGHT / 2 + HALF_PAD_HEIGHT + paddle1_pos]], \
                        1, "White", "White")
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT + paddle2_pos], \
                         [WIDTH,             HEIGHT / 2 - HALF_PAD_HEIGHT + paddle2_pos], \
                         [WIDTH,             HEIGHT / 2 + HALF_PAD_HEIGHT + paddle2_pos], \
                         [WIDTH - PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT + paddle2_pos]], \
                        1, "White", "White")

    # determine whether paddle and ball collide
    # check for collision with left side
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        # COLLISION!
        if ball_pos[1] > HEIGHT/2 + (paddle1_pos - HALF_PAD_HEIGHT) and \
           ball_pos[1] < HEIGHT/2 + (paddle1_pos + HALF_PAD_HEIGHT):
                # BOUNCE BACK
                ball_vel[0] = -1.1 * ball_vel[0]
        else:
            # Player 2 scored!
            score2 += 1
            spawn_ball(RIGHT)
    # check for collision with right side
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        # COLLISION!
        if ball_pos[1] > HEIGHT/2 + (paddle2_pos - HALF_PAD_HEIGHT) and \
           ball_pos[1] < HEIGHT/2 + (paddle2_pos + HALF_PAD_HEIGHT):
                # BOUNCE BACK
                ball_vel[0] = -1.1 * ball_vel[0]
                ball_vel[1] = 1.1 * ball_vel[1]
        else:
            # Player 2 scored!
            score1 += 1
            spawn_ball(LEFT)
    elif ball_pos[1] <= BALL_RADIUS:
        # COLLISION!
                ball_vel[1] = -1 * ball_vel[1]
    elif ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        # COLLISION!
                ball_vel[1] = -1 * ball_vel[1]
                ball_vel[1] = 1.1 * ball_vel[1]
                
    # draw scores
    canvas.draw_text(str(score1),(230,35),28,"White")
    canvas.draw_text(str(score2),(350,35),28,"White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -5
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 5
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -5
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 5
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0



# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
reset_button = frame.add_button('Reset', new_game, )


# start frame
new_game()
frame.start()
