export default class AbstractView{
    constructor() {
        if (this.constructor === AbstractView) {
            throw new Error("AbstractView is an abstract class and cannot be instantiated directly.");
        }

        if (typeof this.bindUIEventHandlers !== "function") {
            throw new Error(`${this.constructor.name} must implement bindUIEventHandlers.`);
        }

        if (typeof this.removeUIEventHandlers !== "function") {
            throw new Error(`${this.constructor.name} must implement removeUIEventHandlers.`);
        }
    }

    setTitle(title) {
        document.title = title;
    }

    async getHtml() {
        return "";
    }

    loadComponents() {
    }

    unloadComponents() {
    }

    bindUIEventHandlers() {
    }

    removeUIEventHandlers() {
    }
}