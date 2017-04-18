var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('board.current');
});

socket.on('board.current', function(data) {
    drawBoard(data);
});

socket.on('correct.answer', function (data) {
    console.log("Showing " + data.answer);
    $('#question').html(data.answer);
    $('#question').show();
});

socket.on('question.open', function(data) {
    var prompt = {};
    console.log(data);
    $('#game').hide();
    $('#question, #answer, #prompt').css({"display": "block"});
    $('#question').html(data.answer);
    $('#answer').html(data.question);
    var font_size = 24;
    /*
    do {
        $('#question, #answer').css({"font-size": font_size});
        font_size++;
    } while (!getScrollBarState().vScrollbar && font_size < 72)
    */
    $('#question, #answer').css({"font-size": Math.max(24, font_size - 2)});
    $('#question, #answer, #prompt').css({"visibility": "visible"});
    $('#question, #prompt').hide();

    $('#prompt').fadeIn(1000);
    if ($('#correct-response').html() != null)
        $('#correct-response').show();
});

function showAnswer() {
    $('#question').show();
    socket.emit('correct.answer', {});
}

function drawBoard(data) {
    let name = document.querySelector("#board-name");
    let categories = document.querySelector("#category-headers");
    let questions = document.querySelector("#questions");

    name.innerHTML = data.name;
    categories.innerHTML = "";
    questions.innerHTML = "";
    console.log(data);

    var cat_template = "<tr>";
    var quests = [];

    for (let id in data.categories) {
        let category = data.categories[id];
        cat_template += `<th class="cat" data-id="${category.id}">${category.name}</th>`;

        quests.push(category.questions);
    }

    cat_template += "</tr>";

    var question_template = "";
    console.log(quests);

    // For each question row
    for (let i = 0; i < 5; i++) {
        let row_template = "<tr>";

        // For each category column
        for (let c = 0; c < data.categories.length; c++) {
            if (c in quests && i in quests[c]) {
                let question = quests[c][i];

                row_template += `<td class="question" data-category="${question.category}" data-id="${question.id}">${question.value}</td>`;
            }
        }

        row_template += "</tr>";
        question_template += row_template;
    }

    categories.innerHTML = cat_template;
    questions.innerHTML = question_template;
    console.log(quests);
    setupClickListeners();
}

function setupClickListeners() {
    let map = Array.prototype.map;
    let els = document.querySelectorAll(".question");
    map.call(els, function(el) {
        el.addEventListener("click", function(evt) {
            socket.emit('question.open', {category: this.dataset.category, id: this.dataset.id});
        });
    });
}
