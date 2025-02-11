import AbstractView from "./abstractView.js";
/* import ChatManager from "../managers/ChatManager.js"; */

export default class Profile extends AbstractView {
    constructor() {
        super();
        this.setTitle("Profile");
        // tenta conectar o socket de chat
        /* const chatManager = new ChatManager();
        chatManager.tryConnectToChatSocket(); */

        this.handleFriendClick = this.handleFriendClick.bind(this);
        this.updateFriend = this.updateFriend.bind(this);
        this.handleTabSwitch = this.handleTabSwitch.bind(this);
        this.handleSearchEnterKey = this.handleSearchEnterKey.bind(this);
        this.handleUserSearch = this.handleUserSearch.bind(this);
        this.loadComponents = this.loadComponents.bind(this);
    }

    async getHtml() {
        try {
            const response = await fetch('/friends/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            return html;
        }
        catch (error) {
            return "<p>Error loading login page</p>";
        }
    }

    async loadComponents() {
        await this.loadFriendsList();
    }

    async getUserDetailHtml(user_id) {
        try {
            const response = await fetch('/user/' + user_id + '/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            return html;
        }
        catch (error) {
            return "<p>Error loading login page</p>";
        }
    }

    async loadUserDetail(user_id) {
        var detailHtml = await this.getUserDetailHtml(user_id);

        var picDiv = document.getElementById('profile-pic');
        var statsDiv = document.getElementById('profile-stats');

        if (picDiv) picDiv.remove();
        if (statsDiv) statsDiv.remove();

        var friendsPageDiv = document.getElementById('friends-page');
        friendsPageDiv.insertAdjacentHTML('beforeend', detailHtml);

    }

    async loadFriendsList() {
        const friendsBox = document.getElementById('friends-tab');
        // Clear any existing content
        friendsBox.innerHTML = '';

        let jsonData = {};
        try {
            const response = await fetch('/api/user/friends/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            jsonData = await response.json();
        }
        catch (error) {
        }

        if (jsonData.friends && jsonData.friends.length > 0) {
            jsonData.friends.forEach(friend => {
                // Create the friend container div
                const friendDiv = document.createElement('div');
                friendDiv.className = 'friend d-flex flex-row align-items-center justify-content-between gap-2 px-2 py-1 mb-1 me-1 rounded-5';

                // Create the inner left content (status icon + name)
                const leftContentDiv = document.createElement('div');
                leftContentDiv.className = 'd-flex flex-row align-items-center gap-3';

                const statusIconDiv = document.createElement('div');
                statusIconDiv.className = 'status-icon';

                //const imgElement = document.createElement('img');
                //imgElement.className = 'friend-img rounded-circle border-0';
                //imgElement.src = '/static/assets/foto-perfil.png';
                //statusIconDiv.appendChild(imgElement);
                //
                // Ícone de acordo com o status online da pessoa
                const iconElement = document.createElement('i');
                iconElement.className = 'bi bi-circle-fill'; // Classe para o ícone
                // Adicionando a cor com base em is_online
                friend.is_online ? iconElement.style.color = 'green' : iconElement.style.color = 'red';
                // Adicionando o ícone ao contêiner
                statusIconDiv.appendChild(iconElement);
                const friendNameP = document.createElement('p');
                friendNameP.className = 'friend-name m-0 mt-1';
                friendNameP.dataset.friend = friend.id; //desnecessario??
                friendNameP.textContent = friend.username;
                leftContentDiv.appendChild(statusIconDiv);
                leftContentDiv.appendChild(friendNameP);
                // Create the info icon
                const infoIcon = document.createElement('i');
                infoIcon.className = 'info-icon mt-1 bi bi-info-circle';
                // Assemble the friend container
                friendDiv.appendChild(leftContentDiv);
                friendDiv.appendChild(infoIcon);
                // Append the friend div to the friends box
                friendsBox.appendChild(friendDiv);
            });
        } else {
            const noFriendsMessage = document.createElement('p');
            noFriendsMessage.className = 'no-friend-msg my-4 text-nowrap d-flex justify-content-center';
            noFriendsMessage.textContent = 'You have no friends!';
            friendsBox.appendChild(noFriendsMessage);
        }
    }

    async loadUsersList() {
        let usersData = {};
        try {
            const response = await fetch('/api/user/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            usersData = await response.json();
        }
        catch (error) {
        }
        const friendsBox = document.getElementById('search-tab');

        // Clear existing content in the friends box
        friendsBox.innerHTML = '';

        // Separate pending friend requests and all users
        const pendingRequests = usersData.users.filter(user => user.pending_friend_request);
        const allUsers = usersData.users;

        // Generate HTML for pending friend requests if any
        const pendingHeader = `
            <div style="display: flex; align-items: center; gap: 5px;">
                <hr style="flex-grow: 1; border: none; border-top: 1px solid #333; margin: 0;">
                <p class="text-profile m-0 px-1 text-center" style="font-size: 11px; font-weight: 300; margin: 0; color: #333">Pending requests</p>
            </div>
        `;
        friendsBox.insertAdjacentHTML('beforeend', pendingHeader);
        if (pendingRequests.length > 0) {

            pendingRequests.forEach(request => {
                const requestHtml = `
                    <div class="friend d-flex flex-row align-items-center justify-content-between gap-2 ps-2 py-1 mb-1 me-1 rounded-5">
                        <div class="d-flex flex-row align-items-center gap-3">
                            <div class="status-icon">
                            </div>
                            <p class="friend-name m-0 mt-1" data-friend="${request.id}">
                                ${request.username}
                            </p>
                        </div>
                    </div>
                `;
                friendsBox.insertAdjacentHTML('beforeend', requestHtml);
            });
        } else {
            const noPendingRequests = `
                <p class="no-friend-msg my-2 text-nowrap d-flex justify-content-center">No pending request ...</p>
            `;
            friendsBox.insertAdjacentHTML('beforeend', noPendingRequests);
        }

        // Generate HTML for all users
        if (allUsers.length > 0) {
            const usersHeader = `
                <div style="display: flex; align-items: center; gap: 5px;">
                    <hr style="flex-grow: 1; border: none; border-top: 1px solid #333; margin: 0;">
                    <p class="text-profile m-0 px-1 text-center" style="font-size: 11px; font-weight: 300; margin: 0; color: #333">All Users</p>
                </div>
            `;
            friendsBox.insertAdjacentHTML('beforeend', usersHeader);

            allUsers.forEach(user => {
                const userHtml = `
                    <div class="friend d-flex flex-row align-items-center justify-content-between gap-2 ps-2 py-1 mb-1 me-1 rounded-5">
                        <div class="d-flex flex-row align-items-center gap-3">
                            <div class="status-icon">
                            </div>
                            <p class="friend-name m-0 mt-1" data-friend="${user.id}">
                                ${user.username}
                            </p>
                        </div>
                    </div>
                `;
                friendsBox.insertAdjacentHTML('beforeend', userHtml);
            });
        } else {
            const noUsers = `
                <p class="text-profile m-0 text-center" style="font-size: 14px; font-weight: 400;">No other user. What a shit game site.</p>
            `;
            friendsBox.insertAdjacentHTML('beforeend', noUsers);
        }
    }

    bindUIEventHandlers() {

        this.bindFriendListClickEvent();

        //add click event for switch tabs between friends and search
        const titleFriends = document.querySelector("#title-friends-friend");
        const titleSearch = document.querySelector("#title-friends-search");
        titleFriends.addEventListener("click", this.handleTabSwitch);
        titleSearch.addEventListener("click", this.handleTabSwitch);

        //search events
        const searchBarInput = document.getElementById('search-input');
        searchBarInput.addEventListener('keydown', this.handleSearchEnterKey);
        const friendsBarInput = document.getElementById('friends-input');
        friendsBarInput.addEventListener('keydown', this.handleSearchEnterKey);
    }

    removeUIEventHandlers() {

        const friendsBox = document.querySelector(".friends-box");
        friendsBox.removeEventListener("click", this.handleFriendClick);

        const titleFriends = document.querySelector("#title-friends-friend");
        const titleSearch = document.querySelector("#title-friends-search");
        titleFriends.removeEventListener("click", this.handleTabSwitch);
        titleSearch.removeEventListener("click", this.handleTabSwitch);
    }

    bindFriendListClickEvent() {
        const friendElements = document.querySelectorAll('[data-friend]');

        friendElements.forEach(friendElement => {
            friendElement.addEventListener('click', this.handleFriendClick);
        });
    }

    handleFriendClick(event) {

        const friendElement = event.target.closest("[data-friend]");
        if (!friendElement) {
            return;
        }

        this.unhighlightPreviousFriend();
        const friendId = friendElement.dataset.friend;
        if (!friendId) {
            return;
        }
        this.highlightSelectedFriend(friendElement);
        const friendsColumn = document.querySelector('.col-friends.friends');
        friendsColumn.classList.remove('unselected');
        const friendsBoxes = document.querySelectorAll('.friends-box.friends');
        friendsBoxes.forEach(box => {
            box.classList.remove('unselected');
        });
        this.loadUserDetail(friendId);
    }

    handleTabSwitch(event) {
        const tab = event.target.textContent.trim().toLowerCase();
        this.toggleTabs(tab);
    }

    handleSearchEnterKey(event, tab) {
        if (event.key === 'Enter') {
            if (event.currentTarget.id === 'friends-input') {
                this.handleFriendsSearch();
            } else {
                this.handleUserSearch();
            }
        }
    }

    handleFriendsSearch() {
        const messageInputDom = document.getElementById('friends-input');
        if (!messageInputDom) {
            return;
        }
        const message = messageInputDom.value;
        if (!message) {
            return;
        }
        messageInputDom.value = '';
        this.renderFriendsList(this.getFriendsList());
    }

    handleUserSearch() {
        const messageInputDom = document.getElementById('search-input');
        if (!messageInputDom) {
            return;
        }
        const message = messageInputDom.value;
        if (!message) {
            return;
        }
        messageInputDom.value = '';
        this.renderUserSearch(this.searchUsers());
    }

    getFriendsList() {
        //endpoint to get friends list
        var friends = [];
        return friends;
    }

    searchUsers() {
        //endpoint to get search results
        var users = [];
        return users;
    }

    renderFriendsList(friends) {
        //render friends list based on friends array
    }

    renderUserSearch(users) {
        //render search results based on results array
    }


    updateFriend(friendElement) {

    }

    async toggleTabs(tab) {
        const divFriend = document.querySelector('.div-friend');
        const divSearch = document.querySelector('.div-search');
        const titleFriends = document.querySelector("#title-friends-friend");
        const titleSearch = document.querySelector("#title-friends-search");

        if (tab === 'friends') {
            divFriend.style.display = 'block';
            divSearch.style.display = 'none';
            titleSearch.classList.remove('selected');
            titleFriends.classList.add('selected');

            this.unhighlightPreviousFriend();

            await this.loadFriendsList();
        } else if (tab === 'search') {
            divFriend.style.display = 'none';
            divSearch.style.display = 'block';
            titleFriends.classList.remove('selected');
            titleSearch.classList.add('selected');

            this.unhighlightPreviousFriend();
            await this.loadUsersList();
        }
        this.bindFriendListClickEvent();
    }

    highlightSelectedFriend(eventTarget) {
        const outerDiv = eventTarget.closest('.friend');
        if (outerDiv)
            outerDiv.classList.add('selected');
    }

    unhighlightPreviousFriend() {
        const selectedFriend = document.querySelector('.friend.selected');
        if (selectedFriend) {
            selectedFriend.classList.remove('selected');
        }
    }
}
