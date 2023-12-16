window.addEventListener("load", (event) => {
    var ladles_old;
    var lines = [];
    // модификаторы размеров на сколько размер canvas больше начального,
    // то есть 1280x640
    var x_modificator;
    var y_modificator;

    function draw_ladlde(ladle, ladle_info) {
        // Функция, рисующая ковши
        // отрисовка коша
        ladle_image = new Image();
        ladle_image.src = ladle_info['photo'];
        canvas_context.drawImage(ladle_image, ladle_info['x'], ladle_info['y']);
        // если ковш "транспортируемый", подробнее о типах ковшей в
        // представлении страницы ковшей LadlesView в методе get_ladles_info
        if (ladle_info['is_transporting']) {
            // получаю расстояние от начала страницы до canvas
            canvas_rect = canvas.getBoundingClientRect();
            let x_slide = canvas_rect.x;
            let y_slide = canvas_rect.y;
            // если экран устройства маленький, то размер стрелок должен быть меньше
            // это можно определить по x_modificator
            let size;
            if (x_modificator < 0.5) {
                size = 3;
            } else {
                size = 6;
            };
            // считаю начальные координаты линии
            // x_slide и y_slide идут как константы, их не домножаем на модификаторы
            // а вот остальные координаты стоит перевести, так как
            // линии рисуются не внутри canvas, а относительно всей страницы
            // 26 и 29 это половина ширины и высоты картинки ковша соответственно
            let x1 = x_slide + (ladle_info['x'] + 26)*x_modificator;
            let y1 = y_slide + (ladle_info['y'] + 29)*y_modificator;
            // считаю конечные координаты стрелки
            let x2 = x_slide + ladle_info['next_x']*x_modificator;
            let y2 = y_slide + ladle_info['next_y']*y_modificator;
            // создаю объект линии
            line = new LeaderLine(
                LeaderLine.pointAnchor({ x: x1, y: y1 }),
                LeaderLine.pointAnchor({ x: x2, y: y2 }),
                {
                    color: '#FF4B00',
                    size: size,
                    dash: {animation: true}
                });
            // рисую линию
            line.draw;
            // добавляю новую линию в список линий, чтобы их можно было очистить
            lines.push(line);
        };
        // теперь нужно записать отрисованные ковши в объект ladles_old
        ladles_old[ladle] = ladle_info;
    };

    function get_modificator() {
        x_modificator = canvas.offsetWidth/canvas.width;
		y_modificator = canvas.offsetHeight/canvas.height;
    };

    function clear_lines() {
        // очищает все стрелки на странице
        for (let line=0; line < lines.length; line++) {
            lines[line].remove()
        };
        lines = [];
    };

    $('#timeform').submit(function(event) {
        // Обработка отправки формы
        event.preventDefault();
        // формирование data запроса
        form_data = {};
        form_data['csrfmiddlewaretoken'] = $(this).find('input[name*="csrfmiddlewaretoken"]').val();
        form_data['time'] = $(this).find('input#timeinput').val();

        if (!form_data['time']) {
            // ничего не делать
        } else {
            $.ajax({
                type: 'POST',
                url: '',
                data: form_data,
                data_type: 'json',
                success: function(response) {
                    console.log(response);
                    ladles_old = response;
                    // Очищаю canvas
                    clear_canvas();
                    // удаляю стрелки
                    clear_lines();
                    setTimeout(() => {
                        // получаю модификатор
                        get_modificator();
                        ladles_old = {};
                        for (let ladle in response) {
                            draw_ladlde(ladle, response[ladle]);
                        };
                    }, 100);
                },
                error: function(error) {
                },
            });
        };
    });

    function lmc_handler(event) {
        // Функция, обрабатывающая клик ЛКМ на canvas
        // получаю координаты клика пользователя
        const clientX = event.clientX;
        const clientY = event.clientY;
        // получаю расстояние от начала страницы до canvas
        canvas_rect = canvas.getBoundingClientRect();
        let x_slide = canvas_rect.x;
        let y_slide = canvas_rect.y;
        // проверяю был ли клик по ковшу
        console.log(ladles_old);
        for (let ladle in ladles_old) {
        	let diff_x = clientX - ladles_old[ladle].x*x_modificator - x_slide;
        	let diff_y = clientY - ladles_old[ladle].y*y_modificator - y_slide;
        	if ((diff_x <= 41 && diff_x >= 0) && (diff_y <= 46 && diff_y >= 0)) {
        		console.log('Ковш №' + ladle);
        		info_output(ladle, ladles_old[ladle]);
        		break;
        	};
        };
    };

    function rmc_handler(event) {
        // Функция обработчик нажатия ПКМ по canvas

    };

    function info_output(ladle, ladle_info) {
        // Функция, выводящая информацию о ковше
        // Меняю информацию в модальном окне на информацию о текущем ковше
        document.getElementById('ladle-num').textContent = ladle;
        document.getElementById('num-melt').textContent = ladle_info['num_melt'];
        document.getElementById('brand').textContent = ladle_info['brand_steel'];
        document.getElementById('aggregate').textContent = ladle_info['aggregate'];
        document.getElementById('next-aggregate').textContent = ladle_info['next_aggregate'];
        document.getElementById('operation-start').textContent = ladle_info['plan_start'];
        document.getElementById('operation-end').textContent = ladle_info['plan_end'];
        // Открываю модальное окно
        let btn = document.getElementById('modal-button');
        btn.click();
    };

    canvas.addEventListener('click', lmc_handler);

    canvas.addEventListener('contextmenu', function(event) {
        event.preventDefault();
    });
});