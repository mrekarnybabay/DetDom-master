let timerId = setTimeout(function tick() {
    alert('tick');
    $.get('/change_parm', function (data) {
        $('#idtype1').val(data.value);
        console.log(data)
    })
    timerId = setTimeout(tick, 10000); // (*)
}, 10000);


// $(window).load(function () {
//     let timerId = setTimeout(function tick() {
//     $.get('/change_parm', function (data) {
//             $('#idtype1').val(data.parm);
//             //console.log('похуй')
//         }
//     )
//     timerId = setTimeout(tick, 10000); // (*)
// }, 10000);
// })

// let timerId = setTimeout(function tick() {
//     $.get('/change_parm', function (data) {
//             $('#idtype1').val(data.parm)
//         }
//     )
//     timerId = setTimeout(tick, 2000); // (*)
// }, 2000);