window.addEventListener("load", (event) => {
    $('#timeform').submit(function(event) {
        // Обработка отправки формы
        event.preventDefault();
        // формирование data запроса
        form_data = {};
        form_data['csrfmiddlewaretoken'] = $(this).find('input[name*="csrfmiddlewaretoken"]').val();
        form_data['time'] = $(this).find('input#timeinput').val();

        $.ajax({
            type: 'POST',
            url: '',
            data: form_data,
            data_type: 'json',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
            },
        });
    });
});