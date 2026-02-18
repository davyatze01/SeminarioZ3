

# DAVIDE ATZENI 60/73/65376


from z3 import *

def CountingStrategy(nums, obiettivo):
    solver = Solver()
    
    risultati = [Int(f'val_{i}') for i in range(6)]
    p = [Int(f'indice_{i}') for i in range(6)]
    operazioni = [Int(f'op_{i}') for i in range(5)] 

    for i in range(6):
        solver.add(And(p[i] >= 0, p[i] < 6))

        for j in range(i + 1, 6):
            solver.add(p[i] != p[j]) 
            
    solver.add(Or([And(p[0] == j, risultati[0] == nums[j]) for j in range(6)]))
    

    for i in range(5):
        solver.add(And(operazioni[i] >= 0, operazioni[i] <= 4))
        numero_corrente = Int(f'curr_num_{i}')
        solver.add(Or([And(p[i+1] == j, numero_corrente == nums[j]) for j in range(6)]))
        
        no_operation = And(operazioni[i] == 0, risultati[i+1] == risultati[i])
        addizione = And(operazioni[i] == 1, risultati[i+1] == risultati[i] + numero_corrente)
        sottrazione = And(operazioni[i] == 2, risultati[i+1] == risultati[i] - numero_corrente)
        moltiplicazione = And(operazioni[i] == 3, risultati[i+1] == risultati[i] * numero_corrente)
        divisione = And(
            operazioni[i] == 4,
            numero_corrente != 0,
            risultati[i] % numero_corrente == 0,
            risultati[i+1] == risultati[i] / numero_corrente
        )

        solver.add(Or(no_operation, addizione, sottrazione, moltiplicazione, divisione))
        
        if i > 0:
            solver.add(Or(operazioni[i-1] != 0, operazioni[i] == 0)) 
            

    distanza = Int('dist')
    solver.add(Or(
        And(risultati[5] >= obiettivo, distanza == risultati[5] - obiettivo),
        And(risultati[5] < obiettivo, distanza == obiettivo - risultati[5])
    ))
    

    conteggio_operazioni = [Int(f'step_var_{i}') for i in range(5)]
    for i in range(5):
        solver.add(Or(
            And(operazioni[i] != 0, conteggio_operazioni[i] == 1),
            And(operazioni[i] == 0, conteggio_operazioni[i] == 0)
        ))

    totale_operazioni = Int('steps')
    solver.add(totale_operazioni == sum(conteggio_operazioni))
    

    modello_migliore = None
    distanza_migliore = float('inf')
    

    while solver.check() == sat:
        modello = solver.model()
        distanza_attuale = modello.evaluate(distanza).as_long()
        operazioni_attuali = modello.evaluate(totale_operazioni).as_long()
        
        modello_migliore = modello
        distanza_migliore = distanza_attuale
        

        solver.add(Or(
            distanza < distanza_attuale,
            And(distanza == distanza_attuale, totale_operazioni < operazioni_attuali)
        ))
        
    if modello_migliore is None:
        print("No valid operations found.")
        return
        

    m = modello_migliore
    print(f"  Initial number: {m.evaluate(risultati[0]).as_long()}")
    
    op_map = {1: '+', 2: '-', 3: '*', 4: '/'}
    
    for i in range(5):
        o = m.evaluate(operazioni[i]).as_long()
        if o == 0: 
            break 
            
        v_curr = m.evaluate(Int(f'curr_num_{i}')).as_long()
        v_next = m.evaluate(risultati[i+1]).as_long()
        print(f"Step {i+1}: operation {op_map[o]} with number {v_curr} -> result {v_next}")
        
    print(f" Final number: {m.evaluate(risultati[5]).as_long()}")
    print(f"  Distance from obiettivo: {distanza_migliore}")


CountingStrategy([2, 4, 8, 16, 32, 64], 1234567)