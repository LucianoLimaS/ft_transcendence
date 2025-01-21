import LocalTournamentManager from "../managers/localTournamentManager.js";
import PongRoomManager from "../managers/PongRoomManager.js";
import AbstractView from "./abstractView.js";

export default class LocalTournament extends AbstractView {
    constructor() {
        super();
        this.setTitle("Local Tournament");

        this.localTournamentManager = new LocalTournamentManager();

        this.handleStartFormSubmit = this.handleStartFormSubmit.bind(this);
        this.updateMatchesUI = this.updateMatchesUI.bind(this);
        this.updateUI = this.updateUI.bind(this);
        this.startGameBtnHandler = this.startGameBtnHandler.bind(this);
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
        document.getElementById("tourn-name").innerText = 'Name: ' + this.localTournamentManager.name;
        if (this.localTournamentManager.status == "Started" || this.localTournamentManager.status == "Finished")
            this.updateUI();
    }

    unloadComponents() {
    }

    bindUIEventHandlers() {
        document.getElementById("tournamentForm").addEventListener("submit", this.handleStartFormSubmit);
        
        this.bindLocalTournamentManagerEvents();
        this.bindButtonEventHandlers();
    }

    removeUIEventHandlers() {
    }

    updateUI() {
        if (this.localTournamentManager.status == "Started" || this.localTournamentManager.status == "Finished") {
            this.writePlayersNames();
            this.lockForm();
            this.deactivateStartButton();
            this.writeWinner();
        }
        this.updateMatchesUI();
    }

    writeWinner() {
        if (this.localTournamentManager.status != "Finished") {
            return;
        }

        document.getElementById('tourn-winner').innerText = "Winner: " + this.localTournamentManager.winner;
    }

    lockForm() {
        const form = document.getElementById("tournamentForm");
        if (!form) {
            return;
        }
    
        const inputs = form.querySelectorAll("input");
        inputs.forEach(input => {
            input.disabled = true; // Lock the input field
        });
    }

    writePlayersNames() {
        const form = document.getElementById("tournamentForm");
        if (!form) {
            return;
        }
    
        const inputs = form.querySelectorAll("input");
        this.localTournamentManager.participants.forEach((name, index) => {
            if (inputs[index]) {
                inputs[index].value = name; // Write the player's name into the input field
            }
        });
    }

    bindLocalTournamentManagerEvents() {
    }

    bindButtonEventHandlers() {
        document.getElementById("startGame").addEventListener("click", this.startGameBtnHandler);
    }

    startGameBtnHandler() {
        const startGameBtn = document.getElementById("startGame");
        startGameBtn.classList.add("d-none");
    }

    handleStartFormSubmit(event) {
        event.preventDefault();

        //Form Validations
        const form = event.target;
        const inputs = form.querySelectorAll("input");
        const playersNames = Array.from(inputs).map(input => input.value.trim());
        const warnElem = document.getElementById("p-warn");

        const duplicateInputIndexes = this.getDuplicateInputIndexes(playersNames);

        if (duplicateInputIndexes.length > 0) {
            this.clearDuplicateInputs(duplicateInputIndexes, inputs);
            warnElem.innerText = "Duplicate names not allowed";
            return;
        }

        this.cleanFormsWarnsErros(inputs, warnElem);

        this.startTournament(playersNames);
    }

    startTournament(playersNames) {
        this.localTournamentManager.startTournament(playersNames);

        this.deactivateStartButton();
        this.updateUI();
    }

    updateMatchesUI() {
        this.localTournamentManager.matches.forEach((match) => {
            const matchDiv = document.getElementById(match.matchId); // Get the match container by ID
            if (!matchDiv) {
                return;
            }

            // Update player 1 and player 2 names
            const player1Div = document.getElementById(`${match.matchId}-p1`);
            const player2Div = document.getElementById(`${match.matchId}-p2`);
            const statusText = document.getElementById(`status-${match.matchId}`);
            const matchBtn = document.getElementById(`btn-${match.matchId}`);

            if (player1Div) player1Div.textContent = match[`${match.matchId}-p1`] || "TBD";
            if (player2Div) player2Div.textContent = match[`${match.matchId}-p2`] || "TBD";

            if (match.status === "ready") {
                statusText.classList.add("d-none");
                matchBtn.classList.remove("d-none");
                matchBtn.disabled = false;
            } else if (match.status === "Finished" && match.winner) {
                statusText.textContent = `Winner: ${match.winner}`;
                statusText.classList.remove("d-none");
                matchBtn.classList.add("d-none");
                matchBtn.disabled = true;
            } else {
                statusText.textContent = "waiting for game...";
                statusText.classList.remove("d-none");
                matchBtn.classList.add("d-none");
                matchBtn.disabled = true;
            }
        });
    }

    deactivateStartButton() {
        const startButton = document.getElementById("startTournament");
        const startTournamentText = document.getElementById("startTournamentText");
        
        if (startButton) {
            startButton.style.display = "none"; // Esconde o botão
            startButton.disabled = true;
        }
        if (startTournamentText) {
            startTournamentText.classList.remove("d-none"); // Exibe o texto
        }
    }

    getDuplicateInputIndexes(names) {
        const seenNames = new Map(); // Tracks first occurrence index of each name
        const duplicateIndices = [];
    
        // Check for duplicates
        names.forEach((name, index) => {
            if (seenNames.has(name)) {
                duplicateIndices.push(index); // Add duplicate occurrence to list
            } else {
                seenNames.set(name, index); // Store the first occurrence
            }
        });

        return duplicateIndices;
    }

    clearDuplicateInputs(duplicateNameIndexes, inputs) {
        if (duplicateNameIndexes.length > 0) {
            duplicateNameIndexes.forEach(index => {
                inputs[index].value = ""; // Clear the input field
                inputs[index].classList.add("is-invalid"); // Highlight cleared field
            });
            return;
        }
    }

    cleanFormsWarnsErros(inputs, warnElem) {
        warnElem.innerText = "";
        inputs.forEach(input => {
            input.classList.remove("is-invalid");
        });
    }
}
