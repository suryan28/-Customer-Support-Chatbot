/* module for importing other js files */
function include(file) {
  const script = document.createElement("script");
  script.src = file;
  script.type = "text/javascript";
  script.defer = true;

  document.getElementsByTagName("head").item(0).appendChild(script);
}

/* import components */
include("./static/js/components/index.js");

window.addEventListener("load", () => {
  $(document).ready(() => {
    // drop down menu for close, restart conversation & clear the chats.
    $(".dropdown-trigger").dropdown();
  });
  // Toggle the chatbot screen
  $("#profile_div").click(() => {
    if (is_run == false) {
      setBotResponse([
        { text: "Hello and welcome to our customer support chat."},
      ]);
      is_run = true;
    }
    $(".profile_div").toggle();
    $(".widget").toggle();
  });

  // clear function to clear the chat contents of the widget.
  // $("#clear").click(() => {
  //   $(".chats").fadeOut("normal", () => {
  //     $(".chats").html("");
  //     $(".chats").fadeIn();
  //   });
  // });

  // close function to close the widget.
  $("#close").click(() => {
    $(".profile_div").toggle();
    $(".widget").toggle();
    scrollToBottomOfResults();
  });
});
