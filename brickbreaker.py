import random
import sys
import tkinter as tk

from Lab.Coursework.BrickBreaker.qlearning import QLearning


class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.direction = [2 * random.randint(0, 1) - 1, -1]
        # increase the below value to increase the speed of ball
        self.speed = 5
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='white')
        super(Ball, self).__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)

    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5

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

        score = 0
        for game_object in game_objects:
            if isinstance(game_object, Brick):
                score += game_object.hit()
        return score


class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = 10
        self.offset = 10
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

    def moveUp(self):
        coords = self.get_position()
        if coords[1] - self.offset >= 300:
            super(Paddle, self).move(0, -self.offset)

    def moveDown(self):
        coords = self.get_position()
        if coords[3] + self.offset <= self.canvas.winfo_height():
            super(Paddle, self).move(0, self.offset)


class Brick(GameObject):
    COLORS = {1: '#4535AA', 2: '#ED639E', 3: '#8FE1A2'}

    def __init__(self, canvas, x, y, hits):
        self.width = 75
        self.height = 20
        self.hits = hits
        color = Brick.COLORS[hits]
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)

    def hit(self):
        hit_score = 10
        self.hits -= 1
        if self.hits == 0:
            self.delete()
        else:
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])
        return hit_score


class Game(tk.Frame):
    def __init__(self, master, qLearning):
        super(Game, self).__init__(master)

        self.qLearning = qLearning
        self.current_score = 0
        self.total_score = 0

        self.width = 600
        self.height = 600
        self.canvas = tk.Canvas(self, bg='#D6D1F5',
                                width=self.width,
                                height=self.height, )
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.ball = None
        self.paddle = Paddle(self.canvas, random.randint(40, self.width - 40), random.randint(305, self.height - 5))
        self.items[self.paddle.item] = self.paddle

        # Paddle movement
        self.horizontal_actions = [self.paddle.moveLeft, self.paddle.doNothing, self.paddle.moveRight]
        self.vertical_actions = [self.paddle.moveUp, self.paddle.doNothing,self.paddle.moveDown]

        # adding brick with different hit capacities - 3,2 and 1
        for x in range(10):
            for y in range(5, self.width - 5, 75):
                self.add_brick(y + 37.5, x * 20 + 50, random.randint(1, 3))

        self.lives_hud = None
        self.current_hud = None
        self.total_hud = None

        self.setup_game()
        self.canvas.focus_set()

        # self.canvas.bind('<Left>', lambda _: self.paddle.moveLeft())
        # self.canvas.bind('<Right>', lambda _: self.paddle.moveRight())
        # self.canvas.bind('<Up>', lambda _: self.paddle.moveUp())
        # self.canvas.bind('<Down>', lambda _: self.paddle.moveDown())

    def getObv(self):
        return self.paddle.get_position(), self.ball.get_position()

    def setup_game(self):
        self.add_ball()
        self.update_lives_text()
        self.qLearning.new_episode()
        self.qLearning.get_initial_state(self.getObv())
        self.game_loop()

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        y = (paddle_coords[1] + paddle_coords[3]) * 0.5
        self.ball = Ball(self.canvas, x, y - 16)

    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def draw_text(self, x, y, text, size='40'):
        font = ('Forte', size)
        return self.canvas.create_text(x, y, text=text,
                                       font=font)

    def update_lives_text(self):
        text = 'Lives: %s' % self.qLearning.episode
        if self.lives_hud is None:
            self.lives_hud = self.draw_text(50, 20, text, str(15))
        else:
            self.canvas.itemconfig(self.lives_hud, text=text)

    def update_current_text(self):
        text = 'Current Score: %s' % self.current_score
        if self.current_hud is None:
            self.current_hud = self.draw_text(520, 20, text, str(15))
        else:
            self.canvas.itemconfig(self.current_hud, text=text)

    def update_total_text(self):
        text = 'Total Score: %s' % self.total_score
        if self.total_hud is None:
            self.total_hud = self.draw_text(295, 20, text, str(15))
        else:
            self.canvas.itemconfig(self.total_hud, text=text)

    def update_score(self, new_score):
        if new_score != 1:
            self.current_score = new_score
            self.update_current_text()
            self.total_score += new_score
            self.update_total_text()

    def game_loop(self):
        # Get action
        horizontal_action, vertical_action = self.qLearning.get_action()
        self.horizontal_actions[horizontal_action]()
        self.vertical_actions[vertical_action]()
        # Check for collision
        score = self.check_collisions()
        self.update_score(score)
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:
            self.ball.speed = None
            self.update_score(1000)
            print(self.qLearning.episode)
            sys.exit()
        elif self.ball.get_position()[3] >= self.height:
            self.ball.speed = None
            self.master.destroy()
        else:
            # Update ball position
            self.ball.update()
            # Get new state
            self.qLearning.get_state(self.getObv())
            # Update Q-table
            self.qLearning.update_table(self.getObv())
            # Next loop
            self.after(1, self.game_loop)

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        return max(self.ball.collide(objects), 1)


def main(qLearning):
    root = tk.Tk()
    root.title('Break those Bricks!')
    game = Game(root, qLearning)
    game.mainloop()


if __name__ == '__main__':
    qLearning = QLearning()
    while True:
        main(qLearning)
