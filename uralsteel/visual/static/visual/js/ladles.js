window.addEventListener("load", (event) => {

    function draw_ladlde(ladle, ladle_info) {
        // Функция, рисующая ковши
        console.log(ladle);
        console.log(ladle_info);
    };

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
                // Очищаю canvas
                clear_canvas();
                for (let ladle in response) {
                    draw_ladlde(ladle, response[ladle]);
                };
            },
            error: function(error) {
            },
        });
    });
});