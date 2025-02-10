import AbstractHandler from "./abstractHandler.js";
import { navigateTo } from "../index.js";

export default class ChangePasswordFormsHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }

    async updateUI(view, context) {
        view.bindUIEventHandlers();
        if (context.ok)
            navigateTo("/profile/");
        else
            navigateTo("/change_password/");
    }

    getContext(form, response) {
        return response;
    }
}
