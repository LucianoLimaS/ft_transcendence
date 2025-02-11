import AbstractHandler from "./abstractHandler.js";
import { navigateTo } from "../index.js";

export default class CreateTournamentHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }


    async postForm(form) {
        const formData = new FormData(form);

        const submitButton = form.querySelector('button[type="submit"]:focus');
        const maxPlayers = submitButton ? submitButton.value : null;


        if (maxPlayers) {
            formData.append('max_players', maxPlayers); // Adiciona ao FormData
        } else {
        }

        return fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                },
            })
            .then(response => {
                if (response.ok) {
                    return response;
                } else {
                    return response;
                }
            })
            .catch(error => {
                throw error;
            }
            );
    }


    async updateUI(view, context) {
        view.bindUIEventHandlers();
        if (context.ok)
            navigateTo("/enter/tournament/");
    }

    getContext(_form, response) {
        return response;
    }
}