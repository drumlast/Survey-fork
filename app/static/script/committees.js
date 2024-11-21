$(document).ready(function() {
    var csrf_token = $('meta[name=csrf-token]').attr('content');

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        }
    });

    function initializeSelect2() {
        $('#parent_id').select2({
            placeholder: 'Выберите родительский комитет',
            allowClear: true
        });
    }

    initializeSelect2();

    function loadCommittees() {
        $.getJSON("/admin/api/committees", function(data) {
            var committeesHtml = '<table class="table table-bordered">';
            committeesHtml += '<thead><tr><th>Название</th><th>Информация</th><th>Действия</th></thead>';
            committeesHtml += '<tbody>';
            data.forEach(function(committee) {
                if (!committee.parent_id) {
                    committeesHtml += generateCommitteeHtml(committee);
                }
            });
            committeesHtml += '</tbody></table>';
            $('#committees-list').html(committeesHtml);
        });
    }

    function generateCommitteeHtml(committee) {
        return `
            <tr>
                <td>${committee.name}</td>
                <td>${committee.info ? committee.info : ''}</td>
                <td>
                    <button class="btn btn-link" onclick="loadSubCommittees(${committee.id})">Подкомитеты</button>
                    <button class="btn btn-link" onclick="editCommittee(${committee.id})">Редактировать</button>
                    <button class="btn btn-link" onclick="deleteCommittee(${committee.id})">Удалить</button>
                    <button class="btn btn-link" onclick="addSubcommittee(${committee.id})">Добавить подкомитет</button>
                </td>
            </tr>
            <tr id="subcommittees-${committee.id}" style="display: none;">
                <td colspan="3">
                    <table class="table table-bordered">
                        <thead><tr><th>Название</th><th>Информация</th><th>Действия</th></thead>
                        <tbody></tbody>
                    </table>
                </td>
            </tr>
        `;
    }

    window.loadSubCommittees = function(parentId) {
        var subcommitteeRow = $(`#subcommittees-${parentId}`);
        if (subcommitteeRow.is(':visible')) {
            subcommitteeRow.hide();
            return;
        }

        $.getJSON(`/admin/api/committees/${parentId}`, function(data) {
            var subcommitteesHtml = '';
            data.forEach(function(subcommittee) {
                subcommitteesHtml += generateCommitteeHtml(subcommittee);
            });
            subcommitteeRow.find('tbody').html(subcommitteesHtml);
            subcommitteeRow.show();
        });
    }

    window.editCommittee = function(committeeId) {
        // Fetch committee data and populate the modal form
        $.getJSON(`/admin/api/committees/${committeeId}`, function(data) {
            $('#edit-name').val(data.name);
            $('#edit-info').val(data.info);
            $('#edit-parent-id').html('');
            $('#edit-parent-id').append('<option value="0">Нет родительского комитета</option>');
            data.forEach(function(committee) {
                if (committee.id !== committeeId) {
                    $('#edit-parent-id').append(`<option value="${committee.id}">${committee.name}</option>`);
                }
            });
            $('#edit-parent-id').val(data.parent_id).trigger('change');
            $('#editCommitteeModal').modal('show');
        });

        $('#edit-committee-form').off('submit').on('submit', function(event) {
            event.preventDefault();
            $.ajax({
                type: 'PUT',
                url: `/admin/api/committees/${committeeId}`,
                data: $(this).serialize(),
                success: function(response) {
                    loadCommittees();
                    $('#editCommitteeModal').modal('hide');
                    showMessage('Комитет успешно обновлен!', 'success');
                },
                error: function(xhr) {
                    var response = JSON.parse(xhr.responseText);
                    showMessage('Ошибка при обновлении комитета: ' + response.error, 'danger');
                }
            });
        });
    }

    window.deleteCommittee = function(committeeId) {
        $('#deleteCommitteeModal').modal('show');
        $('#confirm-delete').off('click').on('click', function() {
            $.ajax({
                type: 'DELETE',
                url: `/admin/api/committees/${committeeId}`,
                success: function(response) {
                    loadCommittees();
                    $('#deleteCommitteeModal').modal('hide');
                    showMessage('Комитет успешно удален!', 'success');
                },
                error: function() {
                    showMessage('Ошибка при удалении комитета.', 'danger');
                }
            });
        });
    }

    window.addSubcommittee = function(parentId) {
        $('#parent-committee-id').val(parentId);
        $('#addSubcommitteeModal').modal('show');
    }

    $('#add-subcommittee-form').on('submit', function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/admin/committees',
            data: $(this).serialize(),
            success: function(response) {
                loadCommittees();
                $('#addSubcommitteeModal').modal('hide');
                showMessage('Подкомитет добавлен!', 'success');
            },
            error: function() {
                showMessage('Ошибка при добавлении подкомитета.', 'danger');
            }
        });
    });

    function showMessage(message, type) {
        $('#message').html(`<div class="alert alert-${type}">${message}</div>`);
    }

    loadCommittees();

    $('#committee-form').on('submit', function(event) {
        event.preventDefault();
        var form = $(this);
        $.ajax({
            type: 'POST',
            url: '/admin/committees/add',
            data: form.serialize(),
            success: function(response) {
                loadCommittees();
                form[0].reset();
                $('#parent_id').val(null).trigger('change');
                initializeSelect2(); // Reinitialize Select2 after resetting form
                showMessage(response.message, 'success');
            },
            error: function(xhr) {
                var response = JSON.parse(xhr.responseText);
                showMessage(response.error, 'danger');
            }
        });
    });
});
