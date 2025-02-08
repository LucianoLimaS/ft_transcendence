import { PongGame } from "./PongGame.js";


//Get canvas and context
const canvas = document.getElementById("pongCanvas");
const context = canvas.getContext("2d");

//Initialize game
const pongGame = new PongGame(context, canvas.width, canvas.height);

//Get game data
const gameData = document.getElementById("game-data");
const roomId = gameData.dataset.roomId;
const gameMode = gameData.dataset.gameMode;


//Websocket connection
let socketUrl;

if (gameMode === "tournament") {
  socketUrl = `wss://${window.location.host}/ws/pong/tournament_match/${roomId}/`;
} else {
  socketUrl = `wss://${window.location.host}/ws/pong/${gameMode}/`;
}

const socket = new WebSocket(socketUrl);

//Websocket
socket.onopen = (event) => {
  handleSocketOpen(event);
};

socket.onmessage = (event) => {
  handleSocketMessage(event);
};

socket.onclose = (event) => {
};

socket.onerror = (event) => {
};

//Event listeners - Start game button
const startButton = document.getElementById("startGame");
startButton.addEventListener("click", () => {
  handleClickStartButton();
});

//Event listeners - Keys
document.addEventListener("keydown", (event) => {
  handleKeyEvent(event, "keydown");
});

document.addEventListener("keyup", (event) => {
  handleKeyEvent(event, "keyup");
});

//Functions
function handleSocketOpen(event) {
  const message = {
    type: "join_room",
    room_id: roomId,
    width: canvas.width,
    height: canvas.height,
  };
  sendMessage(message);
}

function handleSocketMessage(event) {
  const data = JSON.parse(event.data);

  switch (data.type) {
    case "not_auth":
      alert(data.message);
      socket.close();
      break;

    case "game_init":
      pongGame.drawGameState(data.game_state);
      break;

    case "update_game_state":
      pongGame.drawGameState(data.game_state);
      break;

    case "game_has_started":
      handleGameHasStarted();
      break;

    case "winner":
      handleWinner(data.winner);
      break;

    case "redirect_tournament":
      handleRedirectTournament(data.redirect);
      break

    default:
  }
}

function handleClickStartButton() {
  const message = {
    type: "start_game",
  };
  sendMessage(message);
}

function handleKeyEvent(event, keyType) {
  const validKeys = ["ArrowUp", "ArrowDown", "w", "s", "W", "S"];
  if (validKeys.includes(event.key)) {
    event.preventDefault();
    const message = {
      type: keyType,
      key: event.key.toLocaleLowerCase(),
    };
    sendMessage(message);
  }
}

function handleGameHasStarted() {
  startButton.style.display = "none";
  const messageContainer = document.getElementById("messageContainer");
  messageContainer.textContent = "Game has started!";
}

function handleWinner(winner) {
  const messageContainer = document.getElementById("messageContainer");
  messageContainer.textContent = `${winner} wins!`;
  startButton.textContent = "Play Again!";
  startButton.style.display = "block";
}

function handleRedirectTournament(redirect) {
  window.location.href = redirect; //navigateTo
}

function sendMessage(message) {
  const jsonMessage = JSON.stringify(message);
  socket.send(jsonMessage);
}
