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
        for (let i = 0; i < cases.length; i++){
            for (let k = 0; k < carriages.length; k++){
                cas = cases[i]
                car = carriages[k]
                const dx = car.x - mx;
                const dy = car.y - my;
                // проверяем, находится ли внутри мышь
                if (!dragok &&
                    dx * dx + dy * dy < car.r * car.r &&
                    mx > cas.x &&
                    mx < cas.x + cas.width &&
                    my > cas.y &&
                    my < cas.y + cas.height) {

                    dragok = true;
                    car.isDragging = true;
                    cas.isDragging = true;
                }
            }
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
            for (let i = 0; i < cases.length; i++) {
                const cas = cases[i];
                if (cas.isDragging) {
                    cas.x += dx;
                }
                // ограничения движений
                let crane1 = cases[0];
                let crane2 = cases[1];
                let crane3 = cases[2];
                let crane4 = cases[3];
                if (crane1.x < 0) {crane1.x = 0}
                if (crane1.x + 20 > crane2.x) {crane1.x = crane2.x - 20}

                if (crane2.x < crane1.x + 20) {crane2.x = crane1.x}
                if (crane2.x + 20 > crane3.x) {crane2.x = crane3.x - 20}


                if (crane3.x + 20 > crane4.x) {crane3.x = crane4.x - 20}

                if (crane4.x + 20 > WIDTH) {crane4.x = WIDTH - 20}

            }
            for (let k = 0; k < carriages.length; k++) {
                const car = carriages[k];
                if (car.isDragging){
                    car.x += dx;
                    car.y += dy;
                }
                if (car.x + 10 > WIDTH) {car.x = WIDTH - 10}
                if (car.x < 10) {car.x = 10}
                if (car.y + 10 > 151) {car.y = 151 - 10}
                if (car.y < 12) {car.y = 12}
            }

            // перерисовываем сцену с новыми позициями прямоугольников
            draw();

            // сбрасываем начальную позицию мыши для следующего перемещения мыши
            startX = mx;
            startY = my;
        }
    }
});