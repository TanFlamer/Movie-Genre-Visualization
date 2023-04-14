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
    def __init__(self, canvas, x, y, speed, game_mode, width, height):
        self.radius = 10
        self.direction = [2 * random.randint(0, 1) - 1, 2 * game_mode - 1]
        # increase the below value to increase the speed of ball
        self.speed = speed
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='white')
        self.game_mode = game_mode
        self.width = width
        self.height = height
        super(Ball, self).__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        if coords[0] <= 0 or coords[2] >= self.width: self.direction[0] *= -1
        if self.ceiling_collision(coords): self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)

    def ceiling_collision(self, coords):
        return (not self.game_mode and coords[1] <= 0) or (self.game_mode and coords[1] >= self.height)

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
    def __init__(self, canvas, x, y, offset):
        self.width = 80
        self.height = 10
        self.offset = offset
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
        if coords[2] + self.offset <= self.canvas.winfo_width():
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
        self.canvas = tk.Canvas(self, bg='#D6D1F5',
                                width=self.width,
                                height=self.height, )
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.paddle = self.add_paddle()
        self.ball = self.add_ball()

        self.brick_width = self.width / self.bricks_in_row
        self.brick_height = 20

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
        paddle_y = 25 if self.game_mode else self.height - 25
        paddle = Paddle(self.canvas, paddle_x, paddle_y, self.paddle_speed)
        self.items[paddle.item] = paddle
        return paddle

    def add_ball(self):
        [x, y] = self.paddle.get_midpoint()
        offset = 16 if self.game_mode else -16
        ball = Ball(self.canvas, x, y + offset, self.ball_speed, self.game_mode, self.width, self.height)
        return ball

    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits, self.brick_width, self.brick_height)
        self.items[brick.item] = brick

    def add_bricks(self):
        for y in range(self.brick_rows):
            for x in range(self.bricks_in_row):
                brick_x = (x + 0.5) * self.brick_width
                offset = y * self.brick_height
                brick_y = (self.height - 50) - offset if self.game_mode else offset + 50
                self.add_brick(brick_x, brick_y, self.brick_type(x, y))

    def brick_type(self, x, y):
        if self.brick_placement == "Row":
            return (y % 3) + 1
        elif self.brick_placement == "Column":
            return (x % 3) + 1
        else:
            return random.randint(1, 3)

    def draw_text(self, x, y, text, size='40'):
        font = ('Forte', size)
        return self.canvas.create_text(x, y, text=text, font=font)

    def update_lives_text(self):
        self.qLearning.new_episode(self.getObv())
        text = 'Lives: %s' % self.qLearning.episode
        x = self.width - 50 if self.game_mode else 50
        y = self.height - 20 if self.game_mode else 20
        self.draw_text(x, y, text, str(15))

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
        elif self.out_of_bounds(self.ball.get_position()):
            print(self.qLearning.episode, str(num_bricks) + " left")
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
            self.after(1000, self.game_loop)

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)

    def out_of_bounds(self, ball_coords):
        return (not self.game_mode and ball_coords[3] >= self.height) or (self.game_mode and ball_coords[1] <= 0)


def main(game_settings, qLearning):
    root = tk.Tk()
    root.title('Break those Bricks!')
    game = Game(root, game_settings, qLearning)
    game.mainloop()


if __name__ == '__main__':
    game_settings = [5, 10, 5, 8, "Random", True]
    qLearning = QLearning()
    main(game_settings, qLearning)
