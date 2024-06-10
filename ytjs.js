// Sleep function
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


function openWindowWithPost(url, data) {
    var form = document.createElement("form");
    form.target = "popup";
    form.method = "POST";
    form.action = url;
    form.style.display = "none";

    for (var key in data) {
        var input = document.createElement("input");
        input.type = "hidden";
        input.name = key;
        input.value = data[key];
        form.appendChild(input);
    }

    document.body.appendChild(form);

    popup = window.open("", "popup");

    if (popup) {
        form.submit();
    } else {
        alert('You must allow popups for this to work.');
    }

    document.body.removeChild(form);


}


function getName() {
    let list = document.getElementsByClassName('style-scope yt-clip-creation-renderer');

    for (let i = 0; i < list.length; i++) {
        if (list[i].id == 'display-name') {
            return list[i].innerText;
        }
    }

    return null;
}

function clickButton(buttonId) {
    var button = document.getElementById(buttonId);
    button.click();
}

function hideElement(elementId) {
    var element = document.getElementById(elementId);
    element.style.display = 'none';
}

async function main() {

    var timeout = 5000

    clickButton('avatar-btn');

    var end = Date.now() + timeout;
    while (Date.now() < end) {
        const elements = document.querySelectorAll('button, div, span, a');
        for (let element of elements) {
            if (element.textContent.trim() === "Switch account") {
                // Simulate a click on the element
                element.click();
                end = Date.now(); //Stops retry
                break;
            }
        }
        await sleep(100);
    }

    var email = ""
    end = Date.now() + timeout;
    while (Date.now() < end) {
        let list = document.getElementsByClassName('style-scope ytd-google-account-header-renderer');
        for (let i = 0; i < list.length; i++) {
            if (list[i].id == 'email' && list[i].innerText != "") {
                email = list[i].innerText;
                end = Date.now(); //Stops retry
            }
        }
        await sleep(100);
    }

    // Create a new KeyboardEvent
    const escEvent = new KeyboardEvent('keydown', {
        key: 'Escape',    // The key value (could also be 'Esc' for older browsers)
        keyCode: 27,      // The key code for the Escape key
        code: 'Escape',   // The physical key on the keyboard
        which: 27,        // The key code for the Escape key
        bubbles: true,    // Whether the event bubbles up through the DOM
        cancelable: true  // Whether the event is cancelable
    });

    // Dispatch the event on the document
    document.dispatchEvent(escEvent);


    const url = 'http://127.0.0.1:8080/folderList';

    openWindowWithPost(url, {
        url: window.location.href,
        user: getName(),
        email: email
    });

    //send a post request to server contain user and email

}

main()
