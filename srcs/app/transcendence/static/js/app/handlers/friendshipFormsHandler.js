import AbstractHandler from "./abstractHandler.js";

export default class friendshipFormsHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }

    async updateUI(view, context) {
        //unbinding UI event handlers - NEED TO DO
        await view.loadComponents();
        //binding UI event handlers
        view.bindUIEventHandlers();
        const user_id = context.user_id;
        await view.loadUserDetail(user_id);
    }

    getContext(form, _response) {
        return {
            user_id: form[1].value
        }
    }
}
