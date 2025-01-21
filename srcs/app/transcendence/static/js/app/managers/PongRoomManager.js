import { PongGame } from "/static/pong/js/PongGame.js";

export default class PongRoomManager {
    constructor () {

        this.handleSocketOpen = this.handleSocketOpen.bind(this);
        this.handleSocketMessage = this.handleSocketMessage.bind(this);
    }

    setGameData(context, width, height, roomId, gameMode) {
        this.gameData = {
            'context': context,
            'width': width,
            'height': height,
            'roomId': roomId,
            'gameMode': gameMode
        }
    }

    connectSocket()
    {
        let socketUrl;

        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        if (this.gameData.gameMode === "tournament") {
            socketUrl = `${protocol}://${window.location.host}/ws/pong/tournament_match/${this.gameData.roomId}/`;
        } else {
            socketUrl = `${protocol}://${window.location.host}/ws/pong/${this.gameData.gameMode}/`;
        }

        this.socket = new WebSocket(socketUrl);
    }

    createGame()
    {
        //Initialize game
        this.pongGame = new PongGame(this.gameData.context, this.gameData.width, this.gameData.height);
    }

    loadSocketEventHandlers() {
        this.socket.onopen = (event) => {
            this.handleSocketOpen(event);
        };

        this.socket.onmessage = (event) => {
            this.handleSocketMessage(event);
        };

        this.socket.onclose = (event) => {
        };

        this.socket.onerror = (event) => {
        };
    }

    handleSocketOpen(event) {
        const message = {
            type: "join_room",
            room_id: this.gameData.roomId,
            width: this.gameData.width,
            height: this.gameData.height,
        };
        this.sendMessage(message);
    }

    handleSocketMessage(event) {
        const data = JSON.parse(event.data);

        switch (data.type) {
            case "not_auth":
                alert(data.message);
                socket.close();
                break;

            case "game_init":
                this.pongGame.drawGameState(data.game_state);
                break;

            case "update_game_state":
                this.pongGame.drawGameState(data.game_state);
                break;

            case "game_has_started":
                document.dispatchEvent(new CustomEvent('GameStarted'));
                break;

            case "winner":
                document.dispatchEvent(new CustomEvent('Winner', {detail: data.winner}));
                break;

            case "tournament_match_winner":
                    document.dispatchEvent(new CustomEvent('TournamentMatchWinner', {detail: data.winner}));
                    break;

            case "redirect_tournament":
                document.dispatchEvent(new CustomEvent('RedirectTournament', {detail: data.redirect}));
                break

            case "alert_message":
                document.dispatchEvent(new CustomEvent('AlertMsg', {detail: data.message}));
                break

            default:

        }
    }

    sendMessage(message) {
        const jsonMessage = JSON.stringify(message);
        this.socket.send(jsonMessage);
    }
}
