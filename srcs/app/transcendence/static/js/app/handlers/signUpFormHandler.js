import AbstractHandler from "./abstractHandler.js";
import { navigateTo } from "../index.js";

export default class SignUpFormHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }

    async updateUI(view, context) {
        view.bindUIEventHandlers();
        if (context.ok)
            navigateTo("/sign_in/");
        else
            navigateTo("/sign_up/")
    }

    getContext(_form, response) {
        return response;
    }
}