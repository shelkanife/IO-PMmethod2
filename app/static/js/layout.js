const tables=document.getElementById('tables')
let hasSolution

function areFilled(variable,constrains){
    return variable && constrains
}
function correctValue(variable,constrains){
    return variable>=2 && constrains>0
}

function generateLayout(e){
    e.preventDefault()

    const VARIABLES=e.target.variables.value 
    const CONSTRAINS=e.target.constrains.value 

    if(!areFilled(VARIABLES,CONSTRAINS)){
        alert('No se puede generar la matriz')
        return
    }
    if(!correctValue(VARIABLES,CONSTRAINS)){
        alert('No se puede generar la matriz')
        return 
    }
    const layout=document.getElementById('layout')
    
    if(layout.hasChildNodes()) layout.replaceChildren()
    createProblem(layout,VARIABLES,CONSTRAINS)
    hasSolution=true
}

document.forms[0].addEventListener('submit',e=>generateLayout(e))