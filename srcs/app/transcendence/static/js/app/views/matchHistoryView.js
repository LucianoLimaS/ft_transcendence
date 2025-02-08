import AbstractView from "./abstractView.js";

export default class MatchHistoryView extends AbstractView {
    constructor() {
        super();
        this.setTitle("Match History");
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            return html;
        }
        catch(error) {
            return "<p>Error loading login page</p>";
        }
    }

    bindUIEventHandlers() {
    }

    removeUIEventHandlers() {
    }
}
