import tkinter as tk
import time

class MyRectangle:
	def __init__(self, canv, coord_matrix):
		self.canv = canv
		self.coord_matrix = []
		self.base_angle = 1
		side_1 = ((coord_matrix[0][0] - coord_matrix[3][0])**2 
			+ (coord_matrix[0][1] - coord_matrix[3][1])**2)**0.5
		side_2 = ((coord_matrix[0][0] - coord_matrix[1][0])**2 
			+ (coord_matrix[0][1] - coord_matrix[1][1])**2)**0.5
		self.max_side = max(side_1, side_2)
		
		for i in coord_matrix:
			self.coord_matrix.append([])
			insert_index = len(self.coord_matrix)
			for j in i:
				self.coord_matrix[insert_index - 1].append(j)

			self.coord_matrix[len(self.coord_matrix) - 1].append(1)
		bx = self.coord_matrix[self.base_angle][0];
		by = self.coord_matrix[self.base_angle][1];
		self.moving_matrix = [[],[],[]]
		self.moving_matrix[0].extend([0, -1, bx + by])
		self.moving_matrix[1].extend([1, 0, -bx + by])
		self.moving_matrix[2].extend([0, 0, 1])

	def step(self):
		self.print(1)
		new_matrix = [[], [], [], []]
		for i in range(4):
			new_matrix[i].append(self.coord_matrix[i][0]*self.moving_matrix[0][0] +
				self.coord_matrix[i][1]*self.moving_matrix[0][1] +
				self.coord_matrix[i][2]*self.moving_matrix[0][2])
			new_matrix[i].append(self.coord_matrix[i][0]*self.moving_matrix[1][0] +
				self.coord_matrix[i][1]*self.moving_matrix[1][1] +
				self.coord_matrix[i][2]*self.moving_matrix[1][2])
			new_matrix[i].append(self.coord_matrix[i][0]*self.moving_matrix[2][0] +
				self.coord_matrix[i][1]*self.moving_matrix[2][1] +
				self.coord_matrix[i][2]*self.moving_matrix[2][2])
		for i in range(len(new_matrix)):
			for j in range(len(new_matrix[i])):
				self.coord_matrix[i][j] = new_matrix[i][j]
		self.base_angle += 1
		if self.base_angle > 3:
			self.base_angle = 0
		bx = self.coord_matrix[self.base_angle][0];
		by = self.coord_matrix[self.base_angle][1];
		self.moving_matrix[0][2] = bx + by
		self.moving_matrix[1][2] = -bx + by
		self.print()


	def print(self, is_deleted = 0):
		small_side_color = "lightgray"
		color = "lightgray"
		if is_deleted == 0:
			color = "red"
			small_side_color = "green"
		canv.create_line(self.coord_matrix[0][0], self.coord_matrix[0][1],
			self.coord_matrix[1][0], self.coord_matrix[1][1], width = 3, fill = small_side_color)
		canv.create_line(self.coord_matrix[1][0], self.coord_matrix[1][1],
			self.coord_matrix[2][0], self.coord_matrix[2][1], width = 3, fill = color)
		canv.create_line(self.coord_matrix[2][0], self.coord_matrix[2][1],
			self.coord_matrix[3][0], self.coord_matrix[3][1], width = 3, fill = color)
		canv.create_line(self.coord_matrix[3][0], self.coord_matrix[3][1],
			self.coord_matrix[0][0], self.coord_matrix[0][1], width = 3, fill = color)

	def is_exited_borders(self, main_width, main_height):
		max_y = self.coord_matrix[self.base_angle][1]
		buf = self.base_angle
		if buf > 3:
			buf = 0
		max_x = self.coord_matrix[buf][1]
		if max_x + self.max_side >= main_width or max_y + self.max_side >= main_height:
			return True
		return False

	def move(self, root, main_width, main_height):
		if self.is_exited_borders(main_width, main_height):
			return;
		self.step()
		wait_time = 500
		if self.base_angle == 1:
			wait_time = 2000
		root.after(wait_time, lambda: self.move(root, main_width, main_height))

main_width = 700
main_height = 700
coord_matrix = [[100, 100], [150, 150], [250, 50], [200, 0]]

root = tk.Tk()
root.title("Test example")
root.minsize(width = main_width, height = main_height)

canv = tk.Canvas(root, width = main_width, height = main_height, bg = 'lightgray')

rect = MyRectangle(canv, coord_matrix)
rect.print()
root.after(2000, lambda: rect.move(root, main_width, main_height))

canv.pack()
root.mainloop()