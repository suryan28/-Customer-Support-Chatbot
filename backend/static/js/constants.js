const host = window.location.host;
const server_url = `http://${host}/chatbot`;
const apiUrl = `http://${host}/raise_ticket`;
let previousResponse = null;
let count = 0;
let username = "";
let usertype = "";
let is_run = false;
let a_ticket = false;
let satisfied_count = 0;
let url = "https://usaprimesports.com/workflow/locations";
let message_for_tryout =
    "We're sorry to hear that there is currently no USA Prime location near you. 😞 As USA Prime is expanding rapidly, we recommend checking our locations page again to stay updated on any newly added locations! 🌍🚀";

let satisfied_response = [
    {
        text: "Have we satisfied your inquiry today? 😊👍\n",
        custom: {
            payload: "quickReplies",
            data: [
                {
                    title: "Yes",
                    payload: "../#y",
                },
                {
                    title: "No",
                    payload: "../#n",
                },
            ],
        },
    },
];

let open_ticket = [
    {
        text: "Please ask your question in a different way, or click on 🎫'Open Ticket'🎫 and we can have someone look into this for you. 🤔💬\n",
        custom: {
            payload: "quickReplies",
            data: [
                {
                    title: "Open Ticket",
                    payload: "../#ticket",
                },
            ],
        },
    },
];

let open_ticket_tryout = [
    {
        text: "Please open a ticket with your player's age and the USA Prime location you are interested in. 🏟️ We will happily pass your information along to the ICC that oversees that location. 🌟\n",
        custom: {
            payload: "quickReplies",
            data: [
                {
                    title: "Open Ticket",
                    payload: "../#ticket",
                },
            ],
        },
    },
];

let open_tryout = [
    {
        custom: {
            payload: "quickReplies",
            data: [
                {
                    title: "Yes",
                    payload: "../#yt",
                },
                {
                    title: "No",
                    payload: "../#nt",
                },
            ],
        },
    },
];

// let open_restart = [
//     {
//         text: "Thank you, and have a great rest of your day! 😊🌟\n",
//         custom: {
//             payload: "quickReplies",
//             data: [
//                 {
//                     title: "Restart Chat",
//                     payload: "../#restart",
//                 },
//             ],
//         },
//     },
// ];


let not_satisfied_ticket = [
    {
        text: "I'm sorry we are requesting a ticket to be opened in order to properly answer your question. Please click on 'Open Ticket' to below message.\n",
        custom: {
            payload: "quickReplies",
            data: [
                {
                    title: "Open Ticket",
                    payload: "../#ticket",
                },
            ],
        },
    },
];