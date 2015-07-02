#!/usr/bin/python

import random
import pygame,sys,math
import PyParticles
from pygame.locals import *

ANCHO=1110
ALTO=622

(width, height) = (400, 400)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simulacion gravedad')

universe = PyParticles.Environment((width, height))

pantalla=pygame.display.set_mode((ANCHO,ALTO))

universe.colour = (255,0,0)
universe.addFunctions(['move', 'attract', 'combine', 'bounce'])

def cargar_imagen(filename,transparent=False):
    try: imagen=pygame.image.load(filename)

    except pygame.error, message:
        raise SystemExit, message

    imagen=imagen.convert()
    if transparent:
        color=imagen.get_at((0,0))
        imagen.set_colorkey(color, RLEACCEL)
    return imagen

class BottonStart(pygame.sprite.Sprite):
  def __init__(self,x,y):
    pygame.sprite.Sprite.__init__(self)
    self.imagen=cargar_imagen("images/botonstart.png")
    self.rect=self.imagen.get_rect()
    self.rect.centerx=x
    self.rect.centery=y
  def pressed2(self,mouse):
    if mouse[0]<self.rect.right and mouse[0]> self.rect.left:
      if mouse[1]> self.rect.top and mouse[1]<self.rect.bottom:
        #print "hola"
        return True
    else: return False

class BottonPause(pygame.sprite.Sprite):
  def __init__(self,x,y):
    pygame.sprite.Sprite.__init__(self)
    self.imagen=cargar_imagen("images/botonpause.png")
    self.rect=self.imagen.get_rect()
    self.rect.centerx=x
    self.rect.centery=y
  def pressed2(self,mouse):
    if mouse[0]<self.rect.right and mouse[0]> self.rect.left:
      if mouse[1]> self.rect.top and mouse[1]<self.rect.bottom:
        #print "hola"
        return True
    else: return False
#Calculamos el radio de cada particula
def calculateRadius(mass):
    return 2.5 * mass ** (0.5)

#Creamos las particulas en el display
def crearParticulas(velocidad, cantidad):
    for p in range(cantidad):
        particle_mass = random.randint(1,10)
        particle_size = calculateRadius(particle_mass)
        universe.addParticles(mass=particle_mass, size=particle_size, 
                speed=velocidad, colour=(0,0,255))

def main():
    running = True

    pygame.display.set_caption("Cantidad de movimiento")
    fondo=cargar_imagen("images/fondogravedad.png")
    #pygame.mixer.music.load("sounds/carrera.mp3")
    time=0
    arrancar=False
    press=0
    fuente=pygame.font.Font(None,20)
    bstart=BottonStart(70,510);
    bpause=BottonPause(200, 510);
    reloj=pygame.time.Clock()

    #Variables
    velocidad = 1
    cantidad = 10


    while True:
        tick=reloj.tick(60)

        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                sys.exit(0)
            elif eventos.type == MOUSEBUTTONDOWN:
                if bstart.pressed2(pygame.mouse.get_pos()):
                    #if press==0:
                        arrancar=True
                        #press=1
                if bpause.pressed2(pygame.mouse.get_pos()):
                    #if press2==0:
                        arrancar=False
                        #press2=1
            elif eventos.type == KEYDOWN:
                if eventos.key==K_UP and arrancar==False:
                    cantidad += 1
                    press = 1
                    #crearParticulas(velocidad, cantidad)
                elif eventos.key==K_RIGHT and arrancar==False:
                    velocidad += 0.1
                    press = 1
                    #crearParticulas(velocidad, cantidad)
                elif eventos.key==K_DOWN and arrancar==False:
                    cantidad -= 1
                    press = 1
                    #crearParticulas(velocidad, cantidad)
                elif eventos.key==K_LEFT and arrancar==False:
                    velocidad -= 0.1
                    press = 1

                if press == 1:
                    crearParticulas(velocidad, cantidad)
                    press = 0
                #elif eventos.key==K_UP and arrancar==False:
                    #cantidad
                    #crearParticulas(velocidad, cantidad)
                #elif eventos.key==K_RIGHT and arrancar==False:
                    #auto2.speed[0]=auto2.speed[0]+1 

  
        if arrancar==True:
          time=time+(tick/1000.0)
          screen.fill(universe.colour)
          universe.update()


        #Fondo y Datos
        pantalla.blit(fondo, (0,0))
        datosParticula = "Velocidad: %2f, Cantidad estrellas: %d " %(velocidad,
                cantidad)
        datoTiempo = "Tiempo transcurrido %f s"%(time)
        mensaje1=fuente.render(datosParticula,1,(255,255,255))
        mensaje3=fuente.render(datoTiempo,1,(255,255,255))
        #----------------------------------------------------
        pantalla.blit(fondo, (0,0))
        pantalla.blit(mensaje1,(5,560))
        pantalla.blit(mensaje3,(5,600))
        pantalla.blit(bstart.imagen, bstart.rect)
        pantalla.blit(bpause.imagen, bpause.rect)		
        particles_to_remove = []

        #Colisionamos cada particula
        for p in universe.particles:
            if 'collide_with' in p.__dict__:
                particles_to_remove.append(p.collide_with)
                p.size = calculateRadius(p.mass)
                del p.__dict__['collide_with']

            if p.size < 2:
                pygame.draw.rect(screen, p.colour, (int(p.x), int(p.y), 2, 2))
            else:
                pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), int(p.size), 0)




        for p in particles_to_remove:
            if p in universe.particles:
                universe.particles.remove(p)

        pygame.display.flip()


if __name__=='__main__':
    pygame.init()
    main()
