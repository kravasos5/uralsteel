window.addEventListener("load", (event) => {
    // координаты кранов передаются в точках,
    // по оси X имеется 63 точки, значит 1 точка примерно 20.3 px
    // по оси Y - 16, значит 1 точка примерно 40 px
    var x_point = 20.3;
    var y_point = 40;
    // А также начальная точка на картинке немного смещена из-за чего
    // нужно определить отступы
    // стандартные отступы для размеров 1280x640 следующие:
    // x - 43, y - 162
    var x_indent = 43;
    var y_indent = 162;
    var canvas = document.getElementById('canvas');
    var canvas_context = canvas.getContext('2d');

    function draw_crane(crane, crane_info, cranes_info) {
        // Функция, рисующая краны
        // получаю координаты крана в точках
        let crane_body = cranes_info[`${crane}`];
        // Опредение текущего фото каретки
        if (!crane_info['is_upper']){
            if (crane_info['is_ladle']){
                var ladle = cranes_info['Ladle_d_w'];
            } else if (!crane_info['is_ladle']){
                var ladle = cranes_info['Ladle_d_wo'];
            }
        } else if (crane_info['is_upper']){
            if  (crane_info['is_ladle']){
                var ladle = cranes_info['Ladle_u_w'];
            } else if (!crane_info['is_ladle']){
                var ladle = cranes_info['Ladle_u_wo'];
            }
        }
        // Отрисовка корпуса
        // координаты корпуса
        // Формула следующиая:
        // x_coord = текущая_позиция_крана + отступ - половина_ширины_корпуса
        // При этом текущая позиция крана передаётся в точках, формула подразумевает,
        // что все значения переведены в px
        let crane_body_x0 = crane_info.x * x_point + x_indent - crane_body['size_x']/2;
        // y_indent это расстояние до верхней рельсы, на которой едет кран, если смотреть
        // по картинке, это как раз и будет верхняя точка корпуса крана
        let crane_body_y0 = y_indent;
        // создаю объект Image, чтобы нарисовать корпус
        let crane_body_photo = new Image();
        crane_body_photo.src = crane_body['photo'];
        // отрисовка корпуса
        canvas_context.drawImage(crane_body_photo, crane_body_x0, crane_body_y0);
        // Отрисовка каретки
        // Координаты каретки
        // Формула следующая:
        // x_coord = текущая_позиция_крана + отступ - половина_ширины_каретки
        // При этом текущая позиция крана передаётся в точках, формула подразумевает,
        // что все значения переведены в px
        let ladle_x0 = crane_info.x * x_point + x_indent - ladle['size_x']/2;
        // y_coord = отступ + текущая_позиция_каретки (уже переведённая в px)
        // 60 px это дополнительная мера, облегчающая эффект того, что
        // в схеме модулятора и схеме на сайте точки не совпадают
        // в будущем будет исправлено
        let ladle_y0 = y_indent + crane_info.y * y_point + 60;
        // создаю объект Image, чтобы нарисовать каретку
        let ladle_photo = new Image();
        ladle_photo.src = ladle['photo'];
        // отрисовка каретки
        canvas_context.drawImage(ladle_photo, ladle_x0, ladle_y0);
    };

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
                // очищаю холст
                clear_canvas();
                // отрисовываю краны на canvas
                for (let val in response.cranes_pos) {
                    draw_crane(val, response['cranes_pos'][val], response['cranes_info']);
                };
            },
            error: function(error) {
            },
        });
    };
    get_cranes();

    setInterval(get_cranes, 2000);
});