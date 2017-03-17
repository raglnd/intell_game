/*  INTELL The Craft of Intelligence
 *    https://github.com/dylan-wright/cs499-intell/
 *    https://intellproject.com/
 *
 *    game/static/game/actions.js
 *      js controller for front end
 *      Modules:
 *        Actions
 */

/*  Actions
 *    module for controlling behavior of clicking various action buttons
 *    should ensure only one button is active at a time and present
 *    user with options based on clicked button. Then confirm to send
 *    AJAX/JSON request to server. Action will be proccessed when game turn
 *    is over. Results will be sent back to user with new snippets when
 *    requested/ready
 *
 *    attributes
 *      settings
 *    methods
 *      init
 *      bindUIActions
 *      setActiveButton
 *      actionJSON
 *      sendAction
 *    action modal methods
 *      tail
 *      investigate
 *      check
 *      misinf
 *      recruit
 *      apprehend
 *      research
 *      terminate
 */
var Actions = (function () {
  /*  settings
   *    module wide settings used to access various attributes
   *    in module methods
   */
  var settings = {
    buttons: {
      tailButton: document.getElementById("tailBtn"),
      investigateButton: document.getElementById("investigateBtn"),
      checkButton: document.getElementById("checkBtn"),
      misinfButton: document.getElementById("misInfoBtn"),
      recruitButton: document.getElementById("recruitBtn"),
      apprehendButton: document.getElementById("apprehendBtn"),
      researchButton: document.getElementById("researchBtn"),
      terminateButton: document.getElementById("terminateBtn"),

      confirmTail: document.getElementById("confirmTail"),
      confirmInvestigate: document.getElementById("confirmInvestigate"),
      confirmCheck: document.getElementById("confirmCheck"),
      confirmMisinf: document.getElementById("confirmMisinf"),
      confirmRecruit: document.getElementById("confirmRecruit"),
      confirmApprehend: document.getElementById("confirmApprehend"),
      confirmResearch: document.getElementById("confirmResearch"),
      confirmTerminate: document.getElementById("confirmTerminate"),
    },
    activeButton: document.getElementById("researchBtn"),
    agentSelect: document.getElementById("agentSel"),
    agentWarn: document.getElementById("agentWarn"),
    loggedAct: document.getElementById("loggedAct"),

    tailCharSel: document.getElementById("tailCharSel"),
    investigateLocSel: document.getElementById("investigateLocSel"),
    checkDescSel: document.getElementById("checkDescSel"),
    misinfCharSel: document.getElementById("misinfCharSel"),
    misinfLocSel: document.getElementById("misinfLocSel"),
    misinfDescText: document.getElementById("misinfDescText"),
    apprehendCharSel: document.getElementById("apprehendCharSel"),
    terminateAgentSel: document.getElementById("terminateAgentSel"),
    actionTarget: null,
  };

  /*  bindUIActions
   *    used to bind user actions to js functions
   *    mainly used to attach event listeners to buttons
   */
  function bindUIActions () {
    //buttons for opening a modal
    settings.buttons.tailButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.tailButton);
      tail();
    });
    settings.buttons.investigateButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.investigateButton);
      investigate();
    });
    settings.buttons.checkButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.checkButton);
      check();
    });
    settings.buttons.misinfButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.misinfButton);
      misinf();
    });
    settings.buttons.recruitButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.recruitButton);
      recruit();
    });
    settings.buttons.apprehendButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.apprehendButton);
      apprehend();
    });
    settings.buttons.researchButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.researchButton);
      research();
    });
    settings.buttons.terminateButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.terminateButton);
      terminate();
    });

    //buttons in a modal
    settings.buttons.confirmTail.addEventListener("click", function() {
      settings.actionTarget = settings.tailCharSel.value;
      sendAction();
    });
    settings.buttons.confirmInvestigate.addEventListener("click", function() {
      settings.actionTarget = settings.investigateLocSel.value;
      sendAction();
    });
    settings.buttons.confirmCheck.addEventListener("click", function() {
      settings.actionTarget = settings.checkDescSel.value;
      sendAction();
    });
    settings.buttons.confirmMisinf.addEventListener("click", function() {
      settings.actionTarget = {"location": settings.misinfLocSel.value,
                               "character": settings.misinfCharSel.value,
                               "description": settings.misinfDescText.value};
      sendAction();
    });
    settings.buttons.confirmRecruit.addEventListener("click", function() {
      settings.actionTarget = null;
      sendAction();
    });
    settings.buttons.confirmApprehend.addEventListener("click", function() {
      settings.actionTarget = settings.apprehendCharSel.value;
      sendAction();
    });
    settings.buttons.confirmResearch.addEventListener("click", function() {
      settings.actionTarget = null;
      sendAction();
    });
    settings.buttons.confirmTerminate.addEventListener("click", function() {
      settings.actionTarget = settings.terminateAgentSel.value;
      sendAction();
    });
  };

  /*  setActiveButton
   *    used to toggle button when clicked
   *    called as part of each button's event listener
   *    also replaces the active button in the settings
   */
  function setActiveButton (clickedButton) {
    //replace .active with "" in prev clicked button
    settings.activeButton.className = 
        settings.activeButton.className.replace(/(?:^|\s)active(?!\S)/g, '');

    //add .active to class name of clicked button and make active
    clickedButton.className += " active";
    settings.activeButton = clickedButton;
  };

  /*  actionJSON
   *    returns the JSON for the current action
   */
  function actionJSON () {
    //agent is the agent selected in agentSel
    //the action name is the button id minus "btn"
    retObj = {
      "agent": settings.agentSelect.value,
      "action": settings.activeButton.id.slice(0,-3),
      "target": settings.actionTarget,
    };
    return JSON.stringify(retObj);
  };

  /*  sendAction
   *    send an AJAX request to /game/play/pk/submit_action/
   *    include return value of actionJSON (json rep of action
   */
  function sendAction () {
    var csrftoken = Cookies.get("csrftoken");
    var xhttp = new XMLHttpRequest();
    //TODO: make async true (add handler)
    xhttp.open("POST", "submit_action/", false);
    xhttp.setRequestHeader("X-CSRFtoken", csrftoken);
    var request = actionJSON();
    xhttp.send(request);
    var response = xhttp.responseText;

    var d = settings.agentWarn;
    d.innerHTML = settings.activeButton.id.slice(0,-3) + " action logged";
    d.hidden = true;
    //Create div element so it's displayed 
    loggedAct.innerHTML= settings.activeButton.id.slice(0,-3) + " action logged";
    settings.agentWarn.insertAdjacentElement("beforeBegin", d);

    //return request == response;
  };

  /*  verifyAgentSelected
   *    check if an agent has been selected
   *    if not, warn the user
   *    called before opening modals for actions
   */
  function verifyAgentSelected () {
    if (settings.agentSelect.value == "none") {
      settings.agentWarn.innerHTML = "Select an agent";
      return false;
    } else {
      settings.agentWarn.innerHTML = "";
      return true;
    }
  }

  /*  button click handlers
   *    all open a modal
   *    should also check for agent selected
   *    some must create a select dropdown
   */
  function tail () {
    if (verifyAgentSelected()) {
      //load charcters into select
      var characters = Snippets.getCharacters();
      var option;
      var i;

      clearSelect(settings.tailCharSel);
      for (i = 0; i < characters.length; i+=1) {
        option = document.createElement("option");
        option.text = characters[i].fields.name;
        option.value = characters[i].pk;
        settings.tailCharSel.add(option);
      }
      $("#tailModal").modal();
    }
  };
  function investigate () {
    if (verifyAgentSelected()) {
      //load locations into select
      var locations = Snippets.getLocations();
      var option;
      var i;

      clearSelect(settings.investigateLocSel);
      for (i = 0; i < locations.length; i+=1) {
        option = document.createElement("option");
        option.text = locations[i].fields.name;
        option.value = locations[i].pk;
        settings.investigateLocSel.add(option);
      }
      $("#investigateModal").modal();
    }
  };
  function check () {
    if (verifyAgentSelected()) {
      //load descriptions into select
      var descriptions = Snippets.getDescriptions();
      var option;
      var i;

      clearSelect(settings.checkDescSel);
      for (i = 1; i < descriptions.length; i+=2) {
        option = document.createElement("option");
        option.text = descriptions[i].text;
        option.value = descriptions[i].pk;
        settings.checkDescSel.add(option);
      }
      $("#checkModal").modal();
    }
  };
  function misinf () {
    if (verifyAgentSelected()) {
      var characters = Snippets.getCharacters();
      var locations = Snippets.getLocations();
      var option;
      var i;

      clearSelect(settings.misinfCharSel);
      for (i = 0; i < characters.length; i+=1) {
        option = document.createElement("option");
        option.text = characters[i].fields.name;
        option.value = characters[i].pk;
        settings.misinfCharSel.add(option);
      }

      clearSelect(settings.misinfLocSel);
      for (i = 0; i < locations.length; i+=1) {
        option = document.createElement("option");
        option.text = locations[i].fields.name;
        option.value = locations[i].pk;
        settings.misinfLocSel.add(option);
      }
      $("#misinfModal").modal();
    }
  };
  function recruit () {
    if (verifyAgentSelected()) {
      $("#recruitModal").modal();
    }
  };
  function apprehend () {
    if (verifyAgentSelected()) {
      var characters = Snippets.getCharacters();
      var option;
      var i;
      clearSelect(settings.apprehendCharSel);
      for (i = 0; i < characters.length; i+=1) {
        option = document.createElement("option");
        option.text = characters[i].fields.name;
        option.value = characters[i].pk;
        settings.apprehendCharSel.add(option);
      }
      $("#apprehendModal").modal();
    }
  };
  function research () {
    if (verifyAgentSelected()) {
      $("#researchModal").modal();
    }
  };
  function terminate () {
    if (verifyAgentSelected()) {
      var agents = getAgents();
      var option;
      var i;
      clearSelect(settings.terminateAgentSel);
      for (i = 0; i < agents.length; i+=1) {
        option = document.createElement("option");
        option.text = agents[i].fields.name;
        option.value = agents[i].pk;
        settings.terminateAgentSel.add(option);
      }
      $("#terminateModal").modal();
    }
  };

  function getAgents () {
    var xhttp = new XMLHttpRequest();
    //TODO: make async true
    xhttp.open("GET", "get_agents/", false);
    xhttp.send();
    response = xhttp.responseText;
    agents = JSON.parse(response);
    return agents;
  }

  function getOwnAgents () {
    var xhttp = new XMLHttpRequest();
    //TODO make async true
    xhttp.open("GET", "get_own_agents/", false);
    xhttp.send();
    response = xhttp.responseText;
    agents = JSON.parse(response);
    return agents;
  }

  function clearSelect (select) {
    while (select.length != 0) {
      select.remove(0);
    }
  }

  function reloadAgentList () {
    clearSelect (settings.agentSelect);
    var agents = getOwnAgents();
    var i;
    var option;
    for (i = 0; i < agents.length; i+=1) {
      option = document.createElement("option");
      option.value = agents[i].pk;
      option.innerHTML = agents[i].name;
      settings.agentSelect.add(option);
    }
  }
  
  return {
    /*  init
     *    function to initialize all members and bind
     *    ui actions
     *    called by global js initializer
     */
    init: function () {
      //connect buttons to events
      bindUIActions();
    },

    update: function () {
      reloadAgentList();
    }
  };
})();
