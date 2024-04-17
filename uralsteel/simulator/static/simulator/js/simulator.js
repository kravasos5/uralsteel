window.addEventListener("load", function(){
    // получаем ссылки, связанные с холст
    const canvas = document.querySelector('.canvas');
    const ctx = canvas.getContext("2d");
    const BB = canvas.getBoundingClientRect();
    const offsetX = BB.left;
    const offsetY = BB.top;
    const WIDTH = canvas.width;
    const HEIGHT = canvas.height;
    // получаем кнопки
    const down_button_1 = document.querySelector('.down__button__1');
    const down_button_2 = document.querySelector('.down__button__2');
    const down_button_3 = document.querySelector('.down__button__3');
    const down_button_4 = document.querySelector('.down__button__4');
    const take_ladle_1 = document.querySelector('.take__ladle__1');
    const take_ladle_2 = document.querySelector('.take__ladle__2');
    const take_ladle_3 = document.querySelector('.take__ladle__3');
    const take_ladle_4 = document.querySelector('.take__ladle__4');
    // получаем текстовые элементы
    const span_1 = document.querySelector('.span__1');
    const span_2 = document.querySelector('.span__2');
    const span_3 = document.querySelector('.span__3');
    const span_4 = document.querySelector('.span__4');
    const span_5 = document.querySelector('.span__5');
    const span_6 = document.querySelector('.span__6');
    const span_7 = document.querySelector('.span__7');
    const span_8 = document.querySelector('.span__8');
    // переменные, связанные с перетаскиванием
    let dragok = false;
    let startX;
    let startY;
    // массив объектов, определяющих разные формы
    const cases = [];
    const carriages = [];
    const shadows = [];
    // определяем 4 прямоугольника
    cases.push({
        x: 150,
        y: 2,
        width: 20,
        height: 149,
        fill: "#000000",
        isDragging: false
    });
    cases.push({
        x: 450,
        y: 2,
        width: 20,
        height: 149,
        fill: "#000000",
        isDragging: false
    });
    cases.push({
        x: 500,
        y: 2,
        width: 20,
        height: 149,
        fill: "#000000",
        isDragging: false
    });
    cases.push({
        x: 900,
        y: 2,
        width: 20,
        height: 149,
        fill: "#000000",
        isDragging: false
    });
    // определяем 4 круга
    carriages.push({
        x: 160,
        y: 100,
        r: 10,
        fill:"#c0c0c0",
        isDragging: false,
        is_upper: true,
        with_ladle: false
    });
    carriages.push({
        x: 460,
        y: 100,
        r: 10,
        fill: "#c0c0c0",
        isDragging: false,
        is_upper: true,
        with_ladle: false
    });
    carriages.push({
        x: 510,
        y: 100,
        r: 10,
        fill: "#c0c0c0",
        isDragging: false,
        is_upper: true,
        with_ladle: false
    });
    carriages.push({
        x: 910,
        y: 100,
        r: 10,
        fill: "#c0c0c0",
        isDragging: false,
        is_upper: true,
        with_ladle: false
    });
    // Определяем 4 тени
    shadows.push({
        x: 160,
        y: 100,
        r: 4,
        fill:"#FF0000"
    });
    shadows.push({
        x: 460,
        y: 100,
        r: 4,
        fill: "#FF0000"
    });
    shadows.push({
        x: 510,
        y: 100,
        r: 4,
        fill: "#FF0000"
    });
    shadows.push({
        x: 910,
        y: 100,
        r: 4,
        fill: "#FF0000"
    });
    // переменные для прямоугольников
    const case1 = cases[0];
    const case2 = cases[1];
    const case3 = cases[2];
    const case4 = cases[3];
    // переменные для кругов
    const carriage1 = carriages[0];
    const carriage2 = carriages[1];
    const carriage3 = carriages[2];
    const carriage4 = carriages[3];
    // переменные для теней
    const shadow1 = shadows[0];
    const shadow2 = shadows[1];
    const shadow3 = shadows[2];
    const shadow4 = shadows[3];
    // слушаем события мыши
    canvas.onmousedown = myDown;
    canvas.onmouseup = myUp;
    canvas.onmousemove = myMove;
    // вызов рисования сцены
    draw();
    // рисуем один прямоугольник
    function rect(r) {
        ctx.fillStyle = r.fill;
        ctx.fillRect(r.x, r.y, r.width, r.height);
    }
    // рисуем один круг
    function circle(c) {
        ctx.fillStyle = c.fill;
        ctx.beginPath();
        ctx.arc(c.x, c.y, c.r, 0, Math.PI * 2);
        ctx.closePath();
        ctx.fill();
    }
    // очищаем холст
    function clear() {
        ctx.clearRect(0, 0, WIDTH, HEIGHT);
    }
    // перерисовываем сцену
    function draw() {
        clear();
        for (let i = 0; i < cases.length; i++) {
            rect(cases[i]);
        }
        for (let k = 0; k < carriages.length; k++) {
            circle(carriages[k]);
        }
        for (let j = 0; j < shadows.length; j++) {
            circle(shadows[j]);
        }
    }
    // обрабатываем события mousedown
    function myDown(e) {
        // сообщаем браузеру, что мы обрабатываем это событие мыши
        e.preventDefault();
        e.stopPropagation();
        // получаем текущую позицию мыши
        const mx = parseInt(e.clientX - offsetX);
        const my = parseInt(e.clientY - offsetY);
        // проверяем каждую фигуру, чтобы увидеть, находится ли внутри мышь
        dragok = false;
        const d1x = carriage1.x - mx;
        const d1y = carriage1.y - my;
        if (!dragok &&
            d1x * d1x + d1y * d1y < carriage1.r * carriage1.r &&
            mx > case1.x &&
            mx < case1.x + case1.width &&
            my > case1.y &&
            my < case1.y + case1.height) {
                dragok = true;
                carriage1.isDragging = true;
                case1.isDragging = true;
            }
        const d2x = carriage2.x - mx;
        const d2y = carriage2.y - my;
        if (!dragok &&
            d2x * d2x + d2y * d2y < carriage2.r * carriage2.r &&
            mx > case2.x &&
            mx < case2.x + case2.width &&
            my > case2.y &&
            my < case2.y + case2.height) {
                dragok = true;
                carriage2.isDragging = true;
                case2.isDragging = true;
            }
        const d3x = carriage3.x - mx;
        const d3y = carriage3.y - my;
        if (!dragok &&
            d3x * d3x + d3y * d3y < carriage3.r * carriage3.r &&
            mx > case3.x &&
            mx < case3.x + case3.width &&
            my > case3.y &&
            my < case3.y + case3.height) {
                dragok = true;
                carriage3.isDragging = true;
                case3.isDragging = true;
            }
        const d4x = carriage4.x - mx;
        const d4y = carriage4.y - my;
        if (!dragok &&
            d4x * d4x + d4y * d4y < carriage4.r * carriage4.r &&
            mx > case4.x &&
            mx < case4.x + case4.width &&
            my > case4.y &&
            my < case4.y + case4.height) {
                dragok = true;
                carriage4.isDragging = true;
                case4.isDragging = true;
            }
        // сохраняем текущую позицию мыши
        startX = mx;
        startY = my;
    }
    // обрабатываем события нажатия мыши
    function myUp(e) {
        // сообщаем браузеру, что мы обрабатываем это событие мыши
        e.preventDefault();
        e.stopPropagation();
        // очищаем все флаги перетаскивания
        dragok = false;
        for (let i = 0; i < cases.length; i++) {
            for (let k = 0; k < carriages.length; k++) {
                cases[i].isDragging = false;
                carriages[k].isDragging = false;
            }
        }
    }
    // обрабатываем движения мыши
    function myMove(e) {
        // если мы что-то перетаскиваем
        if (dragok) {
            // сообщаем браузеру, что мы обрабатываем это событие мыши
            e.preventDefault();
            e.stopPropagation();
            // получаем текущую позицию мыши
            const mx = parseInt(e.clientX - offsetX);
            const my = parseInt(e.clientY - offsetY);
            // вычисляем расстояние, на которое переместилась мышь
            // с момента последнего перемещения мыши
            const dx = mx - startX;
            const dy = my - startY;
            // перемещаем каждый прямоугольник, который является перетаскиваемым
            // по расстоянию, на которое переместилась мышь
            // с момента последнего перемещения мыши
            if (case1.isDragging) {
                case1.x += dx;
            }
            if (case2.isDragging) {
                case2.x += dx;
            }
            if (case3.isDragging) {
                case3.x += dx;
            }
            if (case4.isDragging) {
                case4.x += dx;
            }
            // ограничения движений
            // ограничения первого крана
            if (case1.x < 0) {case1.x = 0};
            if (case1.x + 20 > case2.x && case1.isDragging == true) {case1.x = case2.x - 20};
            // ограничения второго крана
            if (case2.x < case1.x + 20) {case2.x = case1.x + 20};
            if (case2.x + 20 > case3.x && case2.isDragging == true) {case2.x = case3.x - 20};
            // ограничения третьего крана
            if (case3.x < case2.x + 20) {case3.x = case2.x + 20};
            if (case3.x + 20 > case4.x && case3.isDragging == true) {case3.x = case4.x - 20};
            // ограничения четвертого крана
            if (case4.x < case3.x + 20) {case4.x = case3.x + 20};
            if (case4.x + 20 > WIDTH) {case4.x = WIDTH - 20};
            // перемещаем каждый круг, который является перетаскиваемым
            // по расстоянию, на которое переместилась мышь
            // с момента последнего перемещения мыши
            if (carriage1.isDragging){
                carriage1.x += dx;
                carriage1.y += dy;
            }
            if (carriage2.isDragging){
                carriage2.x += dx;
                carriage2.y += dy;
            }
            if (carriage3.isDragging){
                carriage3.x += dx;
                carriage3.y += dy;
            }
            if (carriage4.isDragging){
                carriage4.x += dx;
                carriage4.y += dy;
            }
            // ограничения движений
            // ограничения первого круга
            if (carriage1.x < 10) {carriage1.x = 10};
            if (carriage1.y + 10 > 138) {carriage1.y = 138 - 10};
            if (carriage1.y < 24) {carriage1.y = 24};
            // ограничения второго круга
            if (carriage2.y + 10 > 138) {carriage2.y = 138 - 10};
            if (carriage2.y < 24) {carriage2.y = 24};
            // ограничения третьего круга
            if (carriage3.y + 10 > 138) {carriage3.y = 138 - 10};
            if (carriage3.y < 24) {carriage3.y = 24};
            // ограничения четвертого круга
            if (carriage4.x + 10 > WIDTH) {carriage4.x = WIDTH - 10};
            if (carriage4.y + 10 > 138) {carriage4.y = 138 - 10};
            if (carriage4.y < 24) {carriage4.y = 24};
            // краны не могут заезжать друг за друга
            // поэтому просто будут сталкиваться и оставаться на месте
            // ограничение первого
            if (carriage1.x + 20 > carriage2.x && carriage1.isDragging == true) {carriage1.x = carriage2.x - 20};
            // ограничение второго
            if (carriage2.x < carriage1.x + 20) {carriage2.x = carriage1.x + 20};
            if (carriage2.x + 20 > carriage3.x && carriage2.isDragging == true) {carriage2.x = carriage3.x - 20};
            // ограничение третьего
            if (carriage3.x < carriage2.x + 20) {carriage3.x = carriage2.x + 20};
            if (carriage3.x + 20 > carriage4.x && carriage3.isDragging == true) {carriage3.x = carriage4.x - 20};
            // ограничение четвертого
            if (carriage4.x < carriage3.x + 20) {carriage4.x = carriage3.x + 20};
            // перерисовываем сцену с новыми позициями прямоугольников
            draw();
            // сбрасываем начальную позицию мыши для следующего перемещения мыши
            startX = mx;
            startY = my;
        }
    }
    // функции опускания кареток кранов
    down_button_1.onclick = function(){
        if (carriage1.is_upper){
            carriage1.is_upper = false;
            down_button_1.textContent = 'Поднять';
            span_1.textContent = 'опущенном\u00A0';
            span_1.style.color = '#FF0000';
        } else {
            carriage1.is_upper = true;
            down_button_1.textContent = 'Опустить';
            span_1.textContent = 'поднятом\u00A0';
            span_1.style.color = '#0000FF';
        }
    }
    down_button_2.onclick = function(){
        if (carriage2.is_upper){
            carriage2.is_upper = false;
            down_button_2.textContent = 'Поднять';
            span_3.textContent = 'опущенном\u00A0';
            span_3.style.color = '#FF0000';
        } else {
            carriage2.is_upper = true;
            down_button_2.textContent = 'Опустить';
            span_3.textContent = 'поднятом\u00A0';
            span_3.style.color = '#0000FF';
        }
    }
    down_button_3.onclick = function(){
        if (carriage3.is_upper){
            carriage3.is_upper = false;
            down_button_3.textContent = 'Поднять';
            span_5.textContent = 'опущенном\u00A0';
            span_5.style.color = '#FF0000';
        } else {
            carriage3.is_upper = true;
            down_button_3.textContent = 'Опустить';
            span_5.textContent = 'поднятом\u00A0';
            span_5.style.color = '#0000FF';
        }
    }
    down_button_4.onclick = function(){
        if (carriage4.is_upper){
            carriage4.is_upper = false;
            down_button_4.textContent = 'Поднять';
            span_7.textContent = 'опущенном\u00A0';
            span_7.style.color = '#FF0000';
        } else {
            carriage4.is_upper = true;
            down_button_4.textContent = 'Опустить';
            span_7.textContent = 'поднятом\u00A0';
            span_7.style.color = '#0000FF';
        }
    }
    // функции подцепливания ковша кранами
    take_ladle_1.onclick = function(){
        if (carriage1.with_ladle && !carriage1.is_upper){
            carriage1.with_ladle = false;
            take_ladle_1.textContent = 'Подцепить ковш';
            span_2.textContent = 'разгружен';
            span_2.style.color = '#0000ff';
        } else if (!carriage1.with_ladle && !carriage1.is_upper){
            carriage1.with_ladle = true;
            take_ladle_1.textContent = 'Отцепить ковш';
            span_2.textContent = 'загружен';
            span_2.style.color = '#ff0000';
        }
    }
    take_ladle_2.onclick = function(){
        if (carriage2.with_ladle && !carriage2.is_upper){
            carriage2.with_ladle = false;
            take_ladle_2.textContent = 'Подцепить ковш';
            span_4.textContent = 'разгружен';
            span_4.style.color = '#0000ff';
        } else if (!carriage2.with_ladle && !carriage2.is_upper){
            carriage2.with_ladle = true;
            take_ladle_2.textContent = 'Отцепить ковш';
            span_4.textContent = 'загружен';
            span_4.style.color = '#ff0000';
        }
    }
    take_ladle_3.onclick = function(){
        if (carriage3.with_ladle && !carriage3.is_upper){
            carriage3.with_ladle = false;
            take_ladle_3.textContent = 'Подцепить ковш';
            span_6.textContent = 'разгружен';
            span_6.style.color = '#0000ff';
        } else if (!carriage3.with_ladle && !carriage3.is_upper){
            carriage3.with_ladle = true;
            take_ladle_3.textContent = 'Отцепить ковш';
            span_6.textContent = 'загружен';
            span_6.style.color = '#ff0000';
        }
    }
    take_ladle_4.onclick = function(){
        if (carriage4.with_ladle && !carriage4.is_upper){
            carriage4.with_ladle = false;
            take_ladle_4.textContent = 'Подцепить ковш';
            span_8.textContent = 'разгружен';
            span_8.style.color = '#0000ff';
        } else if (!carriage4.with_ladle && !carriage4.is_upper){
            carriage4.with_ladle = true;
            take_ladle_4.textContent = 'Отцепить ковш';
            span_8.textContent = 'загружен';
            span_8.style.color = '#ff0000';
        }
    }
    // Функция движения тени
    const moveShadows = setInterval(function() {
        // Смещение по горизонтали 1 тени
        if (shadow1.x > carriage1.x){
            if (Math.abs(shadow1.x - carriage1.x) < 18){
                shadow1.x -= Math.abs(shadow1.x - carriage1.x);
            } else {shadow1.x -= 18;}
        } else if (shadow1.x < carriage1.x){
            if (Math.abs(shadow1.x - carriage1.x) < 18){
                shadow1.x += Math.abs(shadow1.x - carriage1.x);
            } else {shadow1.x += 18;}
        }
        // Смещение по горизонтали 2 тени
        if (shadow2.x > carriage2.x){
            if (Math.abs(shadow2.x - carriage2.x) < 18){
                shadow2.x -= Math.abs(shadow2.x - carriage2.x);
            } else {shadow2.x -= 18;}
        } else if (shadow2.x < carriage2.x){
            if (Math.abs(shadow2.x - carriage2.x) < 18){
                shadow2.x += Math.abs(shadow2.x - carriage2.x);
            } else {shadow2.x += 18;}
        }
        // Смещение по горизонтали 3 тени
        if (shadow3.x > carriage3.x){
            if (Math.abs(shadow3.x - carriage3.x) < 18){
                shadow3.x -= Math.abs(shadow3.x - carriage3.x);
            } else {shadow3.x -= 18;}
        } else if (shadow3.x < carriage3.x){
            if (Math.abs(shadow3.x - carriage3.x) < 18){
                shadow3.x += Math.abs(shadow3.x - carriage3.x);
            } else {shadow3.x += 18;}
        }
        // Смещение по горизонтали 4 тени
        if (shadow4.x > carriage4.x){
            if (Math.abs(shadow4.x - carriage4.x) < 18){
                shadow4.x -= Math.abs(shadow4.x - carriage4.x);
            } else {shadow4.x -= 18;}
        } else if (shadow4.x < carriage4.x){
            if (Math.abs(shadow4.x - carriage4.x) < 18){
                shadow4.x += Math.abs(shadow4.x - carriage4.x);
            } else {shadow4.x += 18;}
        }
        // Смещение по вертикали 1 тени
        if (shadow1.x == carriage1.x){
            if (shadow1.y > carriage1.y){
                if (Math.abs(shadow1.y - carriage1.y) < 18){
                    shadow1.y -= Math.abs(shadow1.y - carriage1.y);
                } else {shadow1.y -= 18;}
            } else if (shadow1.y < carriage1.x){
                if (Math.abs(shadow1.y - carriage1.y) < 18){
                    shadow1.y += Math.abs(shadow1.y - carriage1.y);
                } else {shadow1.y += 18;}
            }
        }
        // Смещение по вертикали 2 тени
        if (shadow2.x == carriage2.x){
            if (shadow2.y > carriage2.y){
                if (Math.abs(shadow2.y - carriage2.y) < 18){
                    shadow2.y -= Math.abs(shadow2.y - carriage2.y);
                } else {shadow2.y -= 18;}
            } else if (shadow2.y < carriage2.x){
                if (Math.abs(shadow2.y - carriage2.y) < 18){
                    shadow2.y += Math.abs(shadow2.y - carriage2.y);
                } else {shadow2.y += 18;}
            }
        }
        // Смещение по вертикали 3 тени
        if (shadow3.x == carriage3.x){
            if (shadow3.y > carriage3.y){
                if (Math.abs(shadow3.y - carriage3.y) < 18){
                    shadow3.y -= Math.abs(shadow3.y - carriage3.y);
                } else {shadow3.y -= 18;}
            } else if (shadow3.y < carriage3.x){
                if (Math.abs(shadow3.y - carriage3.y) < 18){
                    shadow3.y += Math.abs(shadow3.y - carriage3.y);
                } else {shadow3.y += 18;}
            }
        }
        // Смещение по вертикали 4 тени
        if (shadow4.x == carriage4.x){
            if (shadow4.y > carriage4.y){
                if (Math.abs(shadow4.y - carriage4.y) < 18){
                    shadow4.y -= Math.abs(shadow4.y - carriage4.y);
                } else {shadow4.y -= 18;}
            } else if (shadow4.y < carriage4.x){
                if (Math.abs(shadow4.y - carriage4.y) < 18){
                    shadow4.y += Math.abs(shadow4.y - carriage4.y);
                } else {shadow4.y += 18;}
            }
        }
        draw();
    }, 500)
    // Функция получения куки, нужна для получения CSRF-Токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                // const cookie = jQuery.trim(cookies[i]);
                const cookie = cookies[i].trim();
                //if (cookie.startsWith(name + '=')) {
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break; // Выходим, как только найдём нужное cookie
                }
            }
        }
        return cookieValue;
    }
    // Функция отправки данных
    const createData = setInterval(function() {
        let data = {
            "Crane_7": {
                "x": Math.round(shadow1.x/18),
                "y": Math.round((shadow1.y-10)/18),
                "is_ladle": carriage1.with_ladle,
                "is_upper":   carriage1.is_upper
            },
            "Crane_8": {
                "x": Math.round(shadow2.x/18),
                "y": Math.round((shadow2.y-10)/18),
                "is_ladle": carriage2.with_ladle,
                "is_upper":   carriage2.is_upper
            },
            "Crane_9": {
                "x": Math.round(shadow3.x/18),
                "y": Math.round((shadow3.y-10)/18),
                "is_ladle": carriage3.with_ladle,
                "is_upper":   carriage3.is_upper
            },
            "Crane_10": {
                "x": Math.round(shadow4.x/18),
                "y": Math.round((shadow4.y-10)/18),
                "is_ladle": carriage4.with_ladle,
                "is_upper":   carriage4.is_upper
            },
        };
        // Создание форм-даты и добавление информации
        let formdata = new FormData();
        formdata.append("cranes_pos", JSON.stringify(data));
        // ajax post запрос
        $.ajax({
            url: '',         /* Куда отправить запрос */
            type: 'POST',             /* Метод запроса (post или get) */
            processData: false,       // Отключаем обработку данных
            contentType: false,       // Отказываемся от автоматического определения типа содержимого
            data: formdata,     /* Передаваемые данные */
            headers: {'X-CSRFToken': getCookie('csrftoken')}, // Установка CSRF-токена в заголовок
            success: function(){   /* функция которая будет выполнена после успешного запроса.  */
                 console.log('Ajax post success');
            },
            error: function(response){
                console.log(response);
            }
        });
    }, 1000)
});