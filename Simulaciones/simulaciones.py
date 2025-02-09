# Función eCerradura: implementa la operación de e-cerradura
# Recibe un diccionario (representación de un NFA), un nodo final, y un nodo
# Retorna los estados alcanzables desde el nodo dado, incluyendo transiciones ε


def eCerradura(dictionary, states, initial):
    if not isinstance(states, list):
        states = [states]  # Convertir un estado único en lista
    
    stack = states.copy()
    eClosure = set(stack)  # Usamos un set para evitar duplicados
    
    while stack:
        state = stack.pop()
        if state in dictionary:  # Verificar si el estado existe en el diccionario
            transitions = dictionary[state]
            if 'ε' in transitions:
                # Manejar tanto valores únicos como listas para transiciones epsilon
                epsilon_transitions = transitions['ε']
                if isinstance(epsilon_transitions, list):
                    next_states = epsilon_transitions
                else:
                    next_states = [epsilon_transitions]
                
                for next_state in next_states:
                    if next_state not in eClosure:
                        stack.append(next_state)
                        eClosure.add(next_state)
    
    return list(eClosure)

# Función move: implementa la operación de mover
# Recibe un diccionario (representación de un NFA), un nodo final, un conjunto de estados,
# y una etiqueta de transición
# Retorna los estados alcanzables desde el conjunto de estados dado, utilizando la etiqueta dada
def move(dictionary,finalNode,states,label):
    #print("move con los estados ",states," y la etiqueta ", label)
    result=[]
      # Se itera sobre cada estado en el conjunto de estados dado
    for i in states:
        if not i == finalNode:
            # Se obtiene el diccionario de transiciones para el estado i
            subDict = dictionary[i]
            key = list(subDict.keys())[0]
            # Si la clave coincide con la etiqueta de transición, se agrega el valor a result
            if key == label:
                values = list(subDict.values())[0]
                if type(values) == list:
                    for k in values:
                        result.append(k)
                else:
                    result.append(values)
    # Se aplica e-cerradura a cada estado en result, y se agrega el resultado a un conjunto temporal
    temp = []
    #print("e-cerradura con los estados: ",result)
    for i in result:
        temp.append(eCerradura(dictionary,finalNode,i))
    for i in temp:
        if type(i) == list:
             # Si el resultado es una lista de estados, se itera sobre cada estado y se agrega a result
            for j in i:
                result.append(j)
        elif i == None:
            # Si el resultado es None, no se realiza ninguna acción
            pass
        else:
            # Si el resultado es un solo estado, se agrega a result
            result.append(i)
     # Retorna el conjunto de estados alcanzables desde el conjunto de estados dado, utilizando la etiqueta dada
    #print("Los estados resultantes fueron: ", result)
    return list(set(result))

# Función simulationNFA: implementa la simulación de un NFA
# Recibe un diccionario (representación de un NFA), un estado inicial, un estado final,

def simulationNFA(initial, final, string, dictionary, alphabet):
    print("\n---------- SIMULACIÓN NFA ----------")
    print("Cadena a evaluar:", string)
    
    # Verificar que la cadena solo contenga símbolos del alfabeto
    for char in string:
        if char not in alphabet:
            print(f"Error: El carácter '{char}' no está en el alfabeto {alphabet}")
            return False
    
    current_states = eCerradura(dictionary, initial, initial)
    print("Estados iniciales (después de ε-cerradura):", current_states)
    
    # Procesar cada símbolo de la cadena
    for char in string:
        next_states = set()
        for state in current_states:
            if state in dictionary and char in dictionary[state]:
                value = dictionary[state][char]
                # Manejar tanto valores únicos como listas
                if isinstance(value, list):
                    next_states.update(value)
                else:
                    next_states.add(value)
        
        # Aplicar ε-cerradura a todos los estados alcanzados
        temp_states = set()
        for state in next_states:
            temp_states.update(eCerradura(dictionary, state, initial))
        current_states = list(temp_states)
        
        if not current_states:
            print(f"La cadena es rechazada (no hay transiciones válidas para '{char}')")
            return False
        
        print(f"Estados después de procesar '{char}':", current_states)
    
    # Verificar si algún estado final es alcanzable
    if final in current_states:
        print("La cadena es aceptada")
        return True
    else:
        print("La cadena es rechazada (no termina en estado final)")
        return False

