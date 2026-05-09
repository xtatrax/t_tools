#!python3

# ============================================================
# Pygame の基本テストコード
#
# 目的:
#   - Pygame の描画まわりに慣れる
#   - 座標系クラス(Point / Size / Rect)を自作して遊ぶ
#   - 親子オブジェクトによる相対座標を試す
#   - 三角関数と「円運動 ↔ 波」の関係を可視化する土台を作る
#
# 今後やりたいこと:
#   - sin / cos を使った円運動
#   - 回転点から波形を生成
#   - ベクトル表示
#   - GUIっぽい構造化
# ============================================================

import pygame
from pygame.locals import *
from pygame.math import Vector2
import sys
import math


class Color:
	"""
	RGBカラーを扱う簡易クラス。

	Pygame は tuple (r,g,b) を要求する事が多いので、
	内部表現をクラス化しつつ tuple 変換もできるようにしている。
	"""

	# よく使う色の定数
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
		"""tuple から Color を生成"""
		return cls(colorCode3[0], colorCode3[1], colorCode3[2])

	def getTuple(self):
		"""Pygame 用に tuple へ変換"""
		return (self.r, self.g, self.b)

#
class Size:
	"""
	幅と高さを表すクラス。

	Point と分離することで、
	「位置」と「サイズ」を意味的に区別したい。
	"""

	# width, height 指定
	def __init__(self, width, height):
		self.width = width
		self.height = height

	# tuple から生成
	@classmethod
	def fromTuple(cls, tuple: tuple):
		return cls(tuple[0], tuple[1])

	# tuple へ変換
	def getTuple(self):
		return (self.width, self.height)

	# Width取得
	def getWidth(self):
		return self.width

	# Height取得
	def getHeight(self):
		return self.height

	# 加算演算子オーバーロード
	#
	# Size + Size
	# Size + tuple
	# Size + 数値
	# Size + Point
	#
	# を扱えるようにしている
	def __add__(self, other):

		if type(other) == Size:
			return Size(
				self.width + other.getWidth(),
				self.height + other.getHeight()
			)

		elif type(other) == tuple:
			return Size(
				self.width + other[0],
				self.height + other[1]
			)

		elif type(other) == int or type(other) == float:
			return Size(
				self.width + other,
				self.height + other
			)

		elif type(other) == Point:
			return Point(
				self.width + other.getX(),
				self.height + other.getY()
			)

		else:
			raise TypeError("Invalid type for addition")

	# 画面中央計算などで使いたいので割り算対応
	def __truediv__(self, other):
		if type(other) == int or type(other) == float:
			return Size(self.width / other, self.height / other)
		elif type(other) == Point:
			return Point(self.width / other.getX(), self.height / other.getY())
		elif type(other) == Size:
			return Size(self.width / other.getWidth(), self.height / other.getHeight())
		elif type(other) == tuple:
			return Size(self.width / other[0], self.height / other[1])
		else:
			raise TypeError("Invalid type for division")
class Point:
	"""
	2次元座標クラス。

	pygame の tuple 座標を直接使わず、
	オブジェクト指向的に扱うために用意。
	"""

	def __init__(self, x, y):
		if type(x) == int or type(x) == float:
			if type(y) == int or type(y) == float:
				self.x = x
				self.y = y
			else:
				raise TypeError("Invalid type for y coordinate")
		elif type(x) == Size:
			self.x = x.getWidth()
			self.y = x.getHeight()
		elif type(x) == tuple:
			self.x = x[0]
			self.y = x[1]
		elif type(x) == Vector2:
			self.x = x.x
			self.y = x.y
		else:
			raise TypeError("Invalid type for Point initialization")

	# Point 同士の加算
	#
	# 親子座標の合成などに使う
	def __add__(self, other):
		if type(other) == Point:
			return Point(self.x + other.x, self.y + other.y)
		elif type(other) == Size:
			return Point(self.x + other.getWidth(), self.y + other.getHeight())
		elif type(other) == tuple:
			return Point(self.x + other[0], self.y + other[1])
		elif type(other) == int or type(other) == float:
			return Point(self.x + other, self.y + other)
		elif type(other) == Vector2:
			return Point(self.x + other.x, self.y + other.y)
		else:
			raise TypeError("Invalid type for addition")
	def setPosition(self, other):
		if type(other) == Point:
			self.x = other.x
			self.y = other.y
		elif type(other) == Size:
			self.x = other.getWidth()
			self.y = other.getHeight()
		elif type(other) == tuple:
			self.x = other[0]
			self.y = other[1]
		elif type(other) == int or type(other) == float:
			self.x = other
			self.y = other
		else:
			raise TypeError("Invalid type for setting position")

	def getTuple(self):
		return (self.x, self.y)
	def setX(self, x):
		self.x = x
	def getX(self):
		return self.x
	def setY(self, y):
		self.y = y
	def getY(self):
		return self.y
	
