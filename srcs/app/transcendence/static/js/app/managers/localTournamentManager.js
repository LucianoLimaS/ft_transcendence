export default class LocalTournamentManager {
    constructor () {
        if (LocalTournamentManager.instance) {
            return LocalTournamentManager.instance;
        }

        this.status = 'Unstarted';
        LocalTournamentManager.instance = this;
    }

    startTournament(participants) {
        this.participants = participants;
        this.status = 'Started';
        this.createMatches();
    }

    resetTournament() {
        this.name = null;
        this.num_of_players = null;
        this.status = "Unstarted";
        this.participants = [];
        this.matches = [];
    }

    createMatches() {
        const totalPlayers = this.participants.length;
    
        if (![4, 8, 16, 32].includes(totalPlayers)) {
            throw new Error("Only tournaments with 4, 8, 16, or 32 players are supported.");
        }
    
        const totalMatches = totalPlayers - 1; // Total matches for a single-elimination tournament
        const rounds = Math.log2(totalPlayers); // Total rounds (log2 of total players)

        this.matches = [];
        let currentRoundMatches = []; // Matches in the current round
    
        // First round: Pair players sequentially
        for (let i = 0; i < totalPlayers; i += 2) {
            currentRoundMatches.push({
                matchId: `Match${this.matches.length + 1}`,
                [`Match${this.matches.length + 1}-p1`]: this.participants[i],
                [`Match${this.matches.length + 1}-p2`]: this.participants[i + 1],
                status: "ready",
                roomId: null,
                winner: null,
            });
            this.matches.push(currentRoundMatches[currentRoundMatches.length - 1]);
        }
    
        // Subsequent rounds
        for (let round = 2; round <= rounds; round++) {
            const nextRoundMatches = [];
            for (let i = 0; i < currentRoundMatches.length; i += 2) {
                nextRoundMatches.push({
                    matchId: `Match${this.matches.length + 1}`,
                    [`Match${this.matches.length + 1}-p1`]: null, // Placeholder for winner of currentRoundMatches[i]
                    [`Match${this.matches.length + 1}-p2`]: null, // Placeholder for winner of currentRoundMatches[i + 1]
                    status: "pending",
                    roomId: null,
                    winner: null,
                    dependsOn: [currentRoundMatches[i].matchId, currentRoundMatches[i + 1].matchId], // Tracks dependencies
                });
                this.matches.push(nextRoundMatches[nextRoundMatches.length - 1]);
            }
            currentRoundMatches = nextRoundMatches;
        }
    }

    updateMatchesOnWinner(matchId, winner) {
        // Find the match where the winner was defined
        const match = this.matches.find(m => m.matchId === matchId);
    
        if (!match) {
            return;
        }
    
        // Update the winner and status
        match.winner = winner;
        match.status = "Finished";
    
        // Update dependent matches
        this.matches.forEach(nextMatch => {
            if (nextMatch.dependsOn && nextMatch.dependsOn.includes(matchId)) {
                // Determine if the winner should be placed in player 1 or player 2
                const playerField = nextMatch[`Match${nextMatch.matchId.match(/\d+/)[0]}-p1`] === null
                    ? `${nextMatch.matchId}-p1`
                    : `${nextMatch.matchId}-p2`;
    
                nextMatch[playerField] = winner;
    
                // If both players are now defined, mark the match as ready
                if (nextMatch[`${nextMatch.matchId}-p1`] && nextMatch[`${nextMatch.matchId}-p2`]) {
                    nextMatch.status = "ready";
                }
            }
        });

        if (this.isFinalMatch(matchId)) {
            this.status = 'Finished';
            this.winner = winner;
        }
    }

    registerMatch(context) {
        const { room_id, match_id } = context;

        // Find the match with the given match_id
        const match = this.matches.find(m => m.matchId === match_id);

        if (!match) {
            return;
        }

        // Update the match with the room_id and mark it as ready
        match.roomId = room_id;

    }

    isFinalMatch(matchId) {
        // The final match is the last one in the matches array
        const finalMatch = this.matches[this.matches.length - 1];
        return finalMatch && finalMatch.matchId === matchId;
    }

    shuffleParticipants(participants) {
        for (let i = participants.length - 1; i > 0; i--) {
            const randomIndex = Math.floor(Math.random() * (i + 1));
            [participants[i], participants[randomIndex]] = [participants[randomIndex], participants[i]];
        }
        return participants;
    }
}