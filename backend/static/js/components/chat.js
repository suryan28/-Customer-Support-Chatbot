/**
 * scroll to the bottom of the chats after new message has been added to chat
 */
const converter = new showdown.Converter();

function scrollToBottomOfResults() {
    const terminalResultsDiv = document.getElementById("chats");
    terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
}

/**
 * Set user response on the chat screen
 * @param {String} message user message
 */
function setUserResponse(message) {
    const user_response = `<img class="userAvatar" src='./static/img/userAvatar.jpg'><p class="userMsg">${message} </p><div class="clearfix"></div>`;
    $(user_response).appendTo(".chats").show("slow");

    $(".usrInput").val("");
    scrollToBottomOfResults();
    showBotTyping();
    $(".suggestions").remove();
}

/**
 * returns formatted bot response
 * @param {String} text bot message response's text
 */
function getBotResponse(text) {
    botResponse = `<img class="botAvatar" src="./static/img/botAvatar_old.png"/><span class="botMsg">${text}</span><div class="clearfix"></div>`;
    return botResponse;
}

function setBotResponse(response) {
    // renders bot response after 500 milliseconds
    setTimeout(() => {
        hideBotTyping();
        if (response.length < 1) {
            // if there is no response from server, send  fallback message to the user
            const fallbackMsg = "I am facing some issues, please try again later!!!";

            const BotResponse = `<img class="botAvatar" src="./static/img/botAvatar_old.png"/><p class="botMsg">${fallbackMsg}</p><div class="clearfix"></div>`;
            $(BotResponse).appendTo(".chats").hide().fadeIn(1000);
            scrollToBottomOfResults();
        } else {
            // if we get response from server
            for (let i = 0; i < response.length; i += 1) {
                // check if the response contains "text"
                if (Object.hasOwnProperty.call(response[i], "text")) {
                    if (response[i].text != null) {
                        // convert the text to markdown format using showdown.js(https://github.com/showdownjs/showdown);
                        let botResponse;
                        let html = converter.makeHtml(response[i].text);
                        html = html
                            .replaceAll("<p>", "")
                            .replaceAll("</p>", "")
                            .replaceAll("<strong>", "<b>")
                            .replaceAll("</strong>", "</b>");
                        html = html.replace(/(?:\r\n|\r|\n)/g, "<br>");
                        // check for blockquote
                        if (html.includes("<blockquote>")) {
                            html = html.replaceAll("<br>", "");
                            botResponse = getBotResponse(html);
                        }
                        // check for image
                        if (html.includes("<img")) {
                            html = html.replaceAll("<img", '<img class="imgcard_mrkdwn" ');
                            botResponse = getBotResponse(html);
                        }
                        // check for preformatted text
                        if (html.includes("<pre") || html.includes("<code>")) {
                            botResponse = getBotResponse(html);
                        }
                        // check for list text
                        if (
                            html.includes("<ul") ||
                            html.includes("<ol") ||
                            html.includes("<li") ||
                            html.includes("<h3")
                        ) {
                            html = html.replaceAll("<br>", "");
                            botResponse = getBotResponse(html);
                        } else {
                            // if no markdown formatting found, render the text as it is.
                            if (!botResponse) {
                                botResponse = `<img class="botAvatar" src="./static/img/botAvatar_old.png"/><p class="botMsg">${response[i].text}</p><div class="clearfix"></div>`;
                            }
                        }
                        // append the bot response on to the chat screen
                        $(botResponse).appendTo(".chats").hide().fadeIn(1000);
                    }
                }

                // check if the response contains "buttons"
                if (Object.hasOwnProperty.call(response[i], "buttons")) {
                    if (response[i].buttons.length > 0) {
                        addSuggestion(response[i].buttons);
                    }
                }

                // check if the response contains "custom" message
                if (Object.hasOwnProperty.call(response[i], "custom")) {
                    const {payload} = response[i].custom;
                    if (payload === "quickReplies") {
                        // check if the custom payload type is "quickReplies"
                        const quickRepliesData = response[i].custom.data;
                        showQuickReplies(quickRepliesData);
                        return;
                    }
                }
            }
            scrollToBottomOfResults();
        }
        $(".usrInput").focus();
    }, 500);
}

