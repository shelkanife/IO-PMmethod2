const toggleBtn = document.getElementById("toggle-btn");
let lightMode = true;
toggleBtn.addEventListener("click", function (e) {
  e.preventDefault();
  const icon = this.children[0];
  if (lightMode) {
    icon.classList.remove("fa-moon");
    icon.classList.add("fa-sun");
  } else {
    icon.classList.remove("fa-sun");
    icon.classList.add("fa-moon");
  }
  document.body.classList.toggle("dark");
  lightMode = !lightMode;
});

const tables = document.getElementById("tables");
let hasSolution;

function isValidValue(value) {
  return !/^[A-Za-z\s]*$/.test(value);
}
function isInsideRange(value, min, max) {
  return value >= min && value <= max;
}
function areFilled(variable, constrains) {
  return variable && constrains;
}
function correctValue(variable, constrains) {
  return variable >= 2 && constrains > 0;
}

function generateLayout(e) {
  e.preventDefault();

  let VARIABLES = e.target.variables.value,
    CONSTRAINS = e.target.constrains.value;

  if (isValidValue(VARIABLES) && isValidValue(CONSTRAINS)) {
    try {
      VARIABLES = Number.parseInt(VARIABLES);
      CONSTRAINS = Number.parseInt(CONSTRAINS);
      if (isInsideRange(VARIABLES, 2, 20) && isInsideRange(CONSTRAINS, 1, 50)) {
        const layout = document.getElementById("layout");
        if (layout.hasChildNodes()) layout.replaceChildren();
        createProblem(layout, VARIABLES, CONSTRAINS);
        hasSolution = true;
      } else {
        alert("Wrong values: Values out of range");
      }
    } catch {
      alert("Wrong values: Can not generate matrix");
    }
  } else {
    alert("Wrong values: Can not generate matrix");
  }
}

document.forms[0].addEventListener("submit", (e) => generateLayout(e));
