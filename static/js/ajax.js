$("#targeton").click(function () {
    $.get('/test', function (data) {
        console.log(data);
    })
    // $.ajax({
    //     url: '/test',         /* Куда пойдет запрос */
    //     method: 'get',             /* Метод передачи (post или get) */
    //     dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
    //     data: {text: 'Текст'},     /* Параметры передаваемые в запросе. */
    //     success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
    //         alert(data);            /* В переменной data содержится ответ от index.php. */
    //     }
    // });
});
$("#targetoff").click(function () {
    alert("Handler for .click() called.");
});
$("#home-button").click(function () {
});
$("#parametrs-button").click(function () {
});
$("#errors-button").click(function () {
});
$("#start-engine").click(function () {
    window.location = '/start_engine';
});
$("#stop-engine").click(function () {
    window.location = '/stop_engine';
});
$("#change-car").click(function () {
    alert("Ты нажал на сменить машину");
});
$("#log-out").click(function () {
    alert("Ты нажал на выход");
});