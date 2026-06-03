import juego
import random

# Inicializar pygame
juego.init()

# Tamaño ventana
ANCHO = 800
ALTO = 600
pantalla = juego.display.set_mode((ANCHO, ALTO))
juego.display.set_caption("Juego de Disparos")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Reloj
clock = juego.time.Clock()
FPS = 60

# Jugador
jugador = juego.Rect(370, 500, 60, 60)
velocidad_jugador = 6

# Balas
balas = []
velocidad_bala = 8

# Enemigos
enemigos = []
velocidad_enemigo = 3

# Fuente
fuente = juego.font.SysFont(None, 40)

# Puntos
puntos = 0

# Crear enemigos
for i in range(5):
    enemigo = juego.Rect(random.randint(0, 740), random.randint(-300, -50), 60, 60)
    enemigos.append(enemigo)

# Bucle principal
running = True
while running:
    clock.tick(FPS)
    pantalla.fill(NEGRO)

    # Eventos
    for event in juego.event.get():
        if event.type == juego.QUIT:
            running = False

        # Disparar
        if event.type == juego.KEYDOWN:
            if event.key == juego.K_SPACE:
                bala = juego.Rect(jugador.centerx - 5, jugador.y, 10, 20)
                balas.append(bala)

    # Movimiento jugador
    teclas = juego.key.get_pressed()

    if teclas[juego.K_LEFT] and jugador.x > 0:
        jugador.x -= velocidad_jugador

    if teclas[juego.K_RIGHT] and jugador.x < ANCHO - jugador.width:
        jugador.x += velocidad_jugador

    # Movimiento balas
    for bala in balas[:]:
        bala.y -= velocidad_bala

        if bala.y < 0:
            balas.remove(bala)

    # Movimiento enemigos
    for enemigo in enemigos:
        enemigo.y += velocidad_enemigo

        if enemigo.y > ALTO:
            enemigo.x = random.randint(0, 740)
            enemigo.y = random.randint(-300, -50)

    # Colisiones
    for bala in balas[:]:
        for enemigo in enemigos:
            if bala.colliderect(enemigo):
                if bala in balas:
                    balas.remove(bala)

                enemigo.x = random.randint(0, 740)
                enemigo.y = random.randint(-300, -50)

                puntos += 1
                break

    # Dibujar jugador
    juego.draw.rect(pantalla, VERDE, jugador)

    # Dibujar balas
    for bala in balas:
        juego.draw.rect(pantalla, BLANCO, bala)

    # Dibujar enemigos
    for enemigo in enemigos:
        juego.draw.rect(pantalla, ROJO, enemigo)

    # Mostrar puntos
    texto = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

    # Actualizar pantalla
    juego.display.flip()

juego.quit()
