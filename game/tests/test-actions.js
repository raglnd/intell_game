casper.test.comment('actions.js test');
var helper = require('./djangocasper.js');
helper.scenario('/game/play/1/',
  //select agent for all options
  function () {
    casper.evaluate(function () {
      document.getElementById("agentSel").selectedIndex = 1;
    });
  },

  //test tail modal opens and closes
  function () {
    casper.evaluate(function () {
      document.getElementById("tailBtn").click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return $("#tailModal").is(":visible");
    }, "tail open");
  },
  function () {
    casper.evaluate(function () {
      document.getElementById("tailModal").getElementsByClassName(
        "modal-footer")[0].getElementsByClassName(
            "btn")[0].click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return !$("#tailModal").is(":visible");
    }, "tail close");
  },
  //test tail modal form populates and sends
  function () {
    casper.evaluate(function () {
      document.getElementById("tailBtn").click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    //test options not empty select one
    this.test.assertEval(function () {
      var select = document.getElementById("tailCharSel");
      var options = select.options;
      if (options.length > 1) {
        select.selectedIndex = 1;
      } else {
        return false;
      }
      document.getElementById("confirmTail").click();
      return true;
    }, "tail select character");
  },
  function () {
    casper.wait(1000);
  },
  function () {
    casper.log("hello", "error");
    casper.capture("tailcharmodal.png");
  },

  function () {
    casper.evaluate(function () {
      document.getElementById("investigateBtn").click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return $("#investigateModal").is(":visible");
    }, "invetigate open");
  },
  function () {
    casper.evaluate(function () {
      document.getElementById("investigateModal").getElementsByClassName("modal-footer")[0].getElementsByClassName("btn")[0].click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return !$("#investigateModal").is(":visible");
    }, "investigate close");
  },

  function () {
    casper.evaluate(function () {
      document.getElementById("checkBtn").click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return $("#checkModal").is(":visible");
    }, "check open");
  },
  function () {
    casper.evaluate(function () {
      document.getElementById("checkModal").getElementsByClassName("modal-footer")[0].getElementsByClassName("btn")[0].click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return !$("#checkModal").is(":visible");
    }, "check close");
  },

  function () {
    casper.evaluate(function () {
      document.getElementById("misInfoBtn").click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return $("#misinfModal").is(":visible");
    }, "misinf open");
  },
  function () {
    casper.evaluate(function () {
      document.getElementById("misinfModal").getElementsByClassName("modal-footer")[0].getElementsByClassName("btn")[0].click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return !$("#misinfModal").is(":visible");
    }, "misinf close");
  },

  function () {
    casper.evaluate(function () {
      document.getElementById("recruitBtn").click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return $("#recruitModal").is(":visible");
    }, "recruit open");
  },
  function () {
    casper.evaluate(function () {
      document.getElementById("recruitModal").getElementsByClassName("modal-footer")[0].getElementsByClassName("btn")[0].click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return !$("#recruitModal").is(":visible");
    }, "recruit close");
  },

  function () {
    casper.evaluate(function () {
      document.getElementById("apprehendBtn").click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return $("#apprehendModal").is(":visible");
    }, "apprehend open");
  },
  function () {
    casper.evaluate(function () {
      document.getElementById("apprehendModal").getElementsByClassName("modal-footer")[0].getElementsByClassName("btn")[0].click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return !$("#apprehendModal").is(":visible");
    }, "apprehend close");
  },

  function () {
    casper.evaluate(function () {
      document.getElementById("researchBtn").click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return $("#researchModal").is(":visible");
    }, "research open");
  },
  function () {
    casper.evaluate(function () {
      document.getElementById("researchModal").getElementsByClassName("modal-footer")[0].getElementsByClassName("btn")[0].click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return !$("#researchModal").is(":visible");
    }, "research close");
  },

  function () {
    casper.evaluate(function () {
      document.getElementById("terminateBtn").click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return $("#terminateModal").is(":visible");
    });
  },
  function () {
    casper.evaluate(function () {
      document.getElementById("terminateModal").getElementsByClassName("modal-footer")[0].getElementsByClassName("btn")[0].click();
    });
  },
  function () {
    casper.wait(1000);
  },
  function () {
    this.test.assertEval(function () {
      return !$("#terminateModal").is(":visible");
    });
  }
);
helper.run()
