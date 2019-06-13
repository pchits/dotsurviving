
$(document).ready(function() {

    console.log("Going to hunt!");

    function print_to_log(history, status) {
        console.log('print_to_log');
        console.log(history);
        $('.sidebar-content .log').html('<div class="log-line status">' + status + '</div>');
        if (history.length == 0) {
            $('.sidebar-content .log').html('');
        }
        else {
            $(history).each(function (index, value) { 
                $('.sidebar-content .log').append(
                    '<div class="log-line">[' + value[0].toString() + ']</div>'
                );
            });
            
        }
    }

    function move_to_position(x, y, id) {
        let pos = 'table.positions tr.row:nth-child(' + (y + 1) + ') td.cell:nth-child(' + (x + 1) + ')';
        console.log(pos)
        $('#' + id).appendTo($(pos));
    }

    function paint_position(x, y, id) {
        let pos = 'table.positions tr.row:nth-child(' + (y + 1) + ') td.cell:nth-child(' + (x + 1) + ')';
        if (id == 'hunter') {
            $(pos).addClass('hunter-was-there');
        }
    }

    function gameLoop(history, i, steps) {
        setTimeout(function () {
            
            paint_position(history[i][0][0], history[i][0][1], 'hunter')

            move_to_position(history[i][0][0], history[i][0][1], 'hunter');

            i++;
            if (i < steps) {
                gameLoop(history, i, steps);
            }
        }, 100)
    }

    function run_game(history) {

        var i = 0;
        var steps = history.length

        $('.hunter-was-there').removeClass('hunter-was-there');
        console.log('run_game');
        console.log(history)
        
        gameLoop(history, i, steps);
    }

    $('#go-hunt').click(function() {
        $('.sidebar-content .log').html('<div class="log-line status">Loading...</div>');
        $.get("http://127.0.0.1:5000/api/", function(data) {
            
            data_parsed = $.parseJSON(data);
            console.log('data_parsed');
            console.log(data_parsed);

            print_to_log(data_parsed['history'], data_parsed['report']);

            run_game(data_parsed['history']);

        });
    });

    $('#go-generate').click(function() {
        $('.sidebar-content .log').html('<div class="log-line status">Loading...</div>');
        $.get("http://127.0.0.1:5000/api/generate-testdata/", function(data) {
            $('.sidebar-content .log').html('<div class="log-line status">' + data + '</div>');
        });
    });

    $('#go-learn').click(function() {
        $('.sidebar-content .log').html('<div class="log-line status">Loading...</div>');
        $.get("http://127.0.0.1:5000/api/learn/", function(data) {
            $('.sidebar-content .log').html('<div class="log-line status">' + data + '</div>');
        });
    });
});