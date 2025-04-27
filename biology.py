import pyglet
from pyglet import app, gl, graphics
from pyglet.window import Window
import random as r

class Grass():
    def __init__(self, n, width, height, gmax, color, gft):
        self.width = width
        self.height = height
        self.gmax = gmax
        self.color = color
        self.n = n
        self.grow_for_turn = gft
        self.pole = [[1 for _ in range(n)] for _ in range(n)]

    def Grow(self):
        for _ in range(self.grow_for_turn):
            i = r.randint(0, self.n-1)
            j = r.randint(0, self.n-1)
            if self.pole[i][j] < self.gmax:
                self.pole[i][j] += 1        

class Victim():
    def __init__(self, age, i, j, color, fullness, pole, victims):
        self.age = age
        self.i = i
        self.j = j
        self.color = color
        self.fullness = fullness
        self.victims = victims
        self.pole = pole

    def Find_Rabbit(self, dx, dy):
        for v in self.victims:
            if self.i + dx == v.i and self.j + dy == v.j:
                return True
        return False 
    
    def Find_Hunter(self, dx, dy):
        for h in hunters:
            if self.i + dx == h.i and self.j + dy == h.j:
                return True
        return False 

    def Move(self, fullness_for_move):
        self.Eat()
        dx = r.randint(-1, 1)
        dy = r.randint(-1, 1)
        if not self.Find_Rabbit(dx, dy) and not self.Find_Hunter(dx, dy):
            if 0 <= self.i + dx < len(self.pole[0]):
                self.i += dx
            if 0 <= self.j + dy < len(self.pole[0]):
                self.j += dy
        self.age += 1
        self.fullness -= fullness_for_move
        self.Eat()
        self.GetFamily(fullness_for_move)

    def Eat(self):
        if self.fullness < 50:
            if self.pole[self.i][self.j] > 0:
                self.fullness = 100
                self.pole[self.i][self.j] -= 1

    def GetFamily(self, fullness_for_move):
        if self.age > max_age_victims / 4 and self.fullness >= 9 * fullness_for_move:
            n = int(r.gauss(1, 2)) 
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if n <= 0:
                        break
                    if not self.Find_Rabbit(i, j) and 0 <= self.i + i < len(self.pole) and 0 <= self.j + j < len(self.pole):
                        n -= 1
                        victims.append(Victim(0, self.i + i, self.j + j, (255, 255, 255), 50, grass.pole, victims))
                        self.fullness -= fullness_for_move    
           

class Hunter():
    def __init__(self, age, i, j, color, fullness, pole, victims, hunters):
        self.age = age
        self.i = i
        self.j = j
        self.color = color
        self.fullness = fullness
        self.pole = pole
        self.victims = victims
        self.hunters = hunters
        self.ismama = False

    def Move(self, fullness_for_move_h):
        self.Eat()
        if self.fullness >= 70:
            dx = r.randint(-1, 1)
            dy = r.randint(-1, 1)
            if not self.Find_Rabbit(dx, dy)[0] and not self.Find_Hunter(dx, dy)[0]:
                if 0 <= self.i + dx < len(self.pole[0]):
                    self.i += dx
                if 0 <= self.j + dy < len(self.pole[0]):
                    self.j += dy
        self.age += 1
        self.fullness -= fullness_for_move_h
        self.Eat()
        self.GetFamily(fullness_for_move_h)

    def Find_Rabbit(self, dx, dy):
        for i in range(len(victims)):
            if self.i + dx == victims[i].i and self.j + dy == victims[i].j:
                return (True, i)
        return (False, 0)
    
    def Find_Hunter(self, dx, dy):
        for i in range(len(hunters)):
            if self.i + dx == hunters[i].i and self.j + dy == hunters[i].j:
                return (True, i)
        return (False, 0)

    def Eat(self):
        if self.fullness < 70:
            lst = []
            for v in victims:
                lst.append((v.i, v.j))
            lst = list(map(lambda t: (t[0] - self.i) ** 2 + (t[1] - self.j) ** 2, lst))
            if len(lst) > 0:
                minn = lst.index(min(lst))
                self.i = victims[minn].i
                self.j = victims[minn].j
                self.fullness += victims[minn].age * 2
                if len(victims) > 0:
                    victims.pop(minn)

    def GetFamily(self, fullness_for_move_h):
        if self.age > max_age_hunters / 2 and self.fullness >= 70 * fullness_for_move_h and self.ismama == False:
            n = int(r.gauss(1.5, 1)) 
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if n <= 0:
                        break
                    if not self.Find_Rabbit(i, j)[0] and 0 <= self.i + i < len(self.pole) and 0 <= self.j + j < len(self.pole):
                        n -= 1
                        hunters.append(Hunter(0, self.i + i, self.j + j, (255, 0.4, 0), 50, grass.pole, victims, hunters))
                        self.fullness -= fullness_for_move_h   
            self.ismama = True            


