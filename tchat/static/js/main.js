var messages = [];
var page = 1;
var emojisToggled = false;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function saveData(data) {
    // Add messages that are not already saved
    for (let i = 0; i < data.messages.length; i++) {
        let found = false;
        for (let j = 0; j < messages.length; j++) {
            if (messages[j].id === data.messages[i].id) {
                found = true;
                break;
            }
        }
        if (!found) {
            messages.push(data.messages[i]);
        }
    }
    // Sort by date
    messages.sort((a, b) => {
        return new Date(a['published']) - new Date(b['published']);
    });
    // Update HTML (DOM)
    updateHTML();
}

function updateHTML() {
    var items = [];
    $.each(messages, (_, message) => {
        items.push("<div class='balon" + (message['user']['me'] ? '1' : '2') + " p-2 m-0 position-relative' data-is='"
            + message['user']['username'] + " - "
            + new Date(message['published']).toLocaleString() + "'><span class='float-" + (message['user']['me'] ? 'end' : 'start') + "'>"
            + message['content'] + "</span></div>")
    });
    $("#channel-messages").html(items.join(""));
}

function loadNextPage(id) {
    // Get messages from JSON
    page++;
    $.ajax({
        url: "/channels/" + id + "/messages/" + page,
        type: "GET",
        success: function (data) {
            if (data.messages.length == 0) {
                $("#tchat-more").remove();
            }
            saveData(data);
        }
    });
}

function loadConversation(id) {
    // Get messages from JSON
    $.ajax({
        url: "/channels/" + id + "/messages/",
        type: "GET",
        success: function (data) {
            saveData(data);
        }
    });

    setTimeout(function () {
        loadConversation(id);
    }, 1000);
}

function sendMessage(id) {
    // Get message, and clear text
    let text = $("#message-text").val();
    $("#message-text").val("");

    // Send it to server
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: "/channels/" + id + "/messages/",
        type: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: {
            "content": text
        },
        success: function (data) {
            saveData(data);
        }
    });
}

function addUserToChannel(id) {
    // Get user
    let text = $("#user-select").val();

    // Send it to server
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: "/channels/" + id + "/users/",
        type: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: {
            "user": text
        },
        success: function (data) {
            location.reload();
        }
    });
}

function createChannel() {
    // Get channel name
    let name = $("#channel-name").val();

    // Send it to server
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: "/channels/",
        type: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: {
            "name": name
        },
        success: function (data) {
            location.reload();
        }
    });
}

function showEmojis() {
    emojisToggled = !emojisToggled;
    $("#emoji-keyboard").css('display', emojisToggled ? 'block' : 'none');
}

function insertEmoji(emo) {
    let text = $("#message-text").val();
    $("#message-text").val(text + emo);
}

function deleteUser(channel, user) {
    // Send it to server
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: "/channels/" + channel + "/users/" + user,
        type: "DELETE",
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (data) {
            location.reload();
        }
    });
}

function deleteMessage(id){
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: "/channels/" + id + "/messages/",
        type: "DELETE",
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (data) {
            location.reload();
        }
    });

}

function editMessage(id){
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: "/channels/" + id + "/messages/",
        type: "PUT",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: {
            "content": text
        },
        success: function (data) {
            saveData(data);
        }
    });

}


