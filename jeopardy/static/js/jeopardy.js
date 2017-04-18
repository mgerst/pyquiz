class Jeopardy {
    constructor() {
        this.socket = io.connect(`http://${document.domain}:${location.port}`);

        this.boardName = document.querySelector('#board-name');
        this.categories = document.querySelector('#category-headers');
        this.questions = document.querySelector('#questions');

        // Deal with 'this'
        this.onConnect = this.onConnect.bind(this);
        this.onCurrentBoard = this.onCurrentBoard.bind(this);
        this.onQuestionOpen = this.onQuestionOpen.bind(this);

        // Event Listeners
        this.socket.on('connect', this.onConnect);
        this.socket.on('board.current', this.onCurrentBoard);
        this.socket.on('question.open', this.onQuestionOpen);
    }

    onConnect() {
        this.socket.emit('board.current');
    }

    onCurrentBoard(data) {
        this.boardName.innerHTML = data.name;
        this.categories.innerHTML = "";
        this.questions.innerHTML = "";

        let cat_template = "<tr>";
        let quests = [];

        for (let id in data.categories) {
            let category = data.categories[id];
            cat_template += `<th class="cat" data-id="${category.id}">${category.name}</th>`;

            quests.push(category.questions);
        }

        cat_template += "</tr>";

        let question_template = "";

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

        this.categories.innerHTML = cat_template;
        this.questions.innerHTML = question_template;
    }

    onQuestionOpen(data) {
        console.log(data);
    }
};