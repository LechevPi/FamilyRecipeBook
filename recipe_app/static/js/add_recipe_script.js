function addIngredientRow() {
    var table = document.getElementById("ingredients-table");
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    cell1.innerHTML = '<input type="text" name="ingredient_name[]" required class="long">';
    cell2.innerHTML = '<input type="number" name="ingredient_quantity[]" required min="0" class="long">';
    cell3.innerHTML = '<input type="text" name="ingredient_unit[]" required class="long">';
}

function deleteLastIngredient() {
    var table = document.getElementById("ingredients-table");
    var rowCount = table.rows.length;

    // Check if there are any rows to delete (excluding the header row)
    if (rowCount > 2) {
        table.deleteRow(rowCount - 1); // Delete the last row (excluding the header row)
    }
}

function addUtensilField() {
    var container = document.getElementById("utensils-container");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "utensils";
    container.appendChild(input);
    container.appendChild(document.createElement("br"));
}

function deleteLastUtensil() {
    var container = document.getElementById("utensils-container");
    var inputs = container.getElementsByTagName("input");
    var brs = container.getElementsByTagName("br");

    // Check if there are any utensils to delete
    if (inputs.length > 1 && brs.length > 0) {
        // Remove the last added utensil input
        container.removeChild(inputs[inputs.length - 1]);
        // Remove the last added <br> element
        container.removeChild(brs[brs.length - 1]);
    }
}


function addStepField() {
    var container = document.getElementById("steps-container");
    var stepsCount = container.querySelectorAll('.step').length + 1; // Get the current number of steps and increment it
    var div = document.createElement("div");
    div.className = "step";

    var span = document.createElement("span");
    span.className = "step-number";
    span.textContent = stepsCount + '.';

    var input = document.createElement("input");
    input.type = "text";
    input.name = "steps[]"; // Use array notation for multiple steps
    input.className = "long";

    div.appendChild(span);
    div.appendChild(input);
    container.appendChild(div);
}

function deleteLastStep() {
    var container = document.getElementById("steps-container");
    var steps = container.getElementsByClassName("step");
    var brs = container.getElementsByTagName("br");

    // Check if there are any steps to delete
    if (steps.length > 1) {
        // Remove the last added step
        container.removeChild(steps[steps.length - 1]);
        container.removeChild(brs[brs.length - 1]);
    }
}

function addTipField() {
    var container = document.getElementById("tips-container");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "tips";
    input.className = "long";
    container.appendChild(input);
    container.appendChild(document.createElement("br"));
}

function deleteLastTip() {
    var container = document.getElementById("tips-container");
    var inputs = container.getElementsByTagName("input");
    var brs = container.getElementsByTagName("br");

    // Check if there are any tips to delete
    if (inputs.length > 1 && brs.length > 0) {
        // Remove the last added tip input
        container.removeChild(inputs[inputs.length - 1]);
        // Remove the last added <br> element
        container.removeChild(brs[brs.length - 1]);
    }
}

// Function to update step numbers
function updateStepNumbers() {
    const stepNumbers = document.querySelectorAll('.step-number');

    stepNumbers.forEach((number, index) => {
        number.textContent = (index + 1) + '.';
    });
}

// Call the function after the page has loaded
window.onload = function() {
    updateStepNumbers();
};

let tagFieldCounter = 1;

function addTagField(tagString) {
    tagFieldCounter++;

    const tagsContainer = document.getElementById('tagsContainer');
    const tagsContainerId = `tags-container-${tagFieldCounter}`;
    const tagsInputId = `tagsInput-${tagFieldCounter}`;

    const newTagsContainer = document.createElement('div');
    newTagsContainer.id = tagsContainerId;
    newTagsContainer.classList.add('tagsContainer'); // Add class for easier targeting
    tagsContainer.appendChild(newTagsContainer);

    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'tags';
    newInput.className = 'tagsInput';
    newInput.setAttribute('data-index', tagFieldCounter);
    newInput.id = tagsInputId;

    // Put the provided tag string into the input field
    if (tagString) {
        newInput.value = tagString.trim();
    }

    newTagsContainer.appendChild(newInput);

    newTagsContainer.appendChild(document.createElement('br'));
}

function deleteLastTag() {
    var container = document.getElementById("tagsContainer");
    var tagsContainers = container.querySelectorAll(".tagsInput");

    // Check if there are any tags to delete
    if (tagsContainers.length > 1) {
        // Remove the last added tag input container
        container.removeChild(tagsContainers[tagsContainers.length - 1].parentElement);
    }
}

function updateTagField(buttonContent) {
    // Get all tag input elements
    const tagInputs = document.querySelectorAll('.tagsInput');
    let lastInputEmpty = false;

    // Check if the last input field is empty
    const lastInput = tagInputs[tagInputs.length - 1];
    if (lastInput.value.trim() === '') {
        lastInputEmpty = true;
    }

    // If the last input field is empty, load the button content into it
    if (lastInputEmpty) {
        lastInput.value = buttonContent.trim();
    } else {
        // Otherwise, check if the button content is already in any of the tag input fields
        let tagExists = false;
        tagInputs.forEach(function(input) {
            if (input.value.trim() === buttonContent.trim()) {
                tagExists = true;
            }
        });

        // If the button content is not in any tag input field, add a new tag field with the button content
        if (!tagExists) {
            addTagField(buttonContent);
        }
    }
}