window = pyglet.window.Window(800, 800) #создаем окно
n = 50 #количество клеточек
grow_for_turn = 150 # количество травы за ход
grass = Grass(n, 800, 800, 10, (0, 255, 0), grow_for_turn)
num_victims = 8 #количество зайцев на старте
max_age_victims = 10
fullness_for_move = 10
fullness_for_move_h = 1
victims = [] #зайчики
num_hunters = 20
max_age_hunters = 60
hunters = []
for i in range(num_victims):
    victims.append(Victim(0, r.randint(0, n-1), r.randint(0, n-1), (255, 255, 255), 100, grass.pole, victims))
for j in range(num_hunters):
    hunters.append(Hunter(0, r.randint(0, n-1), r.randint(0, n-1), (255, 0.4, 0), 100, grass.pole, victims, hunters))

def Go(dt):#здесь все ходят
    grass.Grow()
    for v in victims:
        v.Move(fullness_for_move)
    for h in hunters:
        h.Move(fullness_for_move_h)    
    i = 0
    while i < len(victims):
        if victims[i].age > max_age_victims or victims[i].fullness <= 0:
            victims.pop(i)
        else:    
            i += 1 
    j = 0        
    while j < len(hunters):
        if hunters[j].age > max_age_hunters or hunters[j].fullness <= 0:
            hunters.pop(j)
            print('aa')
        else:    
            j += 1         
    s = 0
    for i in range(0, n):
         s += sum(grass.pole[i])
    # file.write(str(s) + ' ' + str(len(victims)) + ' ' + str(len(hunters)) + '\n')           
               

pyglet.clock.schedule_interval(Go, 0.01)

@window.event
def on_draw():#здесь всё рисуется
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(-1, 1, -1, 1, -1, 1)
    k = 2/grass.n
    gl.glBegin(gl.GL_QUADS)
    for i in range(n): #отрисовка травы
        for j in range(n):           
            gl.glColor3f(0, 1/grass.gmax * grass.pole[i][j], 0)
            gl.glVertex2f(-1 + j * k, 1 - (i+1) * k)
            gl.glVertex2f(-1 + (j+1) * k, 1 - (i+1) * k)
            gl.glVertex2f(-1 + (j+1) * k, 1 - i * k)
            gl.glVertex2f(-1 + j * k, 1 - i * k)
    gl.glEnd()
    gl.glBegin(gl.GL_QUADS)
    for v in victims: #отрисовка зайчиков          
        gl.glColor3f(*v.color)
        k_age = k/2 - (v.age * k/2)/max_age_victims + k/max_age_victims/2
        gl.glVertex2f(-1 + (v.j) * k + k_age, 1 - (v.i+1) * k + k_age)
        gl.glVertex2f(-1 + (v.j+1) * k - k_age, 1 - (v.i+1) * k + k_age)
        gl.glVertex2f(-1 + (v.j+1) * k - k_age, 1 - (v.i) * k - k_age)
        gl.glVertex2f(-1 + (v.j) * k + k_age, 1 - (v.i) * k - k_age)
    gl.glEnd()
    gl.glBegin(gl.GL_QUADS)
    for h in hunters: #отрисовка волков         
        gl.glColor3f(*h.color)
        k_age = k/2 - (h.age * k/2)/max_age_hunters + k/max_age_hunters/2
        gl.glVertex2f(-1 + (h.j) * k + k_age, 1 - (h.i+1) * k + k_age)
        gl.glVertex2f(-1 + (h.j+1) * k - k_age, 1 - (h.i+1) * k + k_age)
        gl.glVertex2f(-1 + (h.j+1) * k - k_age, 1 - (h.i) * k - k_age)
        gl.glVertex2f(-1 + (h.j) * k + k_age, 1 - (h.i) * k - k_age)
    gl.glEnd()

app.run()