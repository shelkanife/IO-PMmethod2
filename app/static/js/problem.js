const TABLES=document.getElementById('tables')

function generateSelectMinMax(){
    let select=document.createElement('select')
    select.id='minMax'
    let optionMax=document.createElement('option')
    optionMax.value='max'
    optionMax.textContent='MAX'
    let optionMin=document.createElement('option')
    optionMin.value='min'
    optionMin.textContent='MIN'
    select.appendChild(optionMax)
    select.appendChild(optionMin)
    return select
}

function generateSelectOperators(){
    let select=document.createElement('select')
    select.className='lge'
    let optionLe=document.createElement('option')
    optionLe.value='le'
    optionLe.textContent='<='
    let optionGe=document.createElement('option')
    optionGe.value='ge'
    optionGe.textContent='>='
    let optionEq=document.createElement('option')
    optionEq.value='eq'
    optionEq.textContent='='
    select.appendChild(optionLe)
    select.appendChild(optionGe)
    select.appendChild(optionEq)
    return select
}

function generateObjectiveFunction(variables){
    const p=document.createElement('p')
    p.appendChild(generateSelectMinMax())
    for(let i=0;i<variables;i++){
        const xLabel=document.createElement('label')
        if(i+1<variables) xLabel.textContent=`X${i+1} + `
        else xLabel.textContent=`X${i+1}`
        const xInput=document.createElement('input')
        xInput.className='variable'
        p.appendChild(xInput)
        p.appendChild(xLabel)
    }
    return p
}

function generteTable(problem,heading,nconstrains,varHolgura){
    // console.log('generateTable ', varHolgura)
    let p=document.createElement('p')
    p.innerHTML=`${varHolgura[0]}`
    let table = document.createElement('table')
    let trHeading = document.createElement('tr')
    table.appendChild(trHeading)
    let thVariablesTemplate ='<th></th>'
    for(let i of heading[0]){
        thVariablesTemplate += `<th>${i}</th>`
    }

    thVariablesTemplate += '<th>Z</th>'
    trHeading.innerHTML = thVariablesTemplate
    let trObjective = document.createElement('tr')
    let trObjectiveTemplate = '<td></td>'
    for(let i of problem[0])
        trObjectiveTemplate += `<td>${i}</td>`
    trObjective.innerHTML = trObjectiveTemplate
    table.appendChild(trObjective)
    let templateConstrains=''
    for(i=0;i<nconstrains;i++){
        let trConstrains = document.createElement('tr')
        table.appendChild(trConstrains)
        templateConstrains = `<td>${varHolgura[1][i]}</td>`
        for(let item of problem[1][i])
            templateConstrains += `<td>${item}</td>`
        trConstrains.innerHTML = templateConstrains
    }
    p.append(table)
    return p
}

function makeBaseMatriz(variables,constrains){
    let aVariables = [],aConstrains = []
    aVariables.push(Array.from(variables).map(variable => parseInt(variable.value)))
    let aAux=Array.from(constrains).map(constrain => parseInt(constrain.value))
    
    const SLICE = variables.length+1 
    for (let i = 0; i < aAux.length; i += SLICE) 
        aConstrains.push(aAux.slice(i, i + SLICE))

    return aVariables.concat(aConstrains)
}

const getOperators= (collection) => Array.from(collection).map(element => element.value)

function createProblem(layout,variables,constrains){
    layout.appendChild(generateObjectiveFunction(variables))
    for(i=0;i<constrains;i++){
        const p=document.createElement('p')
        for(let j=0;j<variables;j++){
            const xLabel=document.createElement('label')
            const xInput=document.createElement('input')
            xInput.className='constrain'
            if(j<variables-1){
                xLabel.textContent=`X${j+1} + `
                p.appendChild(xInput)
                p.appendChild(xLabel)
            }else{
                 p.appendChild(xInput)
                 xLabel.textContent=`X${j+1}`
                 p.appendChild(xLabel)
                 p.appendChild(generateSelectOperators())
            }
        }
        const xInput=document.createElement('input')
        xInput.className='constrain'
        p.appendChild(xInput)
        layout.appendChild(p)
    }
    const button=document.createElement('button')
    button.textContent='Solve'
    layout.appendChild(button)
    button.addEventListener('click',e=>send(e))
}

function send(e){
    const VARIABLE = document.getElementsByClassName('variable')
    const CONSTRAIN = document.getElementsByClassName('constrain')
    let problemType=document.querySelector('#minMax').value
    let variables=parseInt(document.querySelector('#variables').value)
    let constrains=parseInt(document.querySelector('#constrains').value)
    let problem=makeBaseMatriz(VARIABLE,CONSTRAIN)
    
    let data=[]
    data.push(problemType)
    data.push(variables)
    data.push(constrains)
    data.push(getOperators(document.getElementsByClassName('lge')))
    let body=JSON.stringify({
        "dataProblem":JSON.stringify(data),
        "toSendProblem":JSON.stringify(problem)
    })
    fetch('https://mmethodflask.herokuapp.com/m-method',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body
    })
    .then(async res =>{
        let response=await res.json()

        TABLES.innerHTML=''
        let tb=document.createElement('h1')
        tb.textContent='Tablón Base'
        TABLES.appendChild(tb)
        TABLES.appendChild(generteTable(response[0][0],response[2],constrains,response[3][0]))
        for(let i=1;i<response[0].length;i++){
            let tbi=document.createElement('h1')
            tbi.textContent=`Tablón ${i}`
            TABLES.appendChild(tbi)
            TABLES.appendChild(generteTable(response[0][i],response[2],constrains,response[3][i]))
        }
        alert(`Z= ${response[1]}`)
    })





}