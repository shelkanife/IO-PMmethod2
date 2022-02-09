from .mnumber import MNumber

def count_variables_HE(lst:list, artificial:bool)->int:
    if artificial:
        return len(lst)-lst.count('le')
    return len(lst)-lst.count('eq')

def get_index_artificial_variables(lst:list)->list:
    return [i+1 for i,x in enumerate(lst) if x == 'ge' or x == 'eq']

def add_variables_HE(problem,dataProblem): # Agrego variables de holgura o exceso
    numberVariblesHE=count_variables_HE(dataProblem[3],False)
    problem[0].extend([0 for _ in range(numberVariblesHE+1)]) #agrego 0 al renglon objetivo
    lastItem = len(problem[1])-1
    index = 0
    for i in range(dataProblem[2]):
        if dataProblem[3][i] == "eq":
            for j in range(numberVariblesHE):
                problem[i+1].insert(lastItem+j,0)
        
        if dataProblem[3][i] == "ge":
            for j in range(numberVariblesHE):
                problem[i+1].insert(lastItem+j,0 if index != j else -1) 
            index+=1

        if dataProblem[3][i] == "le":
            for j in range(numberVariblesHE):
                problem[i+1].insert(lastItem+j,0 if index != j else 1)
            index+=1
    return problem

def add_artificial_variables(problem:list,dataProblem):
    numberVariblesHE=count_variables_HE(dataProblem[3],True)
    nonBasicVaribles=len(problem[0])-1
    if dataProblem[0] == 'max':
        problem[0]=list(map(lambda x: MNumber(x*-1,0),problem[0]))
    else:
        problem[0]=list(map(lambda x: MNumber(x,0),problem[0]))
        
    for i in range(numberVariblesHE):
        problem[0].insert(nonBasicVaribles+i,MNumber(0,1))
    problem[0][len(problem[0])-1]=MNumber(0,0)
    lastItem=len(problem[1])-1
    index=0
    for i in range(dataProblem[2]):
        if dataProblem[3][i] == "eq":
            for j in range(numberVariblesHE):
                problem[i+1].insert(lastItem+j,0 if index != j else 1)
            index+=1

        if dataProblem[3][i] == "ge":
            for j in range(numberVariblesHE):
                problem[i+1].insert(lastItem+j,0 if index != j else 1)
            index+=1
        
        if dataProblem[3][i] == "le":
            for j in range(numberVariblesHE):
                problem[i+1].insert(lastItem+j,0)

    return problem

def make_base_table(problem,dataProblem):
    indexes=get_index_artificial_variables(dataProblem[3])
    suma=0
    for i in range(len(problem[1])-1): #recorro el indice del n-ecimo arreglo
        for j in range(len(indexes)):
            suma+=problem[indexes[j]][i]
        aux = MNumber(0,suma*-1)
        problem[0][i]=problem[0][i]+aux
        suma=0
    suma=0
    lastItem=len(problem[1])-1
    for j in range(len(indexes)):
        suma+=problem[indexes[j]][lastItem]
        aux = MNumber(0,suma*-1)
    problem[0][lastItem] = problem[0][lastItem]+aux

    return problem

def get_heading(nvariables,dataProblem):
    s,e,a=1,1,1
    heading=[f'X{i+1}' for i in range(nvariables)]
    for i in dataProblem:
        if i=="le":
            heading.append('S{}'.format(s))
            s+=1
    for i in dataProblem:
        if i=="ge":
            heading.append('E{}'.format(e))
            e+=1
    for i in dataProblem:
        if i=="ge" or i=="eq":
            heading.append('A{}'.format(a))
            a+=1
    return heading

def get_basic_variables(dataProblem):
    basicVariables=[]
    le,geeq=1,1
    for inecuation in dataProblem:
        if inecuation == "le":
            basicVariables.append('S{}'.format(le))
            le+=1
        else:
            basicVariables.append('A{}'.format(geeq))
            geeq+=1
    return basicVariables