var dataObj = {};
var isTicketGenerated = false;
var userType = ''
function send(message) {
    // if(message === "../#restart"){
    //      restartConversation();
    // }else{
    if (a_ticket && message !== "../#ticket") {
        handleTicketMessage(message);
    } else if (isTicketGenerated) {
        count = 2;
        handleSpecificMessages(message, true);
        return;
    } 
    else {
        handleSpecificMessages(message);
    }}
// }

function isEmailValid(email) {
    // Regular expression for a simple email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Test the provided email against the regex
    return emailRegex.test(email);
}

function generate_ticket(requestData) {
    // requestParams = {description: requestData.description, email: requestData.email, cf:{cf_user_name: username, cf_user_type: requestData.category, cf_user_sport_interest: requestData.subCategory}}
    fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
    })
        .then((response) => response.json())
        .then((data) => {
            setBotResponse(data);
            isTicketGenerated = true;
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function handleTicketMessage(message) {
    if (!isEmailValid(message)) {
        dataObj.description = message;
    }

    if (a_ticket && isEmailValid(message)) {
        dataObj.email = message;
        a_ticket = false;
        generate_ticket(dataObj);
    } else {
        a_ticket = true;
        setBotResponse([{text: "Please enter your email for us to respond. 📧👩‍💻"}]);
    }
}

function handleSpecificMessages(message, isRepeating = false) {
    if (isRepeating && count == 2) {
        usertype = userType;
        dataObj = {};
        count = 3;
    }
    if (count == 0) {
        setTimeout(sendAPI(message, "username"), 2000);
    } else if (message == "../#ticket") {
        $("#userInput").prop("disabled", false);
        a_ticket = true;
        setBotResponse([
            {
                text: "Please provide detailed specifics about your question(s) so we can best answer them! 📝🤔",
            },
        ]);
    } else if (message == "../#y") {
        setBotResponse([{ text: "Thank you, and have a great rest of your day! 😊🌟" }, { text: "Keep Asking !!!😊🤗" }]);
        isTicketGenerated = true;
        $("#userInput").prop("disabled", false);
    } else if (message == "../#n") {
        setBotResponse(open_ticket);
        $("#userInput").prop("disabled", false);
    } else if (message == "../#nt") {
        setBotResponse([{ text: message_for_tryout }]);
    } else if (message == "../#yt") {
        setBotResponse(open_ticket_tryout);
    } else if (count == 1) {
        setTimeout(sendAPI(message, "sports"), 2000);
    } else if (count == 2) {
        setTimeout(sendAPI(message, "usertype"), 2000);
        isTicketGenerated = false;
    } else {
        setTimeout(sendAPI(message, usertype), 2000);
    }
}

function sendAPI(message, flag) {
    // setTimeout(r, 2000);
    $.ajax({
        url: server_url,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ text: message, flag: flag }),
        success(botResponse, status) {
            // return botResponse;
            if (botResponse[0] == null){
                setBotResponse("");
                return;
            }
            if (hasValueForKey(botResponse, "category", "tryouts")){
             new_object =  placeObjectInTryoutsCategory(botResponse);
            setBotResponseForUsername(new_object);
            }
            else{
            setBotResponseForUsername(botResponse);
        }},
        error(xhr, textStatus) {
            // if there is no response from server, set error bot response
            setBotResponse("");
        },
    });
}

function setDefaultValues() {
    previousResponse = null;
    count = 0;
    username = "";
    usertype = "";
    usersports = "";
    a_ticket = false;
    // is_run = false;
}

function setBotResponseForUsername(botResponse) {
    if (botResponse[0].isvalid == "False" || botResponse[0].isvalid == false) {
        // If current response is not valid, use the previous response
        if (previousResponse) {
            setBotResponse([previousResponse[0]]);
        } else {
            setBotResponse([{ text: "Hello and welcome to our customer support chat. 👋 May I start by asking your name? 🤔💬" }]);
        }
    } else {
        if(botResponse[0].category != 'Other'){
        satisfied_count = 0;
        }
        if(satisfied_count !=1){
            setBotResponse(botResponse);
        }
        previousResponse = botResponse; // Store the current response
        if (count == 0) {
            setUserName(botResponse);
        } else if (count == 1) {
            dataObj.subCategory = botResponse[0]['sports']
            setUserSport(botResponse);
        } else if (count == 2) {
            setUserType(botResponse);
            userType = botResponse[0]['usertype'];
            dataObj.category = botResponse[0]['usertype'];
        } else {
            if (hasValueForKey(botResponse, 'category', 'tryouts')) {
                window.open(url, '_blank');
                setBotResponse(open_tryout);
            } else {
                if (count >= 3) {
                    if(botResponse[0].category == 'Other'){
                        if(satisfied_count == 1){
                            // $("#userInput").prop("disabled", true);
                            setTicketMsg();
                        }
                        // satisfied_count += 1;
                        satisfied_count = satisfied_count === 0 ? 1 : 0;
                    }
                    else{
                        setSatisfiedMsg();
                        setUserType(botResponse);
                    }
                }
            }
        }
        count += 1;
    }
}

function setTicketMsg(){
    setBotResponse(not_satisfied_ticket);
}
function setSatisfiedMsg() {
    setBotResponse(satisfied_response);
    $("#userInput").prop("disabled", true);
}

function setUserType(response) {
    usertype = response[0].usertype == undefined ? response[0].category : response[0].usertype;
}

function setUserName(response) {
    username = response[0].username;
}

function setUserSport(response) {
    usersports = response[0].sports;
}

function placeObjectInTryoutsCategory(arr) {
    let tryoutsIndex = -1;
    for (let i = 0; i < arr.length; i++) {
        if (arr[i].category === "tryouts") {
            tryoutsIndex = i;
            break;
        }
    }
    if (tryoutsIndex !== -1) {
        const tryoutsObj = arr.splice(tryoutsIndex, 1)[0]; // Remove tryouts object from array
        arr.push(tryoutsObj); // Push tryouts object to the end of array
    }
    return arr;
}

function hasValueForKey(arr, key, value) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i][key] === value) {
            return true; // Key value matches the desired value
        }
    }
    return false; // Key value doesn't match the desired value in any object
}

/**
 * clears the conversation from the chat screen
 * & sends the `/restart` event to the server
 */
function restartConversation() {
    $("#userInput").prop("disabled", false);
    $(".chats").html("");
    $(".usrInput").val("");
    setBotResponse([{text: "Hello and welcome to our customer support chat. 👋 May I start by asking your name? 🤔💬"}]);
    isTicketGenerated = false;
    setDefaultValues();
}

// triggers restartConversation function.
$("#restart").click(() => {
    restartConversation();
});

/**
 * if user hits enter or send button
 * */
$(".usrInput").on("keyup keypress", (e) => {
    const keyCode = e.keyCode || e.which;

    const text = $(".usrInput").val();
    if (keyCode === 13) {
        if (text === "" || $.trim(text) === "") {
            e.preventDefault();
            return false;
        }
        $(".dropDownMsg").remove();
        $(".suggestions").remove();
        $(".quickReplies").remove();
        $(".usrInput").blur();
        setUserResponse(text);
        // var flag = $("#hiddenFlag").val();
        send(text);
        e.preventDefault();
        return false;
    }
    return true;
});

$("#sendButton").on("click", (e) => {
    const text = $(".usrInput").val();
    if (text === "" || $.trim(text) === "") {
        e.preventDefault();
        return false;
    }

    $(".suggestions").remove();
    $(".quickReplies").remove();
    $(".usrInput").blur();
    $(".dropDownMsg").remove();
    setUserResponse(text);
    // var flag = $("#hiddenFlag").val();
    send(text);
    e.preventDefault();
    return false;
});
