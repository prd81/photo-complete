"use strict";

// When true, moving the mouse draws on the canvas
let isDrawing = false;
let x = 0;
let y = 0;

const myPics = document.getElementById("myPics");
const context = myPics.getContext("2d");

// Set dimensions of canvas equal to those of the picture
const img = document.getElementById("img");
myPics.height = img.height;
myPics.width = img.width;

//mask getter
function send_mask() {
    const imageURI = myPics.toDataURL("image/jpeg", 1.0);
    $.ajax({
        type: "POST",
        url: "/upload",
        data: { URI: imageURI },
    }).done(function (response) {
        location.href = "/results" + "?rnd=" + Math.trunc(Math.random() * 2);
    });
}
//save button add listener
document.getElementById("button").addEventListener("click", send_mask);

// event.offsetX, event.offsetY gives the (x,y) offset from the edge of the canvas.

// Add the event listeners for mousedown, mousemove, and mouseup
myPics.addEventListener("mousedown", (e) => {
    x = e.offsetX;
    y = e.offsetY;
    isDrawing = true;
});

myPics.addEventListener("mousemove", (e) => {
    if (isDrawing === true) {
        drawLine(context, x, y, e.offsetX, e.offsetY);
        x = e.offsetX;
        y = e.offsetY;
    }
});

window.addEventListener("mouseup", (e) => {
    if (isDrawing === true) {
        drawLine(context, x, y, e.offsetX, e.offsetY);
        x = 0;
        y = 0;
        isDrawing = false;
    }
});

function drawLine(context, x1, y1, x2, y2) {
    context.beginPath();
    context.strokeStyle = "white";
    context.lineWidth = 10;
    context.moveTo(x1, y1);
    context.lineTo(x2, y2);
    context.stroke();
    context.closePath();
}
