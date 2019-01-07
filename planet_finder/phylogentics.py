from planet_finder.grid import Grid


class Phylogentics:
    def __init__(self, id, grid, starting_point, slow=False):
        self.id = id
        self.grid = grid
        self.starting_point = starting_point
        self.current_location = starting_point
        self.done = False
        self.bomb_found = False
        self.last_reading = 0
        self.fast = not slow
        self.max = 0
        self.max_location = [0,0]
        self.row_direction = 1
        self.x_direction = 1
        self.y_direction = 0
        self.manual_driving = False
        self.goal = [0, 0]

    def __str__(self):
        if self.manual_driving:
            grid_string = 'Robot ' + str(self.id) + ' ' + ' Manual Driving '
            grid_string += str("(%2d,%2d)" % (
            self.x_direction, self.y_direction)) + ')\n'
        elif not self.done:
            grid_string = 'Robot ' + str(self.id) + ' ' + ' Active '
        else:
            grid_string = 'Robot ' + str(self.id) + ' ' + ' Idle '
        grid_string += str("(%2d,%2d)" % (self.current_location[0], self.current_location[1])) + ')\n'
        return grid_string

    def on_grid(self):
        if 0 <= self.current_location[0] < self.grid.width and 0 <= self.current_location[1] < self.grid.height:
            return True
        else:
            self.done = True
            return False

    def measure(self):
        if self.on_grid():
            result = self.grid.cells[self.current_location[0]]\
                [self.current_location[1]]
            if result == 0:
                result = 0.0001
            return result
        else:
            print('Robot ', self.id, 'is off the grid', self.current_location[0], ',', self.current_location[1])
            return 0;

    def share(self, robots):
        for robot in robots:
            if robot.id is not self.id:
                robot.add_max_to_heat_map(self.max, self.max_location)

    def add_max_to_heat_map(self, other_max, max_location):
        # self.heat_map.cells[max_location[0]][max_location[1]] = other_max
        pass

    def manual_drive(self, x, y):
        if self.goal[0] != x or self.goal[1] != y:
            self.manual_driving = True
            self.goal[0] = x
            self.goal[1] = y

    def go(self):
        if self.on_grid() and self.done is not True and self.bomb_found is not True:
            if self.measure() >= self.max:
                self.max = self.measure()
                self.max_location[0] = self.current_location[0]
                self.max_location[1] = self.current_location[1]
                # self.heat_map.cells[self.max_location[0]][self.max_location[1]] = self.max

            if self.measure() == 10:
                self.bomb_found = True
                self.done = True
            else:
                if self.manual_driving:
                    deltaX = self.goal[0] - self.current_location[0]
                    deltaY = self.goal[1] - self.current_location[1]
                    if deltaX is not 0:
                        self.x_direction = int(deltaX / abs(deltaX))
                    else:
                        self.x_direction = 0
                    if deltaY is not 0:
                        self.y_direction = int(deltaY / abs(deltaY))
                    else:
                        self.y_direction = 0
                elif self.fast and self.measure() - self.max <= -2 and \
                        self.measure() < self.last_reading:
                    if self.current_location[1] - 2 < 0:
                        self.y_direction = 0
                        self.x_direction = 0
                    elif self.x_direction != 0:
                        self.y_direction = -2
                        self.x_direction = 0
                        self.row_direction = self.row_direction * -1
                    else:
                        self.y_direction = -2
                        self.x_direction = 0
                        self.row_direction = self.row_direction * 1
                elif self.fast and self.measure() < self.last_reading:
                        if self.current_location[1] + 1 == self.grid.height:
                            self.done = True
                            self.y_direction = 0
                            self.x_direction = 0
                        elif self.y_direction == 1:
                            self.y_direction = 1
                            self.x_direction = 0
                        else:
                            self.y_direction = 1
                            self.x_direction = 0
                        self.row_direction = self.row_direction * -1
                else:
                    if (self.current_location[0] + self.x_direction) == self.grid.width or (self.current_location[0] +
                                                                                            self.x_direction) <= -1:
                        if self.current_location[1] + 1 == self.grid.height:
                            self.done = True
                            self.y_direction = 0
                            self.x_direction = 0
                        else:
                            self.y_direction = 1
                            self.x_direction = 0
                            self.row_direction = self.row_direction * -1
                    else:
                        self.y_direction = 0
                        self.x_direction = self.row_direction
                self.last_reading = self.measure()
                #TODO: this is a hack
                if self.current_location[0] + self.x_direction == -1 or \
                    self.current_location[0] + self.x_direction == self.grid.width:
                    self.x_direction = -1 * self.x_direction

                self.current_location[0] += self.x_direction
                self.current_location[1] += self.y_direction
                if self.manual_driving and \
                        self.current_location[0] == self.goal[0] and \
                        self.current_location[1] == self.goal[1]:
                    self.manual_driving = False
                    self.y_direction = 0
                    self.x_direction = self.row_direction
                    self.max = 0

