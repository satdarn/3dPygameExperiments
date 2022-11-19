import pygame
import numpy as np
from math import cos, sin, pi, sqrt

class ThreeDShapes:
    Shapes = {}
    def returnShapes(self):
        return list(self.Shapes.values())
    class RegularPolyganicPrism:
        def __init__(self, id, dimentions, pos, angle):
            self.id = id
            self.pos = pos
            self.angle = angle
            self.dimentions = dimentions
            self.update(self.id, self.dimentions, self.pos, self.angle)
        def returnState(self):
            state = [self.id, self.sides, self.radius, self.depth, self.posX, self.posY, self.posZ, self.rotX, self.rotY, self.rotZ]
            return state
        def update(self, id, dimentions, pos, angle):
            self.pos = pos
            self.angle = angle
            self.dimentions = dimentions
            self.posX, self.posY, self.posZ = self.pos
            self.rotX, self.rotY, self.rotZ = angle
            self.sides, self.radius, self.depth = self.dimentions
            self.points = []
            for n in range(0, self.sides):
                x = (self.radius/2)*cos(2*n*pi/self.sides) + self.posX
                y = (self.radius/2)*sin(2*n*pi/self.sides) + self.posY
                z = self.depth/2 + self.posZ
                self.points.append(np.array([x,y,z]))
            for n in range(0, self.sides):
                x = (self.radius/2)*cos(2*n*pi/self.sides) + self.posX
                y = (self.radius/2)*sin(2*n*pi/self.sides) + self.posY
                z = self.posZ -self.depth/2
                self.points.append(np.array([x,y,z]))   
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
    shape1 = shapes.RegularPolyganicPrism("box1",(5,100,100), (0,0,0), (0,0,0))
    clock = pygame.time.Clock()
    clock.tick(60)
    drawInfo = DrawInfo(500,500)
    posX = 0
    posY = 0
    posZ = 0
    rotX = 0
    rotY = 0
    rotZ = 0 
    nsides = 3
    while not drawInfo.exit:
        for event in pygame.event.get():
            shapeInfo = shape1.returnState()
            if event.type == pygame.QUIT:
                drawInfo.exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    posX -= 10
                if event.key == pygame.K_d:
                    posX += 10

                if event.key == pygame.K_w:
                    posY -= 10
                if event.key == pygame.K_s:
                    posY += 10
                
                if event.key == pygame.K_r:
                    rotX += 10
                if event.key == pygame.K_f:
                    rotX -= 10

                if event.key == pygame.K_t:
                    rotY += 10
                if event.key == pygame.K_g:
                    rotY -= 10

                if event.key == pygame.K_y:
                    rotZ += 10
                if event.key == pygame.K_h:
                    rotZ -= 10
                
                if event.key == pygame.K_i:
                    nsides += 1
                if event.key == pygame.K_o:
                    nsides -= 1

        drawInfo.canvas.fill(drawInfo.BLACK)
        cartesianShapes = ThreeDtoCartesian(shapes.returnShapes())
        pyGameShapes = cartesianToPygame(drawInfo, cartesianShapes)
        drawShapes(drawInfo, pyGameShapes)
        shape1.update(shapeInfo[0], (nsides,shapeInfo[2],shapeInfo[3]), (posX,posY,posZ), (rotX,rotY,rotZ))
        pygame.display.update()

if __name__ == "__main__":
    main()