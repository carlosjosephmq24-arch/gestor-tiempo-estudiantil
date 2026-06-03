tablero = ["1","2","3","4","5","6","7","8","9"]
jugador = "X"
turnos = 0

while turnos < 9:

    print()
    for i in range(0, 9, 3):
        print(tablero[i], "|", tablero[i+1], "|", tablero[i+2])

    pos = int(input(f"\nTurno de {jugador}. Elige una posición (1-9): ")) - 1

    if tablero[pos] not in ["X", "O"]:
        tablero[pos] = jugador
        turnos += 1

        if ((tablero[0] == tablero[1] == tablero[2]) or
            (tablero[3] == tablero[4] == tablero[5]) or
            (tablero[6] == tablero[7] == tablero[8]) or
            (tablero[0] == tablero[3] == tablero[6]) or
            (tablero[1] == tablero[4] == tablero[7]) or
            (tablero[2] == tablero[5] == tablero[8]) or
            (tablero[0] == tablero[4] == tablero[8]) or
            (tablero[2] == tablero[4] == tablero[6])):

            print("\n¡Ganó el jugador", jugador, "!")
            break

        if jugador == "X":
            jugador = "O"
        else:
            jugador = "X"

    else:
        print("Casilla ocupada")

if turnos == 9:
    print("\nEmpate")