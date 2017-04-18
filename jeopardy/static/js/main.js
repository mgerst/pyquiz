var socket = io.connect('http://' + document.domain + ':' + location.port);
let current_question = null;
let iam = null;

socket.on('connect', function() {
    socket.emit('whoami');
    socket.emit('board.current');
});

socket.on('you.are', data => {
    iam = data;

    if (iam.admin) {
        setupTeamAwards();
    }
});

socket.on('board.current', function(data) {
    drawBoard(data);
});

socket.on('correct.answer', function (data) {
    console.log("Showing " + data.answer);
    $('#question').html("Answer: " + data.answer);
    $('#question').show();
    $('#continue').show();
    $('#correct-response').hide();
    $('#buzzer-div').hide();
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

socket.on('question.open', async function (data) {
    current_question = data;
    var prompt = {};
    console.log(data);
    $('#game').hide();
    if (data.daily_double) {
        $('#dailydouble').show();
        await sleep(5000);
    }
    $('#question, #answer, #prompt').css({"display": "block"});
    $('#question').html(data.answer);
    $('#answer').html(data.question);
    $('#question, #answer, #prompt').css({"visibility": "visible"});
    $('#question, #prompt').hide();
    $('#continue').hide();
    $('#reopen').hide();

    $('#prompt').fadeIn(1000);
    if ($('#correct-response') != null)
        $('#correct-response').show();
    $('#buzzer-div').show();
});

socket.on('team.taken', data => {
    let team = data['id'];
    let name = data['name'];

    let div = document.querySelector(`.team[data-id="${team}"]`);
    div.dataset.exists = "true";
    div.querySelector('.name').innerHTML = name;
    div.querySelector('.score').innerHTML = '0';
});

socket.on('team.award', data => {
    let team = data['team'];

    let score = document.querySelector(`.team[data-id="${team}"] .score`);
    score.innerHTML = data['score'];
});

socket.on('buzzer.opened', function () {
    $('#team_buzzed').html();
    $('#buzzer').on("click");
    $('#buzzer').css('background-color', '#4caf50');
    $('#team_buzzed').html("");
});

socket.on('question.close', function (data) {
    console.log(data);
    if (data.remove) {
        $('#' + data.question.category + '_' + data.question.id).html("");
        var old = document.getElementById(data.question.category + '_' + data.question.id);
        var new_ = old.cloneNode(true);
        old.parentNode.replaceChild(new_, old);
    }
    $('#question, #answer, #prompt').css({"visibility": "hidden"});
    $('#question, #answer, #prompt').css({"display": "none"});
    $('#game').show();

    current_question = null;
});

socket.on('buzzer.clicked', function (data) {
    $('#buzzer').css('background-color', 'red');
    $('#buzzer').off("click");
    $('#team_buzzed').html("Team " + data.team + " buzzed in!");
    $('#reopen').show();
});

$('#continue').click(function () {
    socket.emit('question.close', {remove: true});
});

$('#correct-response').click(function () {
    $('#question').show();
    socket.emit('correct.answer', {});
});

function buzzer() {
    socket.emit('buzzer.clicked', {});
    $('#buzzer').css('background-color', 'red');
}

$('#buzzer').click(buzzer);
$('body').keypress(buzzer);

$('#reopen').click(function () {
    socket.emit('buzzer.open', {});
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
                if (question.visible)
                    row_template += `<td class="question" data-category="${question.category}" data-id="${question.id}" id="${question.category}_${question.id}">${question.value}</td>`;
                else
                    row_template += `<td></td>`;
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

function teamAward(evt) {
    console.debug(evt);

    if (current_question && evt.target.dataset.exists === "true") {
        let team = evt.target.dataset.id;
        socket.emit('team.award', {team: team, correct: true});
    }
}

function teamDeduct(evt) {
    evt.preventDefault();
    if (current_question && evt.target.dataset.exists === "true") {
        let team = evt.target.dataset.id;
        socket.emit('team.award', {team: team, correct: false});
    }
}

function setupClickListeners() {
    let map = Array.prototype.map;
    let els = document.querySelectorAll(".question");
    map.call(els, function (el) {
        el.addEventListener("click", function (evt) {
            socket.emit('question.open', {category: this.dataset.category, id: this.dataset.id});
            socket.emit('buzzer.open', {});
        });
    });
}

function setupTeamAwards() {
    console.log("Setting up team awards");
    let map = Array.prototype.map;
    let teams = document.querySelectorAll('.team');
    map.call(teams, el => {
        el.addEventListener("click", teamAward);
        el.addEventListener("contextmenu", teamDeduct);
    });
}
