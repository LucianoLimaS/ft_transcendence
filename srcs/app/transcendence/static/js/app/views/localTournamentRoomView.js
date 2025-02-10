import AbstractView from "./abstractView.js";
import PongRoomManager from "../managers/PongRoomManager.js";
import LocalTournamentManager from "../managers/localTournamentManager.js";
import { navigateTo } from "../index.js";

export default class LocalTournamentRoomView extends AbstractView {
    constructor() {
        super();
        this.setTitle("Local Tournament Room");
        this.pongRoomManager = new PongRoomManager();
        this.localTournamentManager = new LocalTournamentManager();
        this.isCanvasFocused = true;

        this.handleBlur = this.handleBlur.bind(this);
        this.handleFocus = this.handleFocus.bind(this);
        this.handleWinner = this.handleWinner.bind(this);
        this.handleKeyEvent = this.handleKeyEvent.bind(this);
        this.handleClickStartButton = this.handleClickStartButton.bind(this);
        this.handleClickStartButtonReturn = this.handleClickStartButtonReturn.bind(this);
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            return html;
        }
        catch(error) {
            return "<p>Error loading Room page</p>";
        }
    }

    loadComponents() {
        this.initGame();
        this.match = this.localTournamentManager.matches.find(m => m.roomId == this.pongRoomManager.gameData.roomId);
        if (!this.match) {
            return;
        }
        this.displayPlayers();
    }

    displayPlayers() {
        const roomId = this.pongRoomManager.gameData.roomId;

        // Get the player elements
        const player1Element = document.getElementById(`${roomId}-p1`);
        const player2Element = document.getElementById(`${roomId}-p2`);
        document.getElementById('player1').classList.remove("d-none");
        document.getElementById('player2').classList.remove("d-none");


        if (player1Element && player2Element) {
            // Set the player names
            player1Element.textContent = this.match[`${this.match.matchId}-p1`] || "TBD";
            player2Element.textContent = this.match[`${this.match.matchId}-p2`] || "TBD";

            // Make the elements visible
            player1Element.classList.remove("d-none");
            player2Element.classList.remove("d-none");
        } else {
        }
    }

    unloadComponents() {
        this.pongRoomManager.socket.close();
    }

    bindUIEventHandlers() {
        this.bindMovementHandlers();
        this.bindStartButtonHandler();
        this.bindPongRoomEventHandlers();
        this.bindCanvasFocusEvents();
    }

    removeUIEventHandlers() {
        this.unbindMovementHandler();
        this.unbindStartButtonHandler();
        this.unbindPongRoomEventHandlers();
    }

    //Creating game canvas and connecting to socket

    initGame()
    {
        this.loadGameData();

        this.pongRoomManager.createGame();

        this.pongRoomManager.connectSocket();

        this.pongRoomManager.loadSocketEventHandlers();
    }

    loadGameData() {
        //Get canvas and context
        const canvas = document.getElementById("pongCanvas");
        const context = canvas.getContext("2d");
    
        //Get game info
        const gameData = document.getElementById("game-data");
        const roomId = gameData.dataset.roomId;
        const gameMode = gameData.dataset.gameMode;

        this.pongRoomManager.setGameData(context, canvas.width, canvas.height, roomId, gameMode);
    }

    //Key events Handlers

    handleKeyEvent(event, keyType) {
        const validKeys = ["ArrowUp", "ArrowDown", "w", "s", "W", "S"];
        if (validKeys.includes(event.key) && this.isCanvasFocused) {
          event.preventDefault();
          const message = {
            type: keyType,
            key: event.key.toLocaleLowerCase(),
          };
          this.pongRoomManager.sendMessage(message);
        }
    }

    handleKeydown = (event) => this.handleKeyEvent(event, "keydown");

    handleKeyup = (event) => this.handleKeyEvent(event, "keyup");

    handleClickStartButton() {
        const message = {
          type: "start_game",
        };
        document.getElementById("pongCanvas").focus();
        this.isCanvasFocused = true;
        this.pongRoomManager.sendMessage(message);
    }

    handleClickStartButtonReturn() {
        const nplayers = this.localTournamentManager.num_of_players;
        const tourn_url = `/localTournament/${nplayers}/`;
        navigateTo(tourn_url);
    }

    //PongRoom Events Handlers

    handleGameHasStarted() {
        const startButton = document.getElementById("startGame");
        if (startButton) {
            startButton.style.display = "none";
        }
        const messageContainer = document.getElementById("messageContainer");
        if (messageContainer) {
            messageContainer.textContent = "Game has started!";
        }
    }

    handleWinner(event) {
        const messageContainer = document.getElementById("messageContainer");
        const winnerName = this.getWinnerName(event.detail);
        this.localTournamentManager.updateMatchesOnWinner(this.match.matchId, winnerName);
        const startButton = document.getElementById("startGame");
        if (messageContainer) {
            messageContainer.textContent = `${winnerName} wins!`;
        }
        if (startButton) {
            startButton.removeEventListener("click", this.handleClickStartButton);
            startButton.addEventListener("click", this.handleClickStartButtonReturn);
            startButton.textContent = "Back to Tournament!";
            startButton.style.display = "block";
        }
    }

    getWinnerName(playerPosition) {
        if (playerPosition == 'right')
            return this.match[`${this.match.matchId}-p2`];
        if (playerPosition == 'left')
            return this.match[`${this.match.matchId}-p1`];
    }

    handleRedirectTournament(event) {
    }

    //CanvasFocus Event Handlers

    handleFocus() {
        this.isCanvasFocused = true;
    }

    handleBlur() {
        this.isCanvasFocused = false;
    }

    //Binders
    bindPongRoomEventHandlers() {
        document.addEventListener('GameStarted', this.handleGameHasStarted);
        document.addEventListener('Winner', this.handleWinner);
        document.addEventListener('RedirectTournament', this.handleRedirectTournament);
    }

    bindMovementHandlers() {
        document.addEventListener("keydown", this.handleKeydown);
        document.addEventListener("keyup", this.handleKeyup);
    }

    bindStartButtonHandler() {
        const startButton = document.getElementById("startGame");
        if (startButton) {
            startButton.addEventListener("click", this.handleClickStartButton);
        }
    }

    bindCanvasFocusEvents() {
        const canvas = document.getElementById("pongCanvas");
        if (canvas) {
            canvas.addEventListener("focus", this.handleFocus);
            canvas.addEventListener("blur", this.handleBlur);
        }
    }

    //Unbinders
    unbindMovementHandler() {
        document.removeEventListener("keydown", this.handleKeydown);
        document.removeEventListener("keyup", this.handleKeyup);
    }

    unbindStartButtonHandler() {
        const startButton = document.getElementById("startGame");
        if (startButton) {
            startButton.removeEventListener("click", this.handleClickStartButton);
            startButton.removeEventListener("click", this.handleClickStartButtonReturn);
        }
    }

    unbindPongRoomEventHandlers() {
        document.removeEventListener('GameStarted', this.handleGameHasStarted);
        document.removeEventListener('Winner', this.handleWinner);
        document.removeEventListener('RedirectTournament', this.handleRedirectTournament);
    }
}