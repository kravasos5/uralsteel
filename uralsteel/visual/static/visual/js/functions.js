window.addEventListener("load", (event) => {
    window.canvas = document.getElementById('canvas');
    window.canvas_context = canvas.getContext('2d');
});

window.clear_canvas = function clear_canvas() {
    // Функция, очищающая canvas
    canvas_context.clearRect(0, 0, canvas.width, canvas.height);
};