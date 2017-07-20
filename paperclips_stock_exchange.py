import math
import random
import pygame
import time
from scipy.stats import norm

pygame.init()

class c:
   bk    = (   0,   0,   0) # black
   w     = ( 255, 255, 255) # white
   g     = (   0, 255,   0) # green
   r     = ( 255,   0,   0) # red
   b     = (   0,   0, 255) # blue

# --- Initial stock values --- #
A_init = 1000
A_price = 1000
A_annual_volatility = 0.2
A_daily_volatility = adv = ( A_annual_volatility / math.sqrt(252.0) )
stock_A = [A_init]
A_count = 1

B_init = 900
B_price = 900
B_annual_volatility = 1.5
B_daily_volatility = bdv = ( B_annual_volatility / math.sqrt(252.0) )
stock_B = [B_init]
B_count = 1
# ---------------------------- #

# --- Graphical quantities --- #
y_axis_pix = YP = 250.0
y_axis_scale = ys = (A_price * 2)
y_pix_per_scale = (y_axis_pix / y_axis_scale)
y_zero = 350
y_max = 100

x_axis_pix = xp = 475
x_axis_scale = xs = 20
x_pix_per_scale = xp / xs
x_zero = 125
x_max = 600
x_count = 1

num_horizontal_segments = 20
rescale_tolerance = 25
# ---------------------------- #

# --- Initialize point lists --- #
A_point_list = [[x_zero, y_zero - (A_init * y_pix_per_scale)]] # initialize point list
B_point_list = [[x_zero, y_zero - (B_init * y_pix_per_scale)]]
# ---------------------------- #

# --- pygame globals --- #
size = (700,500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Paperclips")
exit_game = False
clock = pygame.time.Clock()
draw = pygame.draw
update_rate_count = 4
# -------------------------- #

def new_price(price_ref, daily_volatility):
    return price_ref * ( 1 + norm.ppf( random.random(), 0, daily_volatility ) )

def rescale_axes(price_ref):
    global y_axis_scale, y_pix_per_scale, num_horizontal_segments
    y_axis_scale = price_ref * 2.0
    y_pix_per_scale = y_axis_pix / y_axis_scale
    #print "y-scale: %f, y_pix_per_scale: %f" % (y_axis_scale, y_pix_per_scale)

def to_pix_position(price_ref, _count):
    global y_pix_per_scale, y_max, x_pix_per_scale, x_max, x_count, num_horizontal_segments
    y_val = price_ref * y_pix_per_scale
    y_pos = y_zero - y_val
    if (abs(y_pos - y_max) < rescale_tolerance):
        rescale_axes(price_ref)
    else:
        pass
    x_pos = ( _count * x_pix_per_scale ) + x_zero
    if _count != num_horizontal_segments:
        _count += 1
    else:
        pass
    new_pos = [x_pos, y_pos]
    new_count = _count
    return new_pos, new_count

def stock_(price_, stock_list, point_list, daily_volatility, _count): # A_price, stock_A, A_point_list
    global num_horizontal_segments, x_pix_per_scale, update_rate_count
    new_count = _count
    update_price = price_
    if update_rate_count == 5:
        update_price = new_price(price_, daily_volatility)
        #stock_list.append( new_price )
        #price_ = stock_list[len(stock_list) - 1]
        # --- price to pixel position --- #
        new_pos, new_count = to_pix_position(update_price, _count)
        point_list.append( new_pos )
        #print '-' * 10
        #print "1ST point list:", point_list
        if len(point_list) == num_horizontal_segments + 1:
            point_list = point_list[1:]
            for i in range( len(point_list) ):
                point_list[i][0] -= x_pix_per_scale
        else:
            pass
        print '-' * 10
        print "price:", update_price
        print '-' * 10
        #print "2ND point list:", point_list
        # ------------------------------- #
        #print '-' * 10
    #        print "stock_A:", stock_A
    #        print '-' * 10
    #        print 'A_price:', A_price
    else:
        pass
    return point_list, new_count, update_price

def scale_numbers():
    global y_axis_scale

    div = 10
    y_q = y_axis_scale / div
    scale_nums = []

    for n in range( 0, div + 1 ):
	       scale_nums.append( ( y_axis_scale - ( n * y_q ) ) )

    return scale_nums

while not exit_game:
    #global A_price
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        elif event.type == pygame.KEYDOWN:
            print("User pressed a key.")
        elif event.type == pygame.KEYUP:
            print("User let go of a key.")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("User pressed a mouse button")
        else:
            pass

    # --- Game logic goes here --- #
    update_rate_count += 1
    #print "rate count:", update_rate_count
    #print '-' * 10
    #A_point_list, A_count, A_price = stock_(A_price, stock_A, A_point_list, adv, A_count)
    B_point_list, B_count, B_price = stock_(B_price, stock_B, B_point_list, bdv, B_count)
    if update_rate_count == 5:
        update_rate_count = 0
    else:
        pass
    #print "3ND point list:", A_point_list
    #print '-' * 10

    # --- Drawing code goes here --- #
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command:
    screen.fill(c.w)
    draw.line(screen, c.bk, [x_zero, y_max], [x_zero, (y_zero + 25)], 1) # Y AXIS
    draw.line(screen, c.bk, [(x_zero - 25), y_zero], [x_max, y_zero], 1) # X AXIS
    #draw.lines(screen, c.r, False, A_point_list, 1)
    draw.lines(screen, c.b, False, B_point_list, 1)
    font = pygame.font.SysFont('Times New Roman', 18, False, False)
    text = font.render('Paperclip Stock Exchange', True, c.bk)
    screen.blit(text, [300,50])
    for i in range(0, len(scale_numbers())):
        scale_num_labels = font.render( "%.0f" % scale_numbers()[i], True, c.bk)
        screen.blit(scale_num_labels, [80, 85 + i*(y_axis_pix/10)])
    # --- Drawing code ends here --- #

    # --- Update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second.
    clock.tick(10)

pygame.quit()

for i in range(0,1):
    x = random.random()
    print x

print math.pi
