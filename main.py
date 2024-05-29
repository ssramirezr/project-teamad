def calcular_first(no_terminal, gramatica, first, visitados):
    if no_terminal in visitados:
        return
    visitados.add(no_terminal)

    for produccion in gramatica[no_terminal]:
        for simbolo in produccion:
            if simbolo in gramatica:  # Es un no terminal
                calcular_first(simbolo, gramatica, first, visitados)
                first[no_terminal].update(first[simbolo] - {'e'})
                if 'e' not in first[simbolo]:
                    break
            else:  # Es un terminal
                first[no_terminal].add(simbolo)
                break
        else:
            first[no_terminal].add('e')

def cky_first(gramatica):
    first = {no_terminal: set() for no_terminal in gramatica}

    for no_terminal in gramatica:
        calcular_first(no_terminal, gramatica, first, set())

    return first

def calcular_follow(gramatica, first, start_symbol):
    follow = {no_terminal: set() for no_terminal in gramatica}
    follow[start_symbol].add('$')

    while True:
        updated = False
        for no_terminal, producciones in gramatica.items():
            for produccion in producciones:
                for i, simbolo in enumerate(produccion):
                    if simbolo in gramatica:  # Solo considerar no terminales
                        follow_temp = follow[simbolo].copy()
                        for j in range(i + 1, len(produccion)):
                            next_simbolo = produccion[j]
                            if next_simbolo in gramatica:
                                follow_temp.update(first[next_simbolo] - {'e'})
                                if 'e' in first[next_simbolo]:
                                    follow_temp.update(follow[produccion[j]])
                            else:
                                follow_temp.add(next_simbolo)
                                break
                            if 'e' not in first[next_simbolo]:
                                break
                        else:
                            follow_temp.update(follow[no_terminal])
                        if follow_temp - follow[simbolo]:
                            updated = True
                            follow[simbolo].update(follow_temp - follow[simbolo])

        if not updated:
            break

    return follow

def main():
    numCasos = int(input())
    resultados_first = []
    resultados_follow = []

    for _ in range(numCasos):
        m = int(input())
        gramatica = {}

        for _ in range(m):
            entrada = input().split()
            no_terminal = entrada[0]
            producciones = entrada[1:]
            producciones_expandidas = [list(prod) for prod in producciones]
            gramatica[no_terminal] = producciones_expandidas

        first = cky_first(gramatica)
        follow = calcular_follow(gramatica, first, 'S')

        resultados_first.append(first)
        resultados_follow.append(follow)

    for first, follow in zip(resultados_first, resultados_follow):
        for no_terminal in sorted(first.keys()):
            print(f"First({no_terminal}) = {{{', '.join(sorted(first[no_terminal]))}}}")
        for no_terminal in sorted(follow.keys()):
            print(f"Follow({no_terminal}) = {{{', '.join(sorted(follow[no_terminal]))}}}")

if __name__ == '__main__':
    main()
