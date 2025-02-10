

const gameData = document.getElementById("game-data");
const username = gameData.dataset.username;
const tournamentId = gameData.dataset.tournamentId;
const gameMode = gameData.dataset.gameMode;


if (gameMode !== "tournament") {
}

//Websocket connection
const protocol = window.location.protocol === "https:" ? "wss" : "ws";
const socketUrl = `${protocol}://${window.location.host}/ws/pong/tournament/${tournamentId}/`;
const socket = new WebSocket(socketUrl);

//Websocket
socket.onopen = (event) => {
};

socket.onmessage = (event) => {
  handleSocketMessage(event);
};

socket.onclose = (event) => {
};

socket.onerror = (event) => {
};

//Event listerners - Join tournament button
const joinButton = document.getElementById("joinTournament");
joinButton.addEventListener("click", () => {
  handleClickJoinButton();
});

const playButtons = document.querySelectorAll('button[id*="Quarter"][id*="-btn"], button[id*="Semi"][id*="-btn"], button[id="Final-btn"]');
playButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    e.preventDefault(); // Impede o comportamento padrão
    const round = button.id.split('-')[0]; // Pega o nome da rodada (Quarter, Semi ou Final)
    const roomId = button.id.split('-')[0].replace(/Quarter|Semi/, ''); // Remove 'Quarter' ou 'Semi' e deixa apenas o índice
    redirectToMatch(roomId);
  });
});

//Functions
function handleSocketMessage(event) {
  const data = JSON.parse(event.data);

  switch (data.type) {
    case "not_auth":
      alert(data.message);
      socket.close();
      break;

    case "joined":
      joinButton.classList.add("disabled");
      joinButton.disabled = true;
      break;

    case "current_state":
      handleCurrentState(data);
      break;

    case "tournament_message":
      handleTournamentMessage(data);
      break;

    case "tournament_advance":
      handleTournamentAdvance(data);
      break;

    case "error":
      handleErrorMessage(data);
      break;

    default:
  }
}

function handleCurrentState(data) {
  updateTournamentUI(data.state);
}

function handleTournamentMessage(data) {
  displayTournamentMessage(data.message);
}

function handleTournamentAdvance(data) {
  updateTournamentUI(data.state);
}

function handleErrorMessage(data) {
  displayErrorMessage(data.message);
}

function handleClickJoinButton() {
  sendMessage({
    type: "join_tournament"
  });
}

function sendMessage(message) {
  const jsonMessage = JSON.stringify(message);
  socket.send(jsonMessage);
}

function updateTournamentUI(state) {
  // Update participant slots
  state.participants.forEach((participant, index) => {
    const participantElem = document.getElementById(`participant-${index}`);
    if (participantElem) {
      participantElem.innerText = participant || `Player ${index + 1}`;
    }
  });

  // Update match brackets
  state.matches.forEach((match) => {
    const player1Elem = document.getElementById(`${match.round}-p1`);
    const player2Elem = document.getElementById(`${match.round}-p2`);
    const buttonElem = document.getElementById(`${match.round}-btn`);

    if (player1Elem)
      player1Elem.innerText = match.player1 !== "TBD" ? match.player1 : "TBD";
    if (player2Elem)
      player2Elem.innerText = match.player2 !== "TBD" ? match.player2 : "TBD";

    if (buttonElem) {
      if (
        (match.player1 === username || match.player2 === username) &&
        !match.finished &&
        match.player1 !== "TBD" &&
        match.player2 !== "TBD"
      ) {
        buttonElem.style.display = "block";
        buttonElem.onclick = () => redirectToMatch(match.room_id);
      } else {
        buttonElem.classList.add("disabled");
      }
    }
  });
}

// Função para redirecionar para a partida
function redirectToMatch(roomId) {
  window.location.href = `/room/${roomId}/`;
}

//function to display tournament message
function displayTournamentMessage(message) {
  const tournamentStatusMsg = document.getElementById("tournamentMessages");
  if (tournamentStatusMsg) {
    tournamentStatusMsg.innerText = message;
  }
}

//function to display error message
function displayErrorMessage(message) {
  const tournamentErrorMsg = document.getElementById("tournamentErrorMsg");
  if (tournamentErrorMsg) {
    tournamentErrorMsg.innerText = message;
  }
}
