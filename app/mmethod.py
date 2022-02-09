from fractions import Fraction
from app.base_table import *

has_solution=True
def find_min(row:list)->list:
    # Retorna una lista: [indice,valor]
    value=min(row)
    index=row.index(value)
    return [index,value]

def get_right_side(problem:list)->list:
    # Retorna una lista unicament con el lado derecho de las restricciones
    return [row[-1] for row in problem[1:]]   

def get_pivot_comlumn(index:int,problem:list,nconstrains:int)->list:
    #Retorna una lista con los valores de la columna seleccionada como pivote
    return [row[index] for row in problem[1:nconstrains+1]]

def find_minnimun(indexes:list,divisiones:list,pivotes:list)->list or None:
    global has_solution
    allIsNull = False
    if len(divisiones) == 0 and len(pivotes) == 0:
        allIsNull = True
    
    if not allIsNull:
        min = divisiones[0]
        index = indexes[0]
        pivote = pivotes[0]
        for i in range(len(divisiones)):
            if min == None:
                pass
            else:
                if divisiones[i] != None:
                    if divisiones[i] < min:
                        min = divisiones[i]
                        index = indexes[i]
                        pivote = pivotes[i]
        # // [index de la matriz problem / pivote -> numero ]
        return [index+1,pivote]
    else:
        has_solution = False
        return

def find_pivot(rightSide:list,pivotColumn:list)->function:
    # Encuentra los arrglos de lado derecho/ columna pivote
    index = []
    divisiones = []
    pivotes = []
    for i in range(len(rightSide)):
        if(pivotColumn[i] != 0 and pivotColumn[i] > 0):
            divisiones.append(Fraction(rightSide[i],pivotColumn[i]))
            index.append(i)
            pivotes.append(pivotColumn[i])
        
    return find_minnimun(index,divisiones,pivotes)

def get_row_pivoted(row:list,coeficient:int)->list:
    # Retorna una lista con los valores de la fila pivoteada
    return list(map(lambda component: Fraction(component,coeficient),row))

def get_new_FO(oldFO:list,newRowPivoted:list,taregetIndex:int)->list:
    # Retorna una lista despues de la operacion:
    TIMES=oldFO[taregetIndex]*-1
    return [x+(TIMES*newRowPivoted[i]) for i,x in enumerate(oldFO)]

def get_new_row(oldFO:list,newRowPivoted:list,taregetIndex:int)->list:
    # Retorna una lista despues de la operacion:
    #  NRX = RX + NRY
    TIMES=oldFO[taregetIndex]*-1
    newRowPivoted=list(map(lambda x: x.limit_denominator(1000),newRowPivoted))
    return [x+(TIMES*newRowPivoted[i]) for i,x in enumerate(oldFO)]


def simp(problem,nVariables,inecuations):
    global has_solution
    has_solution=True
    response=[]
    rfo=[]
    rfo_=[]
    rs=[]
    for item in problem[0]:
        rfo_.append(item.__str__())
    rfo.append(rfo_)
    for row in problem[1:]:
        x=[]
        for item in row:
            x.append(item)
        rs.append(x)
    rfo.append(rs)
    response.append(rfo)
    heading=get_heading(nVariables,inecuations)
    basicVariables=get_basic_variables(inecuations)
    chVariables=[['',basicVariables.copy()]]
    min = find_min(problem[0][:len(problem[0])-1])
    while(min[1]<0):
        
        rightSide = get_right_side(problem)
        pivotColumn = get_pivot_comlumn(min[0],problem,len(problem)-1)
        pivot = find_pivot(rightSide,pivotColumn)
        if pivot != None:
            ch='Sale <strong>{}</strong> entra <strong>{}</strong></em>'.format(basicVariables[pivot[0]-1],heading[min[0]])
            basicVariables[pivot[0]-1]=heading[min[0]]
            chVariables.append([ch,basicVariables.copy()])
            
        if has_solution :
            problem[pivot[0]] = get_row_pivoted(problem[pivot[0]],pivot[1])
            problem[0] = get_new_FO(problem[0],problem[pivot[0]],min[0])
            
            for i in range(1,len(problem)):
                if i != pivot[0]:
                    problem[i]=get_new_row(problem[i],problem[pivot[0]],min[0])
            rfo=[]
            rfo_=[]
            rs=[]
            for item in problem[0]:
                rfo_.append(item.__str__())
            rfo.append(rfo_)
            for row in problem[1:]:
                x=[]
                for item in row:
                    if isinstance(item,Fraction):
                        x.append(item.__str__())
                rs.append(x)

            rfo.append(rs)
            response.append(rfo)
            min = find_min(problem[0][:len(problem[0])-1])
            
        else:
            break
    
    if has_solution:
        if not verify_problem(chVariables):
            return [response,problem[0][-1].__str__(),[heading],chVariables]
        else: 
            if is_greater_than_zero(response[-1][1:][-1][1:]):
                return [response,'Solucion no acotada',[heading],chVariables]
            else:
                return [response,problem[0][-1].__str__(),[heading],chVariables]
        
    else:
        return [response,'Solucion no acotada',[heading],chVariables]
        
def verify_problem(chVariables):
    basicVariables=chVariables[-1][-1]
    for variable in basicVariables:
        if 'A' in variable: return True
    return False
def is_greater_than_zero(rows):
    for row in rows:
        if Fraction(row[-1])>0: return True
    return False

def start(problem,dataProblem):
    stepOne = add_variables_HE(problem,dataProblem)
    stepTwo = add_artificial_variables(stepOne,dataProblem)
    baseTable = make_base_table(stepTwo,dataProblem)
    return simp(baseTable,dataProblem[1],dataProblem[3])