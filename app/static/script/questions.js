document.addEventListener('DOMContentLoaded', function() {
    const editModal = document.getElementById('editModal');
    const editForm = document.getElementById('editForm');

    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    document.querySelector('.edit-settings').addEventListener('click', function(e) {
        e.preventDefault();
        const surveyId = this.dataset.id;

        // Получение текущих настроек из data-атрибутов или через глобальные переменные
        const slug = '{{ survey.slug }}';
        const settings = {{ survey.survey_settings|tojson }};

        let formContent = `
            <div class="mb-3">
                <label for="surveySlug" class="form-label">Идентификатор URL (slug):</label>
                <input type="text" class="form-control" id="surveySlug" name="slug" value="${slug}">
            </div>
        `;

        settings.forEach(setting => {
            formContent += `
                <div class="mb-3">
                    <label for="setting_${setting.id}" class="form-label">${setting.name}:</label>
                    <input type="text" class="form-control" id="setting_${setting.id}" name="${setting.key}" value="${setting.value}">
                </div>
            `;
        });

        editForm.innerHTML = formContent;
        editModal.setAttribute('data-id', surveyId);
        editModal.setAttribute('data-type', 'survey-settings');

        const modal = new bootstrap.Modal(editModal);
        modal.show();
    });

    // Обработчик для редактирования вступления
    document.querySelector('.edit-introduction').addEventListener('click', function(e) {
        e.preventDefault();
        const surveyId = this.dataset.id;
        const introduction = `{{ survey.introduction|escape(js) }}`;

        editForm.innerHTML = `
            <div class="mb-3">
                <label for="surveyIntroduction" class="form-label">Вступление:</label>
                <textarea class="form-control" id="surveyIntroduction" name="introduction" rows="5">${introduction}</textarea>
            </div>
        `;
        editModal.setAttribute('data-id', surveyId);
        editModal.setAttribute('data-type', 'survey-introduction');

        const modal = new bootstrap.Modal(editModal);
        modal.show();
    });

    // Обработчик для редактирования инструкций
    document.querySelectorAll('.edit-instruction').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const instructionId = this.dataset.id;
            const instructionTitle = this.closest('.card').querySelector('.card-header').innerText.trim();
            const instructionBody = this.closest('.card').querySelector('.card-body').innerText.trim();

            editForm.innerHTML = `
                <div class="mb-3">
                    <label for="instructionTitle" class="form-label">Заголовок инструкции:</label>
                    <input type="text" class="form-control" id="instructionTitle" name="title" value="${instructionTitle}">
                </div>
                <div class="mb-3">
                    <label for="instructionBody" class="form-label">Текст инструкции:</label>
                    <textarea class="form-control" id="instructionBody" name="body_html" rows="5">${instructionBody}</textarea>
                </div>
            `;
            editModal.setAttribute('data-id', instructionId);
            editModal.setAttribute('data-type', 'instruction');

            const modal = new bootstrap.Modal(editModal);
            modal.show();
        });
    });

    // Обработчик для сохранения изменений
    document.getElementById('saveChanges').addEventListener('click', function() {
        const id = editModal.getAttribute('data-id');
        const type = editModal.getAttribute('data-type');
        let data = {};

        if (type === 'survey-settings') {
            data.slug = document.getElementById('surveySlug').value;
            data.settings = {};
            document.querySelectorAll('#editForm input[name]').forEach(input => {
                if (input.name !== 'slug') {
                    data.settings[input.name] = input.value;
                }
            });
        } else if (type === 'survey-introduction') {
            data.introduction = document.getElementById('surveyIntroduction').value;
        } else if (type === 'instruction') {
            data.title = document.getElementById('instructionTitle').value;
            data.body_html = document.getElementById('instructionBody').value;
        } else {
            // Обработка других типов
        }

        // Отправка запроса на сервер
        let url = '';
        if (type === 'survey-settings') {
            url = `/api/surveys/${id}/settings/`;
        } else if (type === 'survey-introduction') {
            url = `/api/surveys/${id}/introduction/`;
        } else if (type === 'instruction') {
            url = `/api/instructions/${id}/`;
        } else {
            url = `/api/${type}/${id}/`;
        }

        fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                const modal = bootstrap.Modal.getInstance(editModal);
                modal.hide();
                // Обновляем страницу или соответствующие элементы
                location.reload();
            } else {
                alert('Ошибка при сохранении данных');
            }
        })
        .catch(error => console.error('Ошибка:', error));
    });

    document.querySelectorAll('.editable-cell').forEach(cell => {
        cell.addEventListener('click', function() {
            const type = this.dataset.type;
            const id = this.dataset.id;
            const title = this.dataset.title;

            editForm.innerHTML = '';

            if (type === 'direction') {
                editForm.innerHTML = `
                    <div class="mb-3"><p>ID направления: ${id}</p></div>
                    <div class="mb-3">
                        <label for="directionTitle" class="form-label">Название направления:</label>
                        <div class="input-group">
                            <input type="text" class="form-control" id="directionTitle" name="title" value="${title}">
                            <span class="input-group-text copy-text" id="copy-text" onclick="copy_text('${title}')">
                                <i class="bi bi-clipboard"></i>
                            </span>
                        </div>
                    </div>
                `;
            } else if (type === 'criterion') {
                editForm.innerHTML = `
                    <div class="mb-3"><p>ID критерия: ${id}</p></div>
                    <div class="mb-3"><p>ID родительского направления: ${this.dataset.directionId}</p></div>
                    <div class="mb-3">
                        <label for="criterionTitle" class="form-label">Название критерия:</label>
                        <div class="input-group">
                            <input type="text" class="form-control" id="criterionTitle" name="title" value="${title}">
                            <span class="input-group-text copy-text" id="copy-text" onclick="copy_text('${title}')">
                                <i class="bi bi-clipboard"></i>
                            </span>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="criterionNumber" class="form-label">Номер критерия:</label>
                        <div class="input-group">
                            <input type="text" class="form-control" id="criterionNumber" name="title" value="${this.dataset.number}">
                            <span class="input-group-text copy-text" id="copy-text" onclick="copy_text('${this.dataset.number}')">
                                <i class="bi bi-clipboard"></i>
                            </span>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="criterionWeight" class="form-label">Вес:</label>
                        <div class="input-group">
                            <input type="number" class="form-control" id="criterionWeight" name="weight" value="${this.dataset.weight}">
                            <span class="input-group-text copy-text" id="copy-text" onclick="copy_text('${this.dataset.weight}')">
                                <i class="bi bi-clipboard"></i>
                            </span>
                        </div>
                    </div>
                     <div class="mb-3">
                        <label for="criterionPrompt" class="form-label">Пояснение:</label>
                        <div class="input-group">
                            <textarea type="text" class="form-control" id="criterionPrompt" name="prompt">${this.dataset.prompt || ''}</textarea>
                            <span class="input-group-text copy-text" id="copy-text" onclick="copy_text('${this.dataset.prompt || ''}')">
                                <i class="bi bi-clipboard"></i>
                            </span>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="question" class="form-label">Развёрнутый вопрос (только если интервью):</label>
                        <div class="input-group">
                            <textarea type="text" class="form-control" id="question" name="question">${this.dataset.question || ''}</textarea>
                            <span class="input-group-text copy-text" id="copy-text" onclick="copy_text('${this.dataset.prompt || ''}')">
                                <i class="bi bi-clipboard"></i>
                            </span>
                        </div>
                    </div>
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="detailedResponse" name="extendedAnswer" ${this.dataset.detailedResponse === 'true' ? 'checked' : ''}>
                        <label class="form-check-label" for="detailedResponse">Развёрнутый ответ</label>
                    </div>
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="extendedAnswer" name="isInterview" ${this.dataset.isInterview === 'true' ? 'checked' : ''}>
                        <label class="form-check-label" for="isInterview">Интервью (требуется развёрнутый ответ без выбора ответа)</label>
                    </div>
                `;
            } else if (type === 'subcriterion') {
                editForm.innerHTML = `
                    <div class="mb-3"><p>ID подкритерия: ${id}</p></div>
                    <div class="mb-3">
                        <label for="subcriterionTitle" class="form-label">Название подкритерия</label>
                        <div class="input-group">
                            <input type="text" class="form-control" id="subcriterionTitle" name="title" value="${title}">
                            <span class="input-group-text copy-text" id="copy-text" onclick="copy_text('${title}')">
                                <i class="bi bi-clipboard"></i>
                            </span>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="criterionWeight" class="form-label">Вес</label>
                        <div class="input-group">
                            <input type="number" class="form-control" id="criterionWeight" name="weight" value="${this.dataset.weight}">
                            <span class="input-group-text copy-text" id="copy-text" onclick="copy_text('${this.dataset.weight}')">
                                <i class="bi bi-clipboard"></i>
                            </span>
                        </div>
                    </div>
                     <div class="mb-3">
                        <label for="punctPrompt" class="form-label">Пояснение</label>
                        <div class="input-group">
                            <textarea type="text" class="form-control" id="punctTooltip" name="tooltip">${this.dataset.prompt || ''}</textarea>
                            <span class="input-group-text copy-text" id="copy-text" onclick="copy_text('${this.dataset.prompt || ''}')">
                                <i class="bi bi-clipboard"></i>
                            </span>
                        </div>
                    </div>
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="detailedResponse" name="extendedAnswer" ${this.dataset.detailedResponse === 'true' ? 'checked' : ''}>
                        <label class="form-check-label" for="detailedResponse">Развёрнутый ответ</label>
                    </div>
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="extendedAnswer" name="isInterview" ${this.dataset.isInterview === 'true' ? 'checked' : ''}>
                        <label class="form-check-label" for="isInterview">Интервью (требуется развёрнутый ответ без выбора ответа)</label>
                    </div>
                `;
            } else if (type === 'punct') {
                editForm.innerHTML = `
                    <div class="mb-3"><p>ID пункта: ${id}</p></div>
                    <div class="mb-3">
                        <label for="punctTitle" class="form-label">Пункт</label>
                        <div class="input-group">
                            <textarea type="text" class="form-control" id="punctTitle" name="title">${title}</textarea>
                            <span class="input-group-text copy-text" id="copy-text" onclick="copy_text('${title}')">
                                <i class="bi bi-clipboard"></i>
                            </span>
                        </div>
                    </div>
                    <div class="row">
                        <span>Диапазон</span>
                        <div class="col">
                            <label for="rangeMin" class="form-label">от</label>
                            <input class="form-control" id="rangeMin" name="weight" value="${this.dataset.rangeMin}">
                        </div>
                        <div class="col">
                            <label for="rangeMax" class="form-label">до</label>
                            <input class="form-control" id="rangeMax" name="weight" value="${this.dataset.rangeMax}">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="punctPrompt" class="form-label">Пояснение</label>
                        <div class="input-group">
                            <textarea type="text" class="form-control" id="punctTooltip" name="tooltip">${this.dataset.prompt || ''}</textarea>
                            <span class="input-group-text copy-text" id="copy-text" onclick="copy_text('${this.dataset.prompt || ''}')">
                                <i class="bi bi-clipboard"></i>
                            </span>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="punctComment" class="form-label">Комментарий</label>
                        <div class="input-group">
                            <textarea type="text" class="form-control" id="punctComment" name="comment">${this.dataset.comment || ''}</textarea>
                            <span class="input-group-text copy-text" id="copy-text" onclick="copy_text('${this.dataset.comment || ''}')">
                                <i class="bi bi-clipboard"></i>
                            </span>
                        </div>
                    </div>
                `;
            }

            editModal.setAttribute('data-id', id);
            editModal.setAttribute('data-type', type);

            const modal = new bootstrap.Modal(editModal);
            modal.show();
        });
    });

    document.getElementById('saveChanges').addEventListener('click', function() {
        const id = editModal.getAttribute('data-id');
        const type = editModal.getAttribute('data-type');
        let data = {};

        if (type === 'direction') {
            data = { title: document.getElementById('directionTitle').value };
        } else if (type === 'criterion') {
            data = {
                title: document.getElementById('criterionTitle').value,
                weight: document.getElementById('criterionWeight').value
            };
        } else if (type === 'subcriterion') {
            data = { title: document.getElementById('subcriterionTitle').value };
        } else if (type === 'punct') {
            data = {
                title: document.getElementById('punctTitle').value,
                extendedAnswer: document.getElementById('extendedAnswer').checked,
                tooltip: document.getElementById('punctTooltip').value
            };
        }

        // Отправляем запрос на сервер для сохранения изменений
        fetch(`/api/${type}s/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    const modal = bootstrap.Modal.getInstance(editModal);
                    modal.hide();
                    // Обновляем данные на странице
                    document.querySelector(`.editable-cell[data-id="${id}"]`).dataset.title = data.title;
                } else {
                    alert('Ошибка при сохранении данных');
                }
            })
            .catch(error => console.error('Ошибка:', error));
    });

    document.getElementById('deleteItem').addEventListener('click', function() {
        const id = editModal.getAttribute('data-id');
        const type = editModal.getAttribute('data-type');

        fetch(`admin/api/${type}/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrf_token
            }
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                const modal = bootstrap.Modal.getInstance(editModal);
                modal.hide();
                // Удаляем строку таблицы
                location.reload();
            } else {
                alert('Ошибка при удалении');
            }
        })
        .catch(error => console.error('Ошибка:', error));
    });
});
