window.addEventListener("load", function(){
    // получаем ссылки, связанные с холстом
    const canvas = document.querySelector('.canvas');
    const ctx = canvas.getContext("2d");
    const BB = canvas.getBoundingClientRect();
    const offsetX = BB.left;
    const offsetY = BB.top;
    const WIDTH = canvas.width;
    const HEIGHT = canvas.height;

    // переменные, связанные с перетаскиванием
    let dragok = false;
    let startX;
    let startY;

    // массив объектов, определяющих разные формы
    const cases = [];
    const carriages = [];

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
    carriages.push({ x: 160, y: 100, r: 10, fill: "#ffffff", isDragging: false });
    carriages.push({ x: 460, y: 100, r: 10, fill: "#ffffff", isDragging: false });
    carriages.push({ x: 510, y: 100, r: 10, fill: "#ffffff", isDragging: false });
    carriages.push({ x: 910, y: 100, r: 10, fill: "#ffffff", isDragging: false });


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

        case1 = cases[0]
        case2 = cases[1]
        case3 = cases[2]
        case4 = cases[3]

        carriage1 = carriages[0]
        carriage2 = carriages[1]
        carriage3 = carriages[2]
        carriage4 = carriages[3]

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
        // если мы что-то перетаскиваем...
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

            // перемещаем каждый прямоугольник, который является перетаскиванием
            // по расстоянию, на которое переместилась мышь
            // с момента последнего перемещения мыши

            case1 = cases[0]
            case2 = cases[1]
            case3 = cases[2]
            case4 = cases[3]

            carriage1 = carriages[0]
            carriage2 = carriages[1]
            carriage3 = carriages[2]
            carriage4 = carriages[3]

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

            if (case1.x < 0) {case1.x = 0}
            if (case1.x + 20 > case2.x && case1.isDragging == true) {case1.x = case2.x - 20}

            if (case2.x < case1.x + 20) {case2.x = case1.x + 20}
            if (case2.x + 20 > case3.x && case2.isDragging == true) {case2.x = case3.x - 20}

            if (case3.x < case2.x + 20) {case3.x = case2.x + 20}
            if (case3.x + 20 > case4.x && case3.isDragging == true) {case3.x = case4.x - 20}

            if (case4.x < case3.x + 20) {case4.x = case3.x + 20}
            if (case4.x + 20 > WIDTH) {case4.x = WIDTH - 20}





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

            if (carriage1.x < 10) {carriage1.x = 10}
            if (carriage1.y + 10 > 151) {carriage1.y = 151 - 10}
            if (carriage1.y < 12) {carriage1.y = 12}

            if (carriage2.y + 10 > 151) {carriage2.y = 151 - 10}
            if (carriage2.y < 12) {carriage2.y = 12}

            if (carriage3.y + 10 > 151) {carriage3.y = 151 - 10}
            if (carriage3.y < 12) {carriage3.y = 12}

            if (carriage4.x + 10 > WIDTH) {carriage4.x = WIDTH - 10}
            if (carriage4.y + 10 > 151) {carriage4.y = 151 - 10}
            if (carriage4.y < 12) {carriage4.y = 12}

            if (carriage1.x + 20 > carriage2.x && carriage1.isDragging == true) {carriage1.x = carriage2.x - 20}

            if (carriage2.x < carriage1.x + 20) {carriage2.x = carriage1.x + 20}
            if (carriage2.x + 20 > carriage3.x && carriage2.isDragging == true) {carriage2.x = carriage3.x - 20}

            if (carriage3.x < carriage2.x + 20) {carriage3.x = carriage2.x + 20}
            if (carriage3.x + 20 > carriage4.x && carriage3.isDragging == true) {carriage3.x = carriage4.x - 20}

            if (carriage4.x < carriage3.x + 20) {carriage4.x = carriage3.x + 20}

            // перерисовываем сцену с новыми позициями прямоугольников
            draw();

            // сбрасываем начальную позицию мыши для следующего перемещения мыши
            startX = mx;
            startY = my;
        }
    }
});