# class Vector:
# 	def __init__(self, x, y):
# 		self.x = x
# 		self.y = y
# 	def getTuple(self):
# 		return (self.x, self.y)
# 	def getX(self):
# 		return self.x
# 	def getY(self):
# 		return self.y

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
	
class Controller():
	def __init__(self):
		self.mouse_pos = Point(0, 0)
		self.key_state = {}

	def update(self):
		# イベント処理
		for event in pygame.event.get():  # イベントを取得
			if event.type == QUIT:        # 閉じるボタンが押されたら終了
				pygame.quit()             # Pygameの終了(ないと終われない)
				sys.exit()                # 終了（ないとエラーで終了することになる）
			elif event.type == KEYDOWN:
				self.key_state[event.key] = True
			elif event.type == KEYUP:
				self.key_state[event.key] = False
			elif event.type == MOUSEMOTION:
				self.mouse_pos.setPosition(event.pos)
		pass

class Object:
	"""
	描画オブジェクトの基底クラス。

	シーンツリーっぽい構造を作るため、
	親子関係を持てるようにしている。

	子は親の座標を基準に動く。
	"""

	def __init__(self, point: Point):
		self.children = []
		self.parent = None
		if type(point) == Point:
			self.position = point
		elif type(point) == Size:
			self.position = Point(point.getWidth(), point.getHeight())
		elif type(point) == tuple:
			self.position = Point(point[0], point[1])
		elif type(point) == Vector2:
			self.position = Point(point.x, point.y)
		else:
			raise TypeError("Invalid type for position")

	def addChild(self, child: 'Object'):
		"""子オブジェクト追加"""
		self.children.append(child)
		child.___setParent(self)
	def getChildren(self):
		return self.children
	def ___setParent(self, parent: 'Object'):
		self.parent = parent

	def getPos(self) -> Point:
		"""ローカル座標"""
		return self.position
	def setPos(self, pos):
		if type(pos) == Point:
			self.position = pos
		elif type(pos) == Size:
			self.position = Point(pos.getWidth(), pos.getHeight())
		elif type(pos) == tuple:
			self.position = Point(pos[0], pos[1])
		elif type(pos) == Vector2:
			self.position = Point(pos.x, pos.y)
		else:
			raise TypeError("Invalid type for position")
	def getWorldPos(self) -> Point:
		"""
		親座標を含めたワールド座標を取得。

		親子構造での相対位置計算の核。
		"""

		if(self.parent == None):
			return self.getPos()
		else:
			return self.parent.getWorldPos() + self.getPos()

	def update(self, T: Controller):
		"""毎フレーム更新用"""
		for child in self.children:
			child.update(T)
		pass

	def draw(self, screen):
		"""子オブジェクトも再帰描画"""
		for child in self.children:
			child.draw(screen)

class World(Object):
	def __init__(self,point: Point):
		super().__init__(point)

class Circle(Object):
	"""
	円描画オブジェクト。

	今後:
		- 回転
		- 三角関数
		- 波形生成
		- ベクトル表示

	などの中心になる予定。
	"""

	def __init__(self, color: Color, point: Point, radius: int, weight: int = 1):
		super().__init__(point)

		self.radius = radius

		# tuple / Color 両対応
		if type(color) == tuple:
			self.color = Color.fromTuple(color)

		elif type(color) == Color:
			self.color = color

		else:
			raise TypeError("Invalid color type")

		self.weight = weight

	def getRadius(self):
		return self.radius

	# def update(self, T: Controller):
	# 	pass

	def draw(self, screen):

		# 円描画
		pygame.draw.circle(
			screen,
			self.color.getTuple(),
			self.getWorldPos().getTuple(),
			self.radius,
			self.weight
		)

		# 子オブジェクト描画
		super().draw(screen)

class Line(Object):
	def __init__(self, color: Color, start: Point, degree: float = 0, length: float = 1, weight: int = 1):
		super().__init__(start)
		self.vec = Vector2(1, 0).rotate(degree) * length
		self.endPos = Point(self.vec.x, self.vec.y)
		self.degree = degree
		self.length = length

		# tuple / Color 両対応
		if type(color) == tuple:
			self.color = Color.fromTuple(color)
		elif type(color) == Color:
			self.color = color
		else:
			raise TypeError("Invalid color type")
		self.weight = weight

	def getWorldEndPos(self):
		if(self.parent == None):
			return self.endPos
		else:
			return super().getWorldPos() + self.endPos
	def setDegree(self, degree):
		self.degree = degree
	def getDegree(self):
		return self.degree
	def setLength(self, length):
		self.length = length
	def getLength(self):
		return self.length

	def update(self, T: Controller):
		self.vec = Vector2(1, 0).rotate(self.degree) * self.length
		self.endPos = Point(self.vec.x, self.vec.y)
		pass

	def draw(self, screen):
		pygame.draw.line(
			screen,
			self.color.getTuple(),
			self.getWorldPos().getTuple(),
			self.getWorldEndPos().getTuple(),
			self.weight
		)
		super().draw(screen)
