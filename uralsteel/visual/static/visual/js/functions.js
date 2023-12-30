window.addEventListener("load", (event) => {
    window.canvas = document.getElementById('canvas');
    window.canvas_context = canvas.getContext('2d');
});

window.clear_canvas = function clear_canvas() {
    // Функция, очищающая canvas
    // очищаю canvas
    canvas_context.clearRect(0, 0, canvas.width, canvas.height);
    // выставляю фон canvas
    canvas_context.drawImage(bg_image, 0, 0);
};