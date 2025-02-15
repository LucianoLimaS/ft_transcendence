export default class AbstractHandler {
    constructor() {
        if (this.constructor === AbstractHandler) {
            throw new Error("AbstractHandler is an abstract class and cannot be instantiated directly.");
        }
    }

    async postForm(form) {
        const formData = new FormData(form);
        const data = new URLSearchParams(formData);

        return fetch(form.action, {
            method: form.method,
            body: data,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded",
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

    async updateUI(_view, _context) { }

    getContext() { }
}
