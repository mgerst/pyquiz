class Jeopardy {

    constructor() {
        this.socket = io.connect(`http://${document.domain}:${location.port}`);

        // Deal with 'this'
        this.onConnect = this.onConnect.bind(this);
        this.onCurrentBoard = this.onCurrentBoard.bind(this);

        // Event Listeners
        this.socket.on('connect', this.onConnect);
    }

    onConnect() {
        this.socket.emit('board.current');
    }
}