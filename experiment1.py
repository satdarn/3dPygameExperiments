import pygame
import numpy as np
from math import cos, sin, pi, sqrt

class ThreeDShapes:
    Shapes = {}
    def returnShapes(self):
        return list(self.Shapes.values())
    class Box:
        def __init__(self, id, dimentions, pos, angle):
            self.id = id
            self.pos = pos
            self.angle = angle
            self.dimentions = dimentions
            self.update(self.dimentions, self.pos, self.angle)
        def update(self, dimentions, pos, angle):
            self.pos = pos
            self.angle = angle
            self.dimentions = dimentions
            self.posX, self.posY, self.posZ = self.pos
            self.length, self.height, self.depth = self.dimentions
            left, right = self.posX-(self.length/2), self.posX + (self.length/2)
            up, down = self.posY + (self.height/2),self.posY - (self.height/2)
            fwd, back = self.posZ + (self.depth/2), self.posZ - (self.depth/2)
            self.point1 = np.array([left, up, fwd])
            self.point2 = np.array([right, up, fwd])
            self.point3 = np.array([left, down, fwd])
            self.point4 = np.array([right, down, fwd])
            self.point5 = np.array([left, up, down])
            self.point6 = np.array([right, up, down])
            self.point7 = np.array([left, down, down])
            self.point8 = np.array([right, down, down])
            self.points = [self.point1, self.point2, self.point3, self.point4,
                           self.point5, self.point6, self.point7, self.point8]
            ThreeDShapes.Shapes[self.id] = (self.points, self.angle)
            

class Matrix:
    projection = np.matrix([
        [1, 0, 0],
        [0, 1, 0]
    ])
    def rotX(theta):
        radians = theta * (pi/180)
        rotationX = np.matrix([
            [1, 0, 0],
            [0, cos(radians), -sin(radians)],
            [0, sin(radians), cos(radians)]
        ])
        return rotationX

    def rotY(theta):
        radians = theta * (pi/180)
        rotationY = np.matrix([
            [cos(radians),0,sin(radians)],
            [0,1,0],
            [-sin(radians), 0, cos(radians)]
        ])
        return rotationY
    
    def rotZ(theta):
        radians = theta * (pi/180)
        rotationZ = np.matrix([
            [cos(radians),-sin(radians), 0],
            [sin(radians),cos(radians),0],
            [0,0,1]
        ])
        return rotationZ



class DrawInfo:
    BLACK  = 0,0,0
    WHITE  = 255,255,255
    RED  = 255,0,0
    GREEN  = 0,255,0
    BLUE = 0,0,255
    BACKGROUND_COLOR = WHITE
    def __init__(self, width, height):
        self.width = width
        self.height = height
        pygame.init()
        # CREATING CANVAS
        self.canvas = pygame.display.set_mode((width, height))
  
        # TITLE OF CANVAS
        pygame.display.set_caption("Experiment1")
        self.exit = False

def drawShapes(drawInfo, shapes = []):
    for shape in shapes:
        for point in shape:
            pygame.draw.circle(drawInfo.canvas, drawInfo.GREEN, point, 5)
        
def cartesianToPygame(drawInfo, cartesianShapes = []):
    pyGameShapes = []
    width = drawInfo.width
    height = drawInfo.height
    for shape in cartesianShapes: 
        pyGameShape = []
        for point in shape:
            x, y = point
            pyX = x + (width/2)
            pyY = y + (height/2)
            pyGameShape.append((pyX,pyY))
        pyGameShapes.append(pyGameShape)
    return pyGameShapes

def ThreeDtoCartesian(ThreeDShapes):
    cartesianShapes = []
    for shape in ThreeDShapes:
        points, angles = shape
        degX,degY,degZ = angles
        cartesianShape = []
        for point in points:
            rotatedX = np.dot(Matrix.rotX(degX), point.reshape((3,1)))
            rotatedY = np.dot(Matrix.rotY(degY), rotatedX)
            rotatedZ = np.dot(Matrix.rotZ(degZ), rotatedY)
            projected2d = np.dot(Matrix.projection, rotatedZ)
            x = int(projected2d[0][0])
            y = int(projected2d[1][0])
            cartesianShape.append((x,y))
        cartesianShapes.append(cartesianShape)
    return cartesianShapes



def main():
    shapes = ThreeDShapes()
    box1 = shapes.Box("box1",(100,100,100), (0,0,0), (0,0,0))
    box2 = shapes.Box("box2", (50,50,50),(0,0,0), (0,0,0))
    print(shapes.Shapes)
    clock = pygame.time.Clock()
    x = 0
    y = 0
    z = 0
    clock.tick(60)
    drawInfo = DrawInfo(500,500)  
    while not drawInfo.exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drawInfo.exit = True
        drawInfo.canvas.fill(drawInfo.BLACK)
        cartesianShapes = ThreeDtoCartesian(shapes.returnShapes())
        pyGameShapes = cartesianToPygame(drawInfo, cartesianShapes)
        drawShapes(drawInfo, pyGameShapes)
        box1.update((100,100,100), (0, 0, 0), (x,y,z))
        box2.update((50,50,50),(0,0,0),(-x,-y,-z))
        if x < 180:
            x += 0.1
        elif y < 180:
            y += 0.1
        elif z < 180:
            z += 0.1
        pygame.display.update()

if __name__ == "__main__":
    main()