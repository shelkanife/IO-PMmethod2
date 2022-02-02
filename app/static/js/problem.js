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
    select.id='lge'
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
    
}