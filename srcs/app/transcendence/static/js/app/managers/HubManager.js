export default class HubManager {
    constructor() {

    }

    setTournamentHubData(tournamentId, gameMode, username) {
        this.gameData = {
            "tournamentId": tournamentId,
            "gameMode": gameMode,
            "username": username,
        }
    }

    connectSocket() {
        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        const socketUrl = `${protocol}://${window.location.host}/ws/pong/tournament/${this.gameData.tournamentId}/`;
        this.socket = new WebSocket(socketUrl);
    }

    loadSocketEventHandlers() {
        this.socket.onopen = (event) => {
        };

        this.socket.onmessage = (event) => {
            this.handleSocketMessage(event);
        };

        this.socket.onclose = (event) => {
        };

        this.socket.onerror = (event) => {
        };
    }

    joinTournament() {
        this.sendMessage({
            type: "join_tournament"
        });
    }

    sendMessage(message) {
        const jsonMessage = JSON.stringify(message);
        this.socket.send(jsonMessage);
    }

    handleSocketMessage(event) {
        const data = JSON.parse(event.data);

        switch (data.type) {
            case "not_auth":
                alert(data.message);
                this.socket.close();
                break;

            case "joined":
                document.dispatchEvent(new CustomEvent("joinedTournament"));
                break;

            case "current_state":
                document.dispatchEvent(new CustomEvent("currentState", { detail: data }));
                break;

            case "tournament_message":
                document.dispatchEvent(new CustomEvent("tournamentMessage", { detail: data }));
                break;

    
          case "error":
            document.dispatchEvent(new CustomEvent("Error", {detail: data.message}));
            break;
      
          default:
        }
    }
}
