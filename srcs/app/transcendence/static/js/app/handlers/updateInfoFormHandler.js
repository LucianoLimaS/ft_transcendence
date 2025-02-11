import AbstractHandler from "./abstractHandler.js";
import { navigateTo } from "../index.js";

export default class UpdateInfoFormsHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }

    async postForm(form) {
        const formData = new FormData(form);

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
            navigateTo("/profile/");
        else
            navigateTo("/update_info/");
    }

    getContext(_form, response) {
        return response;
    }
}