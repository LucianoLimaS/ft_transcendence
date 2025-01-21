import AbstractView from "./abstractView.js";
import PongRoomManager from "../managers/PongRoomManager.js";
/* import ChatManager from "../managers/ChatManager.js"; */
import { navigateTo } from "../index.js";

export default class Room extends AbstractView {
    constructor() {
        super();
        this.setTitle("Room");
        this.pongRoomManager = new PongRoomManager();
        this.isCanvasFocused = true;

        this.handleFocus = this.handleFocus.bind(this);
        this.handleBlur = this.handleBlur.bind(this);
        this.handleKeyEvent = this.handleKeyEvent.bind(this);
        this.handleClickStartButton = this.handleClickStartButton.bind(this);
        // tenta conectar o socket de chat
        /* const chatManager = new ChatManager();
        chatManager.tryConnectToChatSocket(); */
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('Room html fetched. Returning...');
            return html;
        }
        catch(error) {
            return "<p>Error loading Room page</p>";
        }
    }

    loadComponents() {
        this.initGame();
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
        if (messageContainer) {
            messageContainer.textContent = `${event.detail} wins!`;
        }
        const startButton = document.getElementById("startGame");
        if (startButton) {
            startButton.textContent = "Play Again!";
            startButton.style.display = "block";
        }
    }

    handleTournamentMatchWinner(event) {
        const messageContainer = document.getElementById("messageContainer");
        if (messageContainer) {
            messageContainer.textContent = `${event.detail} wins!`;
        }
    }

    handleRedirectTournament(event) {
        //wait 2 seconds before redirecting
        setTimeout(() => {  navigateTo(event.detail) }, 2000);

    }

    handleAlertMsg(event) {
        const spectadorContainer = document.getElementById("alertContainer");
        if (spectadorContainer) {
            spectadorContainer.textContent = `${event.detail}`;
        }
        const startButton = document.getElementById("startGame");
        if (startButton){
            startButton.style.display = "none";
        }
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
        document.addEventListener('AlertMsg', this.handleAlertMsg);
        document.addEventListener('TournamentMatchWinner', this.handleTournamentMatchWinner);

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
        }
    }

    unbindPongRoomEventHandlers() {
        document.removeEventListener('GameStarted', this.handleGameHasStarted);
        document.removeEventListener('Winner', this.handleWinner);
        document.removeEventListener('RedirectTournament', this.handleRedirectTournament);
        document.removeEventListener('AlertMsg', this.handleAlertMsg);
        document.removeEventListener('TournamentMatchWinner', this.handleTournamentMatchWinner);
    }
}