class RLine(Line):
	def __init__(self, color: Color, start: Point, degree: float = 0, length: float = 1, weight: int = 1):
		super().__init__(color, start, degree, length, weight)
	def update(self, T: Controller):
		super().update(T)
		if(type(self.parent) == MainCircle):

			self.endPos = Vector2(1, 0).rotate(self.parent.getDegree() + self.getDegree() ) * self.parent.getRadius()
		#self.setDegree(self.getDegree() + self.parent.getDegreeOffset())

class PosCircle(Circle):
	def __init__(
		self,
		color: Color,
		basePos: Point,
		radius: int=0,
		degree: float = 0,
		length: float = 1,
		weight: int = 1
	):
		super().__init__(color, basePos, radius, weight)
		# 移動のためのパラメータ
		self.degree = degree
		self.length = length
		# 
		self.bacePos = basePos
		self.vec = Vector2(1, 0).rotate(degree) * length
		self.setPos(Point(basePos.getX() + self.vec.x, basePos.getY() + self.vec.y))
	def update(self, T: Controller):
		if(type(self.parent) == MainCircle):
			self.vec = Vector2(1, 0).rotate(self.parent.getDegree()) * self.parent.getRadius()
			self.setPos(self.vec)

		pass

class MainCircle(Circle):
	def __init__(self, color: Color, point: Point, radius: int, weight: int = 1):
		super().__init__(color, point, radius, weight)
		self.degree = 0
		self.degree_offset = 0
		self.dots = {}
	def getDegree(self):
		return self.degree
	def setDegree(self, degree):
		self.degree = degree
	def getDegreeOffset(self):
		return self.degree_offset
	def setDegreeOffset(self, degree_offset):
		self.degree_offset = degree_offset
	def update(self, T: Controller):
		# メイン円の更新ロジック
		self.position.x = T.mouse_pos.getX()
		self.degree = self.position.getX()
		# vec = Vector2(1, 0).rotate(self.getDegree()) * self.getRadius()
		# vec_str = f"{int(vec.x)},{int(vec.y)}"
		# if vec_str not in self.dots:
		# 	self.dots[vec_str] = Circle(
		# 		Color.RED,
		# 		self.getWorldPos() + vec,
		# 		8,
		# 		0
		# 	)
		# 	self.parent.addChild(self.dots[vec_str])
		super().update(T)

class Transformer(Object):
	pass
# ============================================================
# メイン描画オブジェクト生成
# ============================================================

screen_size = Size(800, 600)
world = World(Point(0, 0))


# 中央に配置するメイン円
main_circle = MainCircle(
	Color.GREEN,
	Point(50, screen_size.getHeight()/2),
	50,
	2
)
world.addChild(main_circle)
# 円周上の点
#
# 今後ここを回転させて
# sin / cos の可視化につなげたい
main_circle.addChild(
	PosCircle(
		Color.RED,
		Point(-main_circle.getRadius(), 0),
		8,
		0
	)
)
main_circle.addChild(
	RLine(
		Color.BLUE,
		Point(0, 0),
		0,
		50,
		2
	)
)
main_circle.addChild(
	RLine(
		Color.BLUE,
		Point(0, 0),
		120,
		50,
		2
	)
)
main_circle.addChild(
	RLine(
		Color.BLUE,
		Point(0, 0),
		240,
		50,
		2
	)
)
mouse_pos = Point(0, 0)
def main_loop(screen, controller):
	controller.update()
	mouse_pos.setPosition(pygame.mouse.get_pos())
	# 背景クリア
	screen.fill(Color.WHITE)

	# X軸
	pygame.draw.line(
		screen,
		Color.BLACK,
		(0, screen_size.getHeight()/2),
		(screen_size.getWidth(), screen_size.getHeight()/2)
	)

	# Y軸
	pygame.draw.line(
		screen,
		Color.BLACK,
		(screen_size.getWidth()/2, 0),
		(screen_size.getWidth()/2, screen_size.getHeight())
	)

	world.update(controller)
	# オブジェクト描画
	world.draw(screen)


def main():

	# Pygame 初期化
	pygame.init()

	# ウインドウ生成
	screen = pygame.display.set_mode(screen_size.getTuple())

	# タイトル設定
	pygame.display.set_caption("テスト")
	controller = Controller()
	while (1):
		start = pygame.time.get_ticks()
		# 1フレーム描画
		main_loop(screen, controller)

		main_loop_time = pygame.time.get_ticks() - start
		print(f"Main loop time: {main_loop_time} ms")

		start = pygame.time.get_ticks()
		# 画面反映
		pygame.display.update()
		display_update_time = pygame.time.get_ticks() - start
		print(f"Display update time: {display_update_time} ms")

		start = pygame.time.get_ticks()
		# イベント処理
		for event in pygame.event.get():

			# ウインドウを閉じたら終了
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		event_processing_time = pygame.time.get_ticks() - start
		print(f"Event processing time: {event_processing_time} ms")	
if __name__ == "__main__":
	main()