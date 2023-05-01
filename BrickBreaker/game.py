import random
import tkinter as tk


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
        # Ball radius
        self.radius = 10
        # Initial ball direction
        ball_direction = [-1, 1]
        self.direction = [random.choice(ball_direction), ball_direction[game_mode]]
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
        self.horizontal_collision(coords)
        self.vertical_collision(coords)
        # Get new ball displacement
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        # Move ball
        self.move(x, y)

    def horizontal_collision(self, coords):
        if coords[0] <= 0 or coords[2] >= self.canvas_width:
            self.direction[0] *= -1

    def vertical_collision(self, coords):
        if coords[3] >= self.canvas_height if self.game_mode else coords[1] <= 0:
            self.direction[1] *= -1

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
        self.height = 7
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
    def __init__(self, master, game_settings, bricks, qLearning, runs, results, dimensions, exclude_failure):
        super(Game, self).__init__(master)

        self.exclude_failure = exclude_failure
        self.game_settings = game_settings
        self.dimensions = dimensions
        self.bricks = bricks

        [self.ball_speed, self.paddle_speed, self.game_mode, self.episodes] = self.game_settings

        self.qLearning = qLearning
        self.runs = runs
        self.results = results

        [self.width, self.height] = self.dimensions
        self.canvas = tk.Canvas(self, bg='#D6D1F5',
                                width=self.width,
                                height=self.height, )
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.paddle = self.add_paddle()
        self.ball = self.add_ball()

        # Paddle movement
        self.actions = [self.paddle.moveLeft, self.paddle.moveRight, self.paddle.doNothing]

        self.setup_game()
        self.canvas.focus_set()

    def setup_game(self):
        self.place_bricks()
        self.qLearning.new_episode(self.getObv())
        self.update_text()
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

    def place_bricks(self):
        # Brick count
        brick_rows = len(self.bricks)
        bricks_in_row = len(self.bricks[0])
        # Brick dimensions
        brick_width = self.width / bricks_in_row
        brick_height = 20
        # Brick loop
        for y in range(brick_rows):
            for x in range(bricks_in_row):
                # Brick variables
                brick_x = (x + 0.5) * brick_width
                offset = y * brick_height + 50
                brick_y = self.select_value(self.height - offset, offset)
                hits = self.bricks[y][x]
                # Brick creation
                brick = Brick(self.canvas, brick_x, brick_y, hits, brick_width, brick_height)
                self.items[brick.item] = brick

    def select_value(self, first, second):
        return first if self.game_mode else second

    def update_text(self):
        run_text = "Runs: " + str(self.qLearning.runs + 1)
        self.create_text(55, run_text)
        episode_text = "Episodes: " + str(self.qLearning.episode)
        self.create_text(300, episode_text)
        failed_text = "Failed: " + str(self.qLearning.runs - len(self.results))
        self.create_text(535, failed_text)

    def create_text(self, x, text):
        y = self.select_value(self.height - 20, 20)
        self.canvas.create_text(x, y, text=text, font=('Forte', 15))

    def getObv(self):
        return [self.paddle.get_position(), self.ball.get_position()]

    def game_loop(self):
        # Get action
        action = self.qLearning.select_action()
        # Get opposite observation
        opposite_obv = self.opposite_action(action)
        # Perform action
        self.actions[action]()
        # Check for collision
        self.check_collisions()
        # Update Q-Learning policy
        self.qLearning.update_policy(self.getObv(), opposite_obv, action, self.out_of_bounds())
        # Get number of bricks
        num_bricks = len(self.canvas.find_withtag('brick'))
        # Get number of episode
        episode = self.qLearning.episode
        # Check brick conditions
        if num_bricks == 0:
            # Append result and reset run
            self.reset_run(episode, True)
            # Check if sufficient runs
            self.reset_game()
        elif self.out_of_bounds():
            # Check if exceed episodes
            if episode >= self.episodes:
                self.reset_run(self.episodes, False)
            # Check if sufficient runs
            self.reset_game()
        else:
            # Update ball position
            self.ball.update()
            # Next loop
            self.after(1, self.game_loop)

    def reset_run(self, episode, success):
        # Append result
        if success or not self.exclude_failure: self.results.append(episode)
        # Start new run
        self.qLearning.new_run()
        # Print episode num
        print("Run %d finished in %d episodes" % (self.qLearning.runs, episode))

    def reset_game(self):
        # Close window
        self.destroy()
        # Quit or continue
        if len(self.results) < self.runs:
            # Start new game
            self.__init__(self.master, self.game_settings, self.bricks, self.qLearning,
                          self.runs, self.results, self.dimensions, self.exclude_failure)
        else:
            self.results.append(self.qLearning.runs)
            self.master.quit()

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)

    def out_of_bounds(self):
        ball_coords = self.ball.get_position()
        return ball_coords[1] <= 0 if self.game_mode else ball_coords[3] >= self.height

    def opposite_action(self, action):
        # Move paddle
        def move(coords, dist):
            coords[0] += dist
            coords[2] += dist
        # Get initial position
        paddle_coords = self.paddle.get_position()
        # Paddle offset
        offset = self.paddle.offset
        # Get opposite action
        opposite_action = 1 - action
        # Move paddle
        if opposite_action == 0 and paddle_coords[0] - offset >= 0:
            move(paddle_coords, -offset)
        elif opposite_action == 1 and paddle_coords[2] + offset <= self.width:
            move(paddle_coords, offset)
        return [paddle_coords, self.ball.get_position()]