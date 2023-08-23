import pygame
import random
import pkgutil
from pygame import mixer

# Initialize pygame
pygame.init()

# Constants
ANCHO = 500
ALTO = 500
VEL_PERSONAJE = 5
VEL_ELEMENTO = 5
FPS = 60

# Constants for timers and speed increase
TIEMPO_INCREMENTO = 2000
AUMENTO_VELOCIDAD = 1
TIEMPO_PUNTOS = 10000

# Paths
ruta_start = "recursos/start.ogg"
ruta_nota = "recursos/sorma.png"
ruta_fondo = 'recursos/fondo2.png'
ruta_bloque = "recursos/lol2.png"
ruta_siete = "recursos/lagos.jpg."
ruta_win_sound = "recursos/violo.ogg"
sonido_ganar = pygame.mixer.Sound(ruta_win_sound)

imagen_termino = pygame.image.load('recursos/ending.png')
imagen_termino = pygame.transform.scale(imagen_termino, (ANCHO, ALTO))
rect_termino = imagen_termino.get_rect(center=(ANCHO // 2, ALTO // 2))
boton_salir = pygame.Rect(ANCHO // 2 - 75, ALTO // 2 + 100, 150, 50)
color_boton = (255, 0, 0)

# Initialize pygame mixer
pygame.mixer.init()
mixer.music.load('recursos/songfondo.mp3')
mixer.music.play(-1, 0.0)

# Variables
score = 0
nivel = 1
font = pygame.font.SysFont(None, 36)
mensaje_mostrando = False
angulo_rotacion = 0
opacidad = 255
sonido_inicio = pygame.mixer.Sound(ruta_start)

# Variables para el menú
menu_font = pygame.font.SysFont(None, 48)
opciones = ['Comenzar juego', 'Salir']
opcion_seleccionada = 0

# Fondo
fondo = pygame.image.load(ruta_fondo)
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Configurar pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Esquiva los Bloques")

# Clases
class Personaje(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(ruta_nota)
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO // 2
        self.rect.y = ALTO - 60

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= VEL_PERSONAJE
        if keys[pygame.K_RIGHT] and self.rect.x < ANCHO - self.rect.width:
            self.rect.x += VEL_PERSONAJE
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= VEL_PERSONAJE
        if keys[pygame.K_DOWN] and self.rect.y < ALTO - self.rect.height:
            self.rect.y += VEL_PERSONAJE

class Bloque(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        if self.tipo == "daño":
            self.image = pygame.image.load(ruta_bloque)
        elif self.tipo == "puntos":
            self.image = pygame.image.load(ruta_siete)  # Cambiar a la imagen del bloque de puntos
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = 0 - self.rect.height
        self.velocidad = random.randint(1, VEL_ELEMENTO + nivel)

    def update(self):
        self.rect.y += self.velocidad

        if self.rect.y > ALTO:
            self.rect.y = 0 - self.rect.height
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.velocidad = random.randint(1, VEL_ELEMENTO + 2)

    def agarrar(self):
        if self.tipo == "daño":
            # Lógica para cuando el bloque hace daño
            pass
        elif self.tipo == "puntos":
            # Lógica para cuando el bloque da puntos
            global score
            score += 1
            self.rect.y = 0 - self.rect.height
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.velocidad = random.randint(1, VEL_ELEMENTO + 2)


# Grupos de sprites
todos_los_sprites = pygame.sprite.Group()
bloques = pygame.sprite.Group()

personaje = Personaje()
todos_los_sprites.add(personaje)

cantidad_bloques = random.randint(1, 3)

for i in range(cantidad_bloques):
    tipo_bloque = random.choice(["daño", "puntos"])
    bloque = Bloque(tipo_bloque)  # Pass the tipo parameter here
    todos_los_sprites.add(bloque)
    bloques.add(bloque)
    
# Velocidad de los bloques
def actualizar_velocidad_bloques():
    for bloque in bloques:
        bloque.velocidad += 1
        
# Función para agregar un bloque
def agregar_bloque():
    bloque = Bloque()
    todos_los_sprites.add(bloque)
    bloques.add(bloque)
    
# Función para mostrar un mensaje    
def crear_mensaje(mensaje):
    global mensaje_mostrando, angulo_rotacion, opacidad, imagen_mensaje, rect_mensaje

    font_mensaje = pygame.font.SysFont(None, 50)
    imagen_mensaje = font_mensaje.render(mensaje, True, (255, 0, 0))
    rect_mensaje = imagen_mensaje.get_rect(center=(ANCHO // 2, ALTO // 2))
    
    mensaje_mostrando = True
    angulo_rotacion = 0
    opacidad = 255


# Función para mostrar el menú
def mostrar_menu():
    for index, opcion in enumerate(opciones):
        if index == opcion_seleccionada:
            color = (255, 0, 0)  # Rojo para la opción seleccionada
        else:
            color = (0, 0, 0)  # Negro para las demás
        text = menu_font.render(opcion, True, color)
        pantalla.blit(text, (ANCHO // 2 - text.get_width() // 2, 150 + index * 60))


# Inicializamos las variables
timer = pygame.time.get_ticks()
tiempo_anterior = pygame.time.get_ticks()

timer_puntos = pygame.time.get_ticks()
tiempo_anterior_puntos = pygame.time.get_ticks()

# Menú principal
en_menu = True
clock_menu = pygame.time.Clock()
while en_menu:
    
    pantalla.blit(fondo, (0, 0))
    
    titulo = menu_font.render("SORMA GAME", True, (255, 255, 255))
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))
    mostrar_menu()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            en_menu = False
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_DOWN:
                # Selecciona la siguiente opción
                opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
            elif evento.key == pygame.K_UP:
                # Selecciona la opción anterior
                opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
            elif evento.key == pygame.K_RETURN:
                if opcion_seleccionada == 0:  # Comenzar juego
                    sonido_inicio = pygame.mixer.Sound(ruta_start)
                    sonido_inicio.play()
                    en_menu = False
                elif opcion_seleccionada == 1:  # Salir
                    en_menu = False
                    corriendo = False

    pygame.display.flip()
    pygame.time.Clock().tick(60)


mostrando_imagen_final = False
mostrando_imagen_dano = False
tiempo_finalizacion = 0  # Variable para el tiempo de finalización de las imágenes

corriendo = True
# Bucle principal del juego
while corriendo:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    tiempo_actual = pygame.time.get_ticks()
    
    # Calculate time elapsed for daño blocks
    tiempo_transcurrido = tiempo_actual - tiempo_anterior
    
    if tiempo_transcurrido >= TIEMPO_INCREMENTO:
        # Update the timer for daño blocks
        tiempo_anterior = tiempo_actual

        # Increase the frequency and speed of daño blocks
        cantidad_bloques += 1
        actualizar_velocidad_bloques()

    # Calculate time elapsed for puntos blocks
    tiempo_transcurrido_puntos = tiempo_actual - tiempo_anterior_puntos
    
    if tiempo_transcurrido_puntos >= TIEMPO_PUNTOS:
        # Update the timer for puntos blocks
        tiempo_anterior_puntos = tiempo_actual

        # Add a "puntos" block
        tipo_bloque = "puntos"
        bloque = Bloque(tipo_bloque)
        todos_los_sprites.add(bloque)
        bloques.add(bloque)

    # Actualizar
    todos_los_sprites.update()

    # Chequear colisiones
    colisiones = pygame.sprite.spritecollide(personaje, bloques, True)
    for colision in colisiones:
        if colision.tipo == "daño":
            # Logic for when a "daño" block is hit
            corriendo = False  # End the game
            mostrando_imagen_dano = True
            tiempo_finalizacion = tiempo_actual + 10000  # Display image for 10 seconds
        elif colision.tipo == "puntos":
            colision.agarrar()
            if score >= 5 and not mostrando_imagen_final:  # Check if player reached 5 points
                mostrando_imagen_final = True
                tiempo_finalizacion = tiempo_actual + 10000  # Display image for 10 seconds
        
        if mostrando_imagen_final and tiempo_actual >= tiempo_finalizacion:
            corriendo = False  # End the game
        elif mostrando_imagen_dano and tiempo_actual >= tiempo_finalizacion:
            corriendo = False  # End the game
        
    if len(bloques) < cantidad_bloques:  # Agregar más bloques si es necesario
        tipo_bloque = random.choice(["daño", "puntos"])
        bloque = Bloque(tipo_bloque)
        todos_los_sprites.add(bloque)
        bloques.add(bloque)

    # Dibujar
    pantalla.blit(fondo, (0, 0))
    todos_los_sprites.draw(pantalla)
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    pantalla.blit(text, (10, 10))
    
    if mensaje_mostrando:
        pantalla.blit(imagen_mensaje, rect_mensaje.topleft)

        superficie_desvanecimiento = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        superficie_desvanecimiento.fill((255, 255, 255, 255-opacidad))
        pantalla.blit(superficie_desvanecimiento, (0, 0))

        opacidad -= 5  # Disminuye la opacidad

        # Si la opacidad llega a cero, finalizamos la animación
    if score >= 5 and mostrando_imagen_final:
            pantalla.blit(imagen_termino, rect_termino.topleft)
            sonido_ganar.play()

    if mostrando_imagen_dano and tiempo_actual < tiempo_finalizacion:
        imagen_dano = pygame.image.load('recursos/erto.png')
        imagen_dano = pygame.transform.scale(imagen_dano, (ANCHO, ALTO))
        pantalla.blit(imagen_dano, (0, 0))
    elif mostrando_imagen_dano:
        mostrando_imagen_dano = False  # Deja de mostrar la imagen de daño
            
    pygame.display.flip()
    clock_menu.tick(FPS)

pygame.quit()