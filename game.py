import random
import sys
import tkinter as tk

from Coursework.BrickBreaker.qlearning import QLearning


class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def get_midpoint(self):
        coords = self.get_position()
        return [(coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2]

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


class Ball(GameObject):
    def __init__(self, canvas, x, y, speed, game_mode, canvas_dimensions):
        self.radius = 10
        self.direction = [2 * random.randint(0, 1) - 1, 2 * game_mode - 1]
        # increase the below value to increase the speed of ball
        self.speed = speed
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='white')
        self.game_mode = game_mode
        [self.canvas_width, self.canvas_height] = canvas_dimensions
        super(Ball, self).__init__(canvas, item)

    def update(self):
        # Get ball coordinates
        coords = self.get_position()
        # Check for wall collision
        horizontal = self.horizontal_collision(coords)
        vertical = self.vertical_collision(coords)
        # Reverse ball direction if collision
        self.reverse_direction(horizontal, 0)
        self.reverse_direction(vertical, 1)
        # Get new ball displacement
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        # Move ball
        self.move(x, y)

    def reverse_direction(self, condition, direction):
        if condition: self.direction[direction] *= -1

    def horizontal_collision(self, coords):
        return coords[0] <= 0 or coords[2] >= self.canvas_width

    def vertical_collision(self, coords):
        return coords[3] >= self.canvas_height if self.game_mode else coords[1] <= 0

    def collide(self, game_objects):
        x = self.get_midpoint()[0]

        if len(game_objects) > 1:
            self.direction[1] *= -1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coords = game_object.get_position()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()


class Paddle(GameObject):
    def __init__(self, canvas, x, y, offset, canvas_dimensions):
        self.width = 80
        self.height = 10
        self.offset = offset
        [self.canvas_width, _] = canvas_dimensions
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='#FFB643')
        super(Paddle, self).__init__(canvas, item)

    def doNothing(self):
        super(Paddle, self).move(0, 0)

    def moveLeft(self):
        coords = self.get_position()
        if coords[0] - self.offset >= 0:
            super(Paddle, self).move(-self.offset, 0)

    def moveRight(self):
        coords = self.get_position()
        if coords[2] + self.offset <= self.canvas_width:
            super(Paddle, self).move(self.offset, 0)


class Brick(GameObject):
    COLORS = {1: '#4535AA', 2: '#ED639E', 3: '#8FE1A2'}

    def __init__(self, canvas, x, y, hits, brick_width, brick_height):
        self.width = brick_width
        self.height = brick_height
        self.hits = hits
        color = Brick.COLORS[hits]
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            self.delete()
        else:
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])


class Game(tk.Frame):
    def __init__(self, master, game_settings, qLearning):
        super(Game, self).__init__(master)

        self.game_settings = game_settings

        [self.ball_speed, self.paddle_speed, self.brick_rows, self.bricks_in_row,
         self.brick_placement, self.game_mode] = self.game_settings

        self.qLearning = qLearning

        self.width = 600
        self.height = 450
        self.dimensions = [self.width, self.height]
        self.canvas = tk.Canvas(self, bg='#D6D1F5',
                                width=self.width,
                                height=self.height, )
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.paddle = self.add_paddle()
        self.ball = self.add_ball()

        # Paddle movement
        self.horizontal_actions = [self.paddle.moveLeft, self.paddle.doNothing, self.paddle.moveRight]

        self.setup_game()
        self.canvas.focus_set()

    def getObv(self):
        return self.paddle.get_midpoint() + self.ball.get_midpoint()

    def setup_game(self):
        self.add_bricks()
        self.update_lives_text()
        self.game_loop()

    def add_paddle(self):
        paddle_x = random.randint(40, self.width - 40)
        paddle_y = self.select_value(25, self.height - 25)
        paddle = Paddle(self.canvas, paddle_x, paddle_y, self.paddle_speed, self.dimensions)
        self.items[paddle.item] = paddle
        return paddle

    def add_ball(self):
        [x, y] = self.paddle.get_midpoint()
        offset = self.select_value(16, -16)
        ball = Ball(self.canvas, x, y + offset, self.ball_speed, self.game_mode, self.dimensions)
        return ball

    def add_bricks(self):
        # Brick dimensions
        brick_width = self.width / self.bricks_in_row
        brick_height = 20
        # Brick loop
        for y in range(self.brick_rows):
            for x in range(self.bricks_in_row):
                # Brick variables
                brick_x = (x + 0.5) * brick_width
                offset = y * brick_height + 50
                brick_y = self.select_value(self.height - offset, offset)
                hits = self.brick_type(x, y)
                # Brick creation
                brick = Brick(self.canvas, brick_x, brick_y, hits, brick_width, brick_height)
                self.items[brick.item] = brick

    def brick_type(self, x, y):
        if self.brick_placement == "Row":
            return (y % 3) + 1
        elif self.brick_placement == "Column":
            return (x % 3) + 1
        else:
            return random.randint(1, 3)

    def select_value(self, first, second):
        return first if self.game_mode else second

    def update_lives_text(self):
        self.qLearning.new_episode(self.getObv())
        font = ('Forte', 15)
        text = 'Lives: %s' % self.qLearning.episode
        x = self.select_value(self.width - 50, 50)
        y = self.select_value(self.height - 20, 20)
        self.canvas.create_text(x, y, text=text, font=font)

    def game_loop(self):
        # Get action
        horizontal_action, _ = self.qLearning.get_action()
        self.horizontal_actions[horizontal_action]()
        # Check for collision
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:
            self.ball.speed = None
            print(self.qLearning.episode, "Done")
            sys.exit()
        elif self.out_of_bounds():
            # Stop ball
            self.ball.speed = None
            # Update Q-table
            self.qLearning.update_table(self.getObv(), 0)
            # Close window
            self.destroy()
            # Start new game
            self.__init__(self.master, self.game_settings, self.qLearning)
        else:
            # Update ball position
            self.ball.update()
            # Update Q-table
            self.qLearning.update_table(self.getObv(), 1)
            # Next loop
            self.after(1, self.game_loop)

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)

    def out_of_bounds(self):
        ball_coords = self.ball.get_position()
        return ball_coords[1] <= 0 if self.game_mode else ball_coords[3] >= self.height


def main(game_settings, qLearning):
    root = tk.Tk()
    root.title('Break those Bricks!')
    game = Game(root, game_settings, qLearning)
    game.mainloop()


if __name__ == '__main__':
    game_settings = [5, 10, 5, 8, "Random", False]
    qLearning = QLearning()
    main(game_settings, qLearning)
