window.addEventListener("load", (event) => {
    function get_cranes() {
        // Функция, запрашивающая положение кранов
        form_data = {};
        form_data['csrfmiddlewaretoken'] = csrf_token;
        // Запрос на сервер и дальнейшее отображение кранов
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
    };
    get_cranes();

    setInterval(get_cranes, 5000);
});