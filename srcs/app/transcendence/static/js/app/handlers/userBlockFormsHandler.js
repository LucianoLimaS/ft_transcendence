import AbstractHandler from "./abstractHandler.js";

export default class userBlockFormsHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }

    async updateUI(view, context) {
        const user_id = context.user_id
        await view.loadUserDetail(user_id);
    }

    getContext(form, _response) {
        return {
            user_id: form[1].value
        }
    }
}
