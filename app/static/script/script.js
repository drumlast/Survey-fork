function copy_text(text) {
    console.log(text)
    navigator.clipboard.writeText(text);
}

function printRangeValue(value, id) {
    const questionId = document.getElementById(id).dataset.questionId;
    const radioOptions = document.getElementsByName(questionId + "-radio");
    let selectedRadioValue = 0;

    for (const option of radioOptions) {
        if (option.checked) {
            selectedRadioValue = parseFloat(option.value);
            break;
        }
    }
    const finalValue = selectedRadioValue + parseFloat(value);
    document.getElementById(questionId + "-range-label").textContent = "Ваша градация: " + finalValue.toFixed(2);
    document.getElementById(id).value = value;
}

function printRadioValue(value, id) {
    const questionId = document.getElementById(id).dataset.questionId;
    const rangeElement = document.getElementsByName(questionId + "-range")[0];
    const rangeValue = parseFloat(rangeElement.value) || 0;

    const finalValue = parseFloat(value) + rangeValue;
    document.getElementById(questionId + "-range-label").textContent = "Ваша градация: " + finalValue.toFixed(2);
}

function displayRangeValue(value, displayId) {
    const displayElement = document.getElementById(displayId);
    if (displayElement) {
        displayElement.innerText = value;
    }
}

function addComment(id) {
    const questionId = document.getElementById(id).dataset.questionId;
    const container = document.getElementById(`${questionId}-comment-container`);
    const addButton = document.getElementById(`${questionId}-add-button`);
    const deleteButton = document.getElementById(`${questionId}-delete-button`);

    if (container && addButton && deleteButton) {
        addButton.style.display = 'none';
        deleteButton.style.display = 'block';
        container.innerHTML = `<textarea class="form-control" id="${questionId}-textarea" name="${questionId}-comment" rows="4" required></textarea>`;
    } else {
        console.error("Unable to find comment elements for question:", questionId);
    }
}

function deleteComment(id) {
    const questionId = document.getElementById(id).dataset.questionId;
    const container = document.getElementById(`${questionId}-comment-container`);
    const addButton = document.getElementById(`${questionId}-add-button`);
    const deleteButton = document.getElementById(`${questionId}-delete-button`);

    if (container && addButton && deleteButton) {
        addButton.style.display = 'block';
        deleteButton.style.display = 'none';
        container.innerHTML = "";
    } else {
        console.error("Unable to find comment elements for question:", questionId);
    }
}
