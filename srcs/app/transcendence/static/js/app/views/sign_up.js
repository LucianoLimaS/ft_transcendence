import AbstractView from "./abstractView.js";

export default class Sign_up extends AbstractView {
    constructor() {
        super();
        this.setTitle("Sign_up");
    }

    async getHtml() {
        try {
            const response = await fetch('/sign_up/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            return html;
        }
        catch(error) {
            return "<p>Error loading register page</p>";
        }
    }
}
