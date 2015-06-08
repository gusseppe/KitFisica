 #!/usr/bin/env python
# -*- coding: utf-8 -*-
#modulos
import sys, pygame, math
from pygame.locals import *
#contantes
ANCHO=1110
ALTO=622
#--------------------------------------------------
#funciones
#-----------------------------------------------------
def cargar_imagen(filename,transparent=False):
	try: imagen=pygame.image.load(filename)

	except pygame.error, message:
		raise SystemExit, message

	imagen=imagen.convert()
	if transparent:
		color=imagen.get_at((0,0))
		imagen.set_colorkey(color, RLEACCEL)
	return imagen
#-----------------------------------------------------
#clases
#-----------------------------------------------------
class BottonStart(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.imagen=cargar_imagen("../images/botonstart.png")
		self.rect=self.imagen.get_rect()
		self.rect.centerx=x
		self.rect.centery=y
	def pressed2(self,mouse):
		if mouse[0]<self.rect.right and mouse[0]> self.rect.left:
			if mouse[1]> self.rect.top and mouse[1]<self.rect.bottom:
				#print "hola"
				return True
		else: return False
#-----------------------------------------------------
class Auto1(pygame.sprite.Sprite):
	def __init__(self, x):
		pygame.sprite.Sprite.__init__(self)
		self.imagen=cargar_imagen("images/movil2.png",True)
		self.rect=self.imagen.get_rect()
		self.rect.centerx=x
		self.rect.centery=400
		#-----------coordenadas del auto-------------------	
		self.x_ini=x
		self.x_actul=self.x_ini		
		#--------------velocidad---------------------------
		self.speed=[10.0, 0]
	def modificaru(self,x):
		self.rect.centerx=x
		self.x_ini=x;
		self.x_actul=self.x_ini
	def actualizar(self,time,arrancar):
		if arrancar==True:
			self.rect.centerx=self.x_ini+self.speed[0]*time
			self.x_actul=self.rect.centerx
		#self.rect.centery+=self.speed[1]*time
		#---revisando que no se salga del trayecto
		if self.rect.right >=ANCHO:
			self.speed[0]=0
#---------------------------------------------------
class Auto2(pygame.sprite.Sprite):
	def __init__(self,x):
		pygame.sprite.Sprite.__init__(self)
		self.imagen=cargar_imagen("images/movil1.png",True)
		self.rect=self.imagen.get_rect()
		self.rect.centerx=x
		self.rect.centery=350
		#-----coordenadas del auto----------------
		self.x_ini=x;
		self.x_actul=self.x_ini
		#------velocidad del auto-----------------
		self.speed=[20.0, 0]
	def modificaru(self,x):
		self.x_ini=x;
		self.x_actul=self.x_ini
	def actualizar(self,time,arrancar):
		if arrancar==True:
			self.rect.centerx=self.x_ini+self.speed[0]*time
			self.x_actul=self.rect.centerx;
		#self.rect.centery+=self.speed[1]*time
		#---revisando que no se salga del trayecto
		if self.rect.right >=ANCHO:
			self.speed[0]=0			
#-----------------------------------------------------
def main():
	#creando la pantalla del juego
	pantalla=pygame.display.set_mode((ANCHO,ALTO))
	pygame.display.set_caption("Tiempo de alcance")
	fondo=cargar_imagen('images/fondoauto.png')
	pygame.mixer.music.load("sounds/carrera.mp3")
	time=0
	arrancar=False
	press=0
	fuente=pygame.font.Font(None,20)
	auto1=Auto1(200)
	auto2=Auto2(50)
	bstart=BottonStart(70,510);
	reloj=pygame.time.Clock()
	while True:
		tick=reloj.tick(60)
		for eventos in pygame.event.get():
			if eventos.type == QUIT:
				sys.exit(0)
			elif eventos.type == MOUSEBUTTONDOWN:
				if bstart.pressed2(pygame.mouse.get_pos()):
					if press==0:
						arrancar=True
						#pygame.mixer.music.play(loops=-1)
						pygame.mixer.music.play()
						press=1
			elif eventos.type == KEYDOWN:
				if eventos.key==K_a and arrancar==False:
					auto1.rect.centerx=auto1.rect.centerx+1
					auto1.modificaru(auto1.rect.centerx)
				elif eventos.key==K_s and arrancar==False:
					auto2.rect.centerx=auto2.rect.centerx+1
					auto2.modificaru(auto2.rect.centerx)
				elif eventos.key==K_UP and arrancar==False:
					auto1.speed[0]=auto1.speed[0]+1
				elif eventos.key==K_RIGHT and arrancar==False:
					auto2.speed[0]=auto2.speed[0]+1	

		#control del tiempo--------------------------
		if arrancar==True:
			time=time+(tick/1000.0)
		#-----------------------------------------
		auto1.actualizar(time,arrancar)
		auto2.actualizar(time,arrancar)
		#-----------------mostrar informacion--------
		if auto1.x_actul <= auto2.x_actul:
			arrancar=False;
			pygame.mixer.music.stop();
				#-----------------------------------------
		datosAuto1 = "Posicion I: %d m  Velocidad: %3d m/s X: %d m" %(auto1.x_ini,auto1.speed[0],auto1.x_actul)
		datosAuto2 = "Posicion I: %d m  Velocidad: %3d m/s X: %d m" %(auto2.x_ini,auto2.speed[0],auto2.x_actul)
		datoTiempo = "Tiempo transcurrido %f s"%(time)
		mensaje1=fuente.render(datosAuto1,1,(255,255,255))
		mensaje2=fuente.render(datosAuto2,1,(255,255,255))
		mensaje3=fuente.render(datoTiempo,1,(255,255,255))
		#----------------------------------------------------
		pantalla.blit(fondo, (0,0))
		pantalla.blit(mensaje1,(5,560))
		pantalla.blit(mensaje2,(5,580))
		pantalla.blit(mensaje3,(5,600))
		pantalla.blit(auto1.imagen, auto1.rect)
		pantalla.blit(auto2.imagen, auto2.rect)
		pantalla.blit(bstart.imagen, bstart.rect)
		pygame.display.flip()
	return 0

if __name__=='__main__':
	pygame.init()
	main()
