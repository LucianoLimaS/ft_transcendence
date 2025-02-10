import AbstractHandler from "./abstractHandler.js";
import { navigateTo } from "../index.js";

export default class SignInFormHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }

    async updateUI(view, context) {
        view.bindUIEventHandlers();
        if (context.ok)
            navigateTo("/");
        else
            navigateTo("/sign_in/")
    }

    getContext(_form, response) {
        return response;
    }
}