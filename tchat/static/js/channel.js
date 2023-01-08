function loadConversation(id) {
    // TODO: Appeler /channels/{id}/messages/ pour charger les messages
    // et les charger dans #channel-messages
    console.log("loadConversation: " + id);
}

function sendMessage() {
    // Get message, and clear text
    let text = $("#message-text").val();
    $("#message-text").val("");

    // Send it to server (TODO)
    console.log("sendMessage: " + text);
}
