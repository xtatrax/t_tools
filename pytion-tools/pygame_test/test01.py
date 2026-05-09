#!python3
# Pygameの基本的な使い方をテストするコード
# 試しに三角関数と円と波の関係を可視化したい

import pygame
from pygame.locals import *
import sys

class Color:
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	YELLOW = (255, 255, 0)
	MAGENTA = (255, 0, 255)
	CYAN = (0, 255, 255)
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b
	@classmethod
	def fromTuple(cls, colorCode3: tuple):
		return cls(colorCode3[0], colorCode3[1], colorCode3[2])
	def getTuple(self):
		return (self.r, self.g, self.b)
		pass

#
class Size:
	# コンストラクタのオーバーロード width, height
	def __init__(self, width, height):
		self.width = width
		self.height = height
	# コンストラクタのオーバーロード tuple
	@classmethod
	def fromTuple(cls, tuple: tuple):
		return cls(tuple[0], tuple[1])

	# タプルで返す
	def getTuple(self):
		return (self.width, self.height)
	
	# Width
	def getWidth(self):
		return self.width
	# Height
	def getHeight(self):
		return self.height
	# 割り算オーバーロード
	def __add__(self, other):
		if type(other) == Size:
			return Size(self.width + other.getWidth(), self.height + other.getHeight())
		elif type(other) == tuple:
			return Size(self.width + other[0], self.height + other[1])
		elif type(other) == int or type(other) == float:
			return Size(self.width + other, self.height + other)
		elif type(other) == Point:
			return Point(self.width + other.getX(), self.height + other.getY())
		else:
			raise TypeError("Invalid type for addition")
	def __truediv__(self, other: tuple):
		return Size(self.width / other[0], self.height / other[1])
	def __truediv__(self, other: int):
		return Size(self.width / other, self.height / other)
	def __truediv__(self, other: float):
		return Size(self.width / other, self.height / other)
	# def __truediv__(self, other: Size):
	# 	return Size(self.width / other.getWidth(), self.height / other.getHeight())
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	@classmethod
	def fromSize(cls, size: Size):
		return cls(size.getWidth(), size.getHeight())
	@classmethod
	def fromTuple(cls, tuple: tuple):
		return cls(tuple[0], tuple[1])
	def __add__(self, other: 'Point'):
		return Point(self.x + other.x, self.y + other.y)
	def __add__(self, other: 'Size'):
		return Point(self.x + other.getWidth(), self.y + other.getHeight())
	def getTuple(self):
		return (self.x, self.y)
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	
class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def getTuple(self):
		return (self.x, self.y)
	def getX(self):
		return self.x
	def getY(self):
		return self.y

class Rect:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	@classmethod
	def fromPointAndSize(cls, point: Point, size: Size):
		return cls(point.getX(), point.getY(), size.getWidth(), size.getHeight())
	@classmethod
	def fromTuple(cls, tuple: tuple):
		return cls(tuple[0], tuple[1], tuple[2], tuple[3])

	def getTuple(self):
		return (self.x, self.y, self.width, self.height)

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height
	def getSize(self):
		return Size(self.width, self.height)

class Object:
	def __init__(self, point: Point):
		self.children = []
		self.parent = None
		self.position = point


	def addChild(self, child: 'Object'):
		self.children.append(child)
		child.___setParent(self)

	def ___setParent(self, parent: 'Object'):
		self.parent = parent

	def getPos(self)-> Point:
		return self.position

	def getWorldPos(self) -> Point:
		if(self.parent == None):
			return self.getPos()
		else:
			return self.parent.getWorldPos() + self.getPos()
			pass
	def update(self):
		pass
	def draw(self, screen):
		for child in self.children:
			child.draw(screen)
		pass

class World(Object):
	def __init__(self, point: Point):
		super().__init__(point)

class Circle(Object):
	def __init__(self, color: Color, point: Point, radius: int, weight: int = 1):
		super().__init__(point)
		self.radius = radius
		if type(color) == tuple:
			self.color = Color.fromTuple(color)
		elif type(color) == Color:
			self.color = color
		else:
			raise TypeError("Invalid color type")
		self.weight = weight
	def getRadius(self):
		return self.radius
	def update(self):
		pass
	def draw(self, screen):
		pygame.draw.circle(
			screen,
			self.color.getTuple(),
			self.getWorldPos().getTuple(),
			self.radius,
			self.weight
		)
		super().draw(screen)
		


screen_size = Size(800, 600)    # 画面の大きさを指定
main_circle = Circle(Color.GREEN, screen_size / int(2), 50, 2)
main_circle.addChild(Circle(Color.RED, Point(-main_circle.getRadius() , 0), 8, 0))
def main_loop(screen):
	screen.fill(Color.WHITE)        # 画面を黒色に塗りつぶし
	pygame.draw.line(
		screen,
		Color.BLACK,
		(0,screen_size.getHeight()/2),
		(screen_size.getWidth(), screen_size.getHeight()/2)
	)  # 上下中央線
	pygame.draw.line(
		screen,
		Color.BLACK,
		(screen_size.getWidth()/2, 0),
		(screen_size.getWidth()/2, screen_size.getHeight())
	)  # 左右中央線
	main_circle.draw(screen)
	pass

def main():
	pygame.init()                                   # Pygameの初期化
	screen = pygame.display.set_mode(screen_size.getTuple())    # 画面の大きさを指定
	pygame.display.set_caption("テスト")              # 画面上部に表示するタイトルを設定
	while (1):
		main_loop(screen)
		pygame.display.update()     # 画面を更新
		# イベント処理
		for event in pygame.event.get():
			if event.type == QUIT:  # 閉じるボタンが押されたら終了
				pygame.quit()       # Pygameの終了(画面閉じられる)
				sys.exit()


if __name__ == "__main__":
	main()