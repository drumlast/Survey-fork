function getRandomElement(array) {
    return array[Math.floor(Math.random() * array.length)];
}

function fillRegistrationForm() {
    document.getElementById("committeeSelect").selectedIndex = Math.floor(Math.random() * document.getElementById("committeeSelect").options.length);
    document.getElementById("subdivisionInput").value = "Подразделение №" + Math.floor(Math.random() * 100);
    document.getElementById("postInput").value = "Должность №" + Math.floor(Math.random() * 100);
    document.getElementById("privacyCheckbox").checked = true;
}

function fillSurveyForm() {
    // Автозаполнение текстовых полей
    document.querySelectorAll("textarea[id*='_response']").forEach(textarea => {
        textarea.value = "Тестовый ответ для " + textarea.id;
    });

    // Автозаполнение радиокнопок
    const radioGroups = {};
    document.querySelectorAll("input[type='radio']").forEach(radio => {
        const name = radio.getAttribute("name");
        if (!radioGroups[name]) {
            radioGroups[name] = [];
        }
        radioGroups[name].push(radio);
    });

    for (const name in radioGroups) {
        const radios = radioGroups[name];
        const randomRadio = getRandomElement(radios);
        randomRadio.checked = true;
        printRadioValue(randomRadio.value, randomRadio.id);
    }

    // Автозаполнение ползунков диапазона
    document.querySelectorAll("input[type='range']").forEach(range => {
        const step = parseFloat(range.step) || 0.25;  // Шаг по умолчанию 0.25
        const min = parseFloat(range.min);
        const max = parseFloat(range.max);
        const rangeSteps = Math.floor((max - min) / step);
        const randomStep = Math.floor(Math.random() * (rangeSteps + 1));
        const randomValue = (min + randomStep * step).toFixed(2);

        range.value = randomValue;
        displayRangeValue(randomValue, range.id + "_value");
    });

    // Добавление случайных комментариев
    document.querySelectorAll("button[id*='-add-button']").forEach(button => {
        const questionId = button.dataset.questionId;
        addComment(button.id);
        const textarea = document.getElementById(`${questionId}-textarea`);
        if (textarea) {
            textarea.value = "Тестовый комментарий для вопроса " + questionId;
        }
    });
}

function autoFillForms() {
    fillRegistrationForm();
    fillSurveyForm();
    alert("Формы заполнены автоматически. Нажмите 'Отправить ответы' для отправки данных.");
}

autoFillForms();
