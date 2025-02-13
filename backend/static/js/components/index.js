function include(file) {
    const script = document.createElement("script");
    script.src = file;
    script.type = "text/javascript";
    script.defer = true;

    document.getElementsByTagName("head").item(0).appendChild(script);
}

/* include all the components js file */

include("./static/js/components/chat.js");
include("./static/js/constants.js");
include("./static/js/components/botTyping.js");
include("./static/js/components/quickReplies.js");
include("./static/js/components/suggestionButtons.js");
