/*  INTELL The Craft of Intelligence
 *    https://github.com/dylan-wright/cs499-intell
 *    https://intellproject.com
 *
 *  game/static/game/waiting.js
 *    js controller for game waiting page
 *      Modules:
 *        Waiting
 */

/*  Waiting
 *    module for controlling the behavior of game waiting page document
 *
 *    private
 *      attributes
 *        settings
 *      methods
 *        bindUIActions
 *        update
 *        create
 *    public
 *      methods
 *        init
 */
var Waiting = (function () {
  /*    settings
   *      module wide attributes
   *      buttons, timers, games, document objects
   */
  var settings = {
    games: [],
    timers: [],
    buttons: {
      joinButton: document.getElementById("joinBtn"),
      playButton: document.getElementById("playBtn"),
      createButton: document.getElementById("createBtn"),
      endButton: document.getElementById("endBtn"),
    },
    createModalBody: document.getElementById("createModalBody"),
    currGamesBody: document.getElementById("currGamesBody"),
    currGamesRow: null,
    pendGamesBody: document.getElementById("pendGamesBody"),
    pendGamesRow: null,
  }

  /*  bindUIActions
   *    used to intialize event listeners
   */
  function bindUIActions () {
    //listener for join button
    settings.buttons.joinButton.addEventListener("click", function () {
      if (settings.pendGamesRow != null) {
        var key = settings.pendGamesBody.rows[settings.pendGamesRow].dataset.value;
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", window.location.pathname+key+"/join/", false);
        xhttp.send();
        //refresh
        window.location.pathname = window.location.pathname;
      }
    });

    //listener for play button
    settings.buttons.playButton.addEventListener("click", function () {
      if (settings.currGamesRow != null) {
        var key = settings.currGamesBody.rows[settings.currGamesRow].dataset.value;
        window.location.pathname = "/game/play/"+key+"/";
      }
    });

    //listener for create button
    settings.buttons.createButton.addEventListener("click", function () {
      create();
    });

    //listener for end button
    settings.buttons.endButton.addEventListener("click", function () {
      if (settings.currGamesRow != null) {
        var key = settings.currGamesBody.rows[settings.currGamesRow].dataset.value;
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "/game/games/"+key+"/end/", false);
        xhttp.send();
        response = JSON.parse(xhttp.responseText);
        if (response.deleted) {
          //settings.currGamesBody.deleteRow(settings.currGamesRow);
          //var rows settings.currGamesBody.rows;
          //refresh
          window.location.pathname = window.location.pathname;
        } else {
          alert(response.message);
        }
      }
    });

    //listeners for table rows
    var i;
    var rows = settings.currGamesBody.rows;
    for (i = 0; i < rows.length; i += 1) {
      (function (rowIndex) {
        settings.currGamesBody.rows[rowIndex].addEventListener("click", function () {
          if (settings.currGamesRow != null) {
            settings.currGamesBody.rows[settings.currGamesRow].className = "";
          }
          settings.currGamesBody.rows[rowIndex].className = "active";
          settings.currGamesRow = rowIndex;
          settings.buttons.endButton.disabled = false;
        });
      })(i);
    }

    rows = settings.pendGamesBody.rows;
    for (i = 0; i < rows.length; i += 1) {
      (function (rowIndex) {
        settings.pendGamesBody.rows[rowIndex].addEventListener("click", function () {
          if (settings.pendGamesRow != null) {
            settings.pendGamesBody.rows[settings.pendGamesRow].className = "";
          }
          settings.pendGamesBody.rows[rowIndex].className = "active";
          settings.pendGamesRow = rowIndex;
          settings.buttons.joinButton.disabled = false;
        });
      })(i);
    }
  }

  /*  update
   *    function attached to timer.
   *    update all timers every second
   */
  function update () {
    var i;
    var now = Math.round(Date.now()/1000);

    var rows = settings.currGamesBody.rows;
    for (i = 0; i < rows.length; i += 1) {
      var cell = rows[i].cells[3];
      var delta = cell.dataset.delta;
      var next = Math.round(cell.dataset.next);
      //currently lieing when timeout occoured
      var time = ((next-now) > 0 ? (next-now)%delta : delta-(now-next)%delta);

      var s = time % 60;
      var m = Math.trunc(time/60) % 60;
      var h = Math.trunc(time/3600) % 60;
      cell.innerHTML = (h < 10 ? "0"+h : h)+" : "+
                       (m < 10 ? "0"+m : m)+" : "+
                       (s < 10 ? "0"+s : s);
    }
  }

  /*  create
   *    function which communicates with the server's create
   *    game interface
   */
  function create () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
      if (xhttp.readystate == 4 && xhttp.status == 200) {
        response = xhttp.responseText;
        settings.createModalBody.innerHTML = response;
      }
    }
    xhttp.open("GET", "create/", true);
    xhttp.send();
    
    $("#gameModal").modal();
  }

  return {
    /*  init
     *    public function called to instantiate the object
     */
    init: function () {
      bindUIActions ();
      window.setInterval(update, 1000);
    }
  }
})();

(function() {
  Waiting.init();
})();
