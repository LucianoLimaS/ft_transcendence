import AbstractHandler from "./abstractHandler.js";
import { navigateTo } from "../index.js";
import LocalTournamentManager from "../managers/localTournamentManager.js";

export default class localTournamentMatchFormsHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }

    async postForm(form) {
        const formData = new FormData(form);
        const data = new URLSearchParams(formData);

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: data,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            });

            if (!response.ok) {
                throw new Error(response.statusText);
            }

            const jsonData = await response.json();
            return jsonData;

        } catch (error) {
            throw error; // Rethrow the error for the caller to handle
        }
    }

    async updateUI(view, context) {
        const localTournamentManager = new LocalTournamentManager();
        localTournamentManager.registerMatch(context)
        navigateTo(`/localTournament/room/${context.room_id}/`);
    }

    getContext(form, response) {
        const context = {
            room_id : response.room_id,
            match_id : form.getAttribute('match-id')
        };
        return context;
    }
}
