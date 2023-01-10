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

function updateHTML(data) {
    // TODO: Update #channel-messages
    console.log(data.messages);
    var items = [];
    $.each(data.messages, (_, message) => {
        items.push("<div class='media.body'>" + message['content'] + " - envoyé par " + message['user']['username']
         + " le " + new Date(message['published']).toLocaleString() + "</div>")
    });
    $("#channel-messages").html(items.join(""));
}

function loadConversation(id) {
    // Get messages from JSON
    $.ajax({
        url: "/channels/" + id + "/messages/",
        type: "GET",
        success: function (data) {
            updateHTML(data);
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
            updateHTML(data);
        }
    });
}
