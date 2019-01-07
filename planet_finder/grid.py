from planet_finder.distance import euclidean_distance


class Grid:
    def __init__(self, cascade, delta_intensity):
        self.cascade = cascade
        self.delta_intensity = delta_intensity
        self.bomb_location = None
        self.cells = [[0 for i in range(self.delta_intensity)] for j in range(self.cascade)]
        self.drawn = [[False for i in range(self.delta_intensity)] for j in range(self.cascade)]

    def init_bomb(self, x, y, strength=10):
        self.bomb_location = [x, y]
        current_strength = strength
        offset = 0
        while current_strength > 0:
            for x_offset in range(-offset, offset + 1):
                for y_offset in range(-offset, offset + 1):
                    if (self.bomb_location[0] + x_offset >= 0) and (
                            self.bomb_location[1] + y_offset >= 0) and (
                            self.bomb_location[0] + x_offset < self.cascade) and (
                            self.bomb_location[1] + y_offset < self.delta_intensity):
                        if (self.cells[self.bomb_location[0] + x_offset][self.bomb_location[1] + y_offset]) \
                                < current_strength:
                            self.cells[self.bomb_location[0] + x_offset][
                                self.bomb_location[1] + y_offset] = current_strength
            offset = offset + 1
            current_strength = current_strength - 1

    def split_grid(self, starting_x, starting_y, cascade, delta_intensity):
        new_grid = Grid(cascade, delta_intensity)
        for x in range(starting_x, starting_x + cascade):
            for y in range (starting_y, starting_y + delta_intensity):
                new_grid.cells[x-starting_x][y-starting_y] = self.cells[x][y]
        return new_grid

    def __str__(self):
        grid_string = 'Grid\n'
        for y in range(self.delta_intensity):
            for x in range(self.cascade):
                if self.cells[x][y] > 0:
                    grid_string += '[' + str("%2.1f" % self.cells[x][y]) + ']'
                else:
                    grid_string += '[' + '  ' + ']'
            grid_string += '\n'
        return grid_string

    def semivariance(self):
        data = []
        for y0 in range(self.delta_intensity):
            for x0 in range(self.cascade):
                if self.cells[x0][y0] > 0:
                    for h in range(1, self.cascade):
                        temp = []
                        for hY in range(-h, h+1):
                            for hX in range(-h, h+1):
                                if abs(hX)+abs(hY) == h and x0 + hX < self.cascade and y0+hY < self.delta_intensity and x0 + hX >= 0 and y0 + hY >= 0:
                                    temp.append(abs(self.cells[x0][y0] - self.cells[x0+hX][y0+hY]))
                        if len(data) > h-1:
                            data[h-1].extend(temp)
                        else:
                            data.append(temp)
        lag = 1
        print ('Lag,', 'SV')
        for i in data:
            gamma = 0
            for point in i:
                gamma += pow(point, 2)
            gamma = 1 / (2 * len(i)) * gamma
            print(lag, ',', gamma)
            lag += 1
        print(self)

    def semivariance_analog(self):
        data = []
        stupid = []
        for y0 in range(self.delta_intensity):
            for x0 in range(self.cascade):
                for x1 in range(self.cascade):
                    for y1 in range(self.delta_intensity):
                        h = int(euclidean_distance(x0, y0, x1, y1)*1000)
                        z = abs(self.cells[x0][y0] - self.cells[x1][y1])
                        data.append(z)
        print('Lag,', 'SV')
        for row in data:
            lag = row[0]
            gamma = (1 / 2) * row[1]
            print(lag, ',', gamma)




if __name__ == "__main__":
    grid = Grid(32, 32)
    grid.init_bomb(15, 15, 10)
    grid.semivariance_analog()

