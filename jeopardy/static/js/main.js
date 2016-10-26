var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('board.current');
});

socket.on('board.current', function(data) {
    drawBoard(data);
});

socket.on('question.open', function(data) {
    console.log(data);
});

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
        cat_template += `<th class="cat" data-id="${category.id}">${category.name}</th>`

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