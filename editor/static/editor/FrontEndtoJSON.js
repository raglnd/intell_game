/*  INTELL The Craft of Intelligence
 *    https://github.com/dylan-wright/cs499-intell/
 *    https://intellproject.com/
 *
 *    editor/static/editor/FrontEndtoJSON.js
 *      js controller for front end aspect of the editor
 *      Modules:
 *        toJSONClass
 */

/*  toJSONClass:
 *
 *  The toJSONClass() will be used to instantiate an object in the scenario editor
 *  HTML given values to replace the name, turn, point and author. After it is 
 *  instantiated, it's method will be called whenever an onclick even occurs 
 *  to one of it's related buttons. After this occurs, the hashmap hashJSON
 *  will be updated with the new objects. Once the submit method is used, the 
 *  JSON file will be formed using the hashmap and then sent to the back end.
 *
 *    attributes
 *      name -- Scenario title
 *      turn_num - number of turns in a scenario
 *      point_num - number of INTELL points provided initially
 *      author - author name
 *
 *      hashKey - used to identify where an object is located in hashJSON
 *      charKey - Keeps track of char objects
 *      eventKey - Keeps track of event objects   
 *      locKey - Keeps track of location objects   
 *      descKey - Keeps track of char description objects   
 *      descbyKey - Keeps track of describedby (relationship) objects   
 *      happatKey - Keeps track of happenedat (relationship)  objects   
 *      involvKey - Keeps track of involved (relationship)  objects    
 *		tagKey - Keeps track of all tags objects (so tables show up correctly)
 *
 *      eventTags[] - collection of event tags stored in the event object
 *      charHash[] - arrays for tab keys 
 *      eventHash[] - ""
 *      hashJSON[] - Primary hashMap that is used to contain all of the objects
 *          created by the user and send, so that they can be sent to the back
 *          end
 *
 *    methods
 *      add_char, edit_char, del_char - methods used to interract with char tab
 *      add_event, edit_event, del_event - methods used to interract with the 
 *          top half of the edit tab
 *      add_eventTag, edit_eventTag, del_eventTag - methods used to interract 
 *          with the bottom half of the event tab. 
 #      add_loc, edit_loc, del_loc -  methods used to interract with the location
 *          tab
 #      
 *      submitJSON - Method that takes the hashJSON method, generates a JSON
 *          message and then sends the results to the back end database
 *
 #      populateTagTargets - Small helper method that populates the "Target" 
 *          field based on the previously created objects and the Tag Type
 *      selChar - event listener that would change tab fields based on the 
 *          char element selected on the character tag
 *      selLoc - similar to selChar, but for location tab instead
 *      selEvent, selEventTag - similar to the previous tabs but are used to interract
 *          with both tables in the event tab.
 */

/* In progress:
 *
 *  Currently the functionality for the edit/delete methods are still in 
 *  progress. 
 *
 *  Also, there are still some issues with the saveJSON method that are currently
 *  being worked out.
 *
 *  For the record, most functions other than the add methods are still subject
 *  change and will likely to do so prior to the completion of this project
 */

 function save(filename, data) {
    var blob = new Blob([data], {type: 'text/csv'});
    if(window.navigator.msSaveOrOpenBlob) {
        window.navigator.msSaveBlob(blob, filename);
    }
    else{
        var elem = window.document.createElement('a');
        elem.href = window.URL.createObjectURL(blob);
        elem.download = filename;        
        document.body.appendChild(elem);
        elem.click();        
        document.body.removeChild(elem);
    }
}

/*

    toJSONClass() - Class that is used to instantiate and keep track of all of 
    the objects created by the user. 

*/

function toJSONClass() {


    //TODO:
        //Get the edit/delete buttons working  
        //Input validation?
        //figure out how to get values from the map for the location editor
        //Use onreadystatechange
		//have the add buttons deselect from associated table
		//have add/edit clear the input fields

    //Scenario properties
    this.name = 'NULL';
    this.turn_num = 20;
    this.point_num = 20;
    this.author = 'NULL';

    //Unique keys for each of the tabs to uniquely identify objects in the 
    //hashJSON structure
    this.hashKey = 0;
    this.charKey = 0;
    this.eventKey = 0;
    this.locKey = 0;

    //need event related keys as well...
    this.descKey = 0;
    this.descbyKey = 0;
    this.happatKey = 0;
    this.involvKey = 0;
	this.tagKey = 0;
    
    //Used for the event listeners 
    this.currSelObj = {};
	this.currSelTag = {};

    //Collection of event tags that will be stored in an event object
    this.eventTags = [];

	//key hashing arrays for the tab keys so that they can be used in the hashJSON structure
	this.charHash = [];
	this.eventHash = [];
	this.locHash = [];
	
    //hashMap to contain input received from the user  
    this.hashJSON = [];

    // Need var for input
	this.input = $(document.createElement('input'));
    this.input.attr("type", "file");   

/*
  	Suggested Characters (added by YJ - Spring 2017) 
		Functions like add_char, but with edits

	This function, when run, will add one suggested character
	name from the database into the character name field.
*/
    this.get_sugChar = function() {  
	
	var charName; // AJAX request to get suggested character name
	$.ajax({ // Relies on get_sugCharName(request) in views.py
        	url: '../character/get_sugCharName/', // url pattern in urls.py
        	data: {
          		'name': charName
        	},
        	dataType: 'json',
		async: false, 
        	success: function (data) {
			charName = data["name"];
        	}
      	});

	var isKey = document.getElementById('keyCharBox').checked; // default
	var charNotes = document.getElementById('charComment').value; // default

        //Create a character object to be used when selSugChar (below) is run
        var charObj = {
            model:"editor.character",
            pk:this.CharKey, 
            fields:{
                name: charName,
                key: isKey,
                notes: charNotes
            }
        };

	// Add suggestion character to table --> delete last suggested character
	var totalRows = document.getElementById('sugCharsTableBody').rows.length-1;
	if(totalRows > 0){ // if table isn't empty
		// modified from del_char function
		//delete the table element
        	var table = document.getElementById("sugCharsTableBody");
        	table.deleteRow(0);
		
        	//clear the input fields
		document.getElementById('charNameBox').value = "";
		document.getElementById('keyCharBox').checked = false;
		document.getElementById('charComment').value = "";
	}
        var newCharElement = document.getElementById("sugCharsTableBody").insertRow(0);
        cell = newCharElement.insertCell(0);
        cell.innerHTML = charName;

        //EventListener used when a row in the character table is selected 
        newCharElement.addEventListener("click", function(){selSugChar(charObj);});

	// suggested character cannot be edited or deleted --> can add to scenario
	document.getElementById('charEditBtn').disabled = true; // default
	document.getElementById('charDelBtn').disabled = true; // default
    }

	this._add_char = function(charName, isKey, charNotes) {
		//Create a character object to match with the fixture.json format
        var charObj = {
            model:"editor.character",
            pk:this.charKey, 
            fields:{
                name: charName,
                key: isKey,
                notes: charNotes
            }
        };

        //Add the character object to the hashmap where the pk will be used
        //to determine this objects location
        this.hashJSON[this.hashKey] = charObj;

		//put the value into the hash array for later use
		this.charHash[this.charKey] = this.hashKey;
		
		//reset the highlighting for the selection
		var table = document.getElementById('charsTableBody');
		for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
		}
		
        //Need to add the character object to the table as well...
        var newCharElement = document.getElementById("charsTableBody").insertRow(0);
        cell = newCharElement.insertCell(0);
        cell.innerHTML = charName;

        //EventListener used when a row in the character table is selected 
        newCharElement.addEventListener("click", function(){selChar(charObj);});
        		
        //incrememnt the keys associated with character object and hash location. 
        this.hashKey++;
        this.charKey++;
	}
	
    /*
        add_char takes no arguments and is called when the add button is selected
        in the character tab.

        It receives the values stored in each fo the fields for the character
        tab, creates a formalized character object and stores the result in the
        object's hash map.
    */
    this.add_char = function() {  


        //Fetch the desired attributes for the character
        var charName = document.getElementById('charNameBox').value;
        var isKey = document.getElementById('keyCharBox').checked;
        var charNotes = document.getElementById('charComment').value;

        this._add_char(charName, isKey, charNotes);

		//clear the input fields
		document.getElementById('charNameBox').value = "";
		document.getElementById('keyCharBox').checked = "";
		document.getElementById('charComment').value = "";
		document.getElementById('charEditBtn').disabled = true;
		document.getElementById('charDelBtn').disabled = true;
    }

    this.edit_char = function() {
        
        var charName = document.getElementById('charNameBox').value;
        var isKey = document.getElementById('keyCharBox').checked;
        var charNotes = document.getElementById('charComment').value;
    

        //Use key value to locate the object in the hashmap and edit the fields
		var editTarget = this.hashJSON[this.charHash[window.currSelObj.pk]];
        editTarget.fields.name = charName;
		editTarget.fields.key = isKey;
		editTarget.fields.notes = charNotes;
		
        //also need to edit that specified value in the table
		//get ref to table object
        var table = document.getElementById("charsTableBody");

        //Find the position where things will be changed
        var currPos = (table.rows.length-1) - window.currSelObj.pk;

		table.rows[currPos].cells[0].innerHTML = charName;
		
		//clear the input fields
		document.getElementById('charNameBox').value = "";
		document.getElementById('keyCharBox').checked = "";
		document.getElementById('charComment').value = "";
		
		//reset the highlighting for the selection
		for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
		}
		document.getElementById('charEditBtn').disabled = true;
		document.getElementById('charDelBtn').disabled = true;
    }

    this.del_char = function() {
        //Need to account for multiple variables when deleting a character
        //First need to update the charKey and charHash attributes 
        this.charKey--;
        this.hashKey--;

        //Store the pivot location so that the keys can be updated
        var pivotLoc = window.currSelObj.pk;

        //For each element in the character hash, check if the location is
        //greater than the pivot
        for(var iCharHash in this.charHash){
            if(iCharHash > pivotLoc && iCharHash != pivotLoc){
                //Need to reset 
                //this.charHash[iCharObj.pk] = this.charHash[iCharObj.pk+1];
                //decrement the pk of the object after the deleted value 
                this.hashJSON[this.charHash[iCharHash]].pk--;
				this.charHash[iCharHash]--;
            }
        }

        //delete the actual object using the splice method
        this.hashJSON.splice(this.charHash[window.currSelObj.pk], 1);

        //remove the element the charHash as well to lineup with hashJSON
        this.charHash.splice(window.currSelObj.pk, 1);

        //finally delete the table element
        var table = document.getElementById("charsTableBody");
        var currPos = (table.rows.length-1) - window.currSelObj.pk;
        table.deleteRow(currPos);
		
        //clear the input fields
		document.getElementById('charNameBox').value = "";
		document.getElementById('keyCharBox').checked = false;
		document.getElementById('charComment').value = "";
		
		//reset the highlighting for the selection
		for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
		}
		document.getElementById('charEditBtn').disabled = true;
		document.getElementById('charDelBtn').disabled = true;
    }

	this._add_event = function(eventName, isKey, isSecret, eventSnip, secretSnip, tagTurn) {
		//TODO: add some input validation based event tags 

        //Create an event object to match with the fixture.json format
        var eventObj = {
            model:"editor.event",
            pk:this.eventKey,

            fields:{
                name: eventName,
                turn: tagTurn
            },

            // descKey++ seems bad. - 5/2/17
            description:{
                descmodel:'editor.description',
                descpk:this.descKey++,
                key: isKey,
                secret: false,
                snippet: eventSnip,
                describedby:{
                    descbymodel:'editor.describedby',
                    descbypk:this.descbyKey++
                }
            },
			
			//add the secret description
			//isSecret is used later to determine if it gets added to the JSON array in submitJSON
			secretDescription:{
				descmodel:'editor.description',
                descpk:this.descKey,
                key: isKey,
                secret: isSecret,
                snippet: secretSnip,
                describedby:{
                    descbymodel:'editor.describedby',
                    descbypk:this.descbyKey
                }
			},

            // All of eventTags.
            tags:this.eventTags.slice()
        };

        //Add the character object to the hashmap where the pk will be used
        //to determine this objects location
        this.hashJSON[this.hashKey] = eventObj;
		
		//put the value into the hash array for later use
		this.eventHash[this.eventKey] = this.hashKey;

		//reset the highlighting for the selection
		var table = document.getElementById('eventsTableBody');
		for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
		}
		
        //Update the events table with the new event object 
        var newEventElement = document.getElementById("eventsTableBody").insertRow(0);
        eventNameCell = newEventElement.insertCell(0);
        eventNameCell.innerHTML = eventObj.fields.name;

        //EventListener used when a row in the events table is selected 
        newEventElement.addEventListener("click", function(){selEvent(eventObj);});
		
        this.eventKey++;
        this.hashKey++;
        this.descKey++;
        this.descbyKey++;
			
		this.tagKey = 0;
        // Empties out eventTags.
		this.eventTags.splice(0,this.eventTags.length);
	}
	
	
    /*
        add_event takes no arguments and is called when the add button is selected
        in the event tab.

        it reacts similarly to the add_character method, but with the unique
        fields associated with the event tab
    */ 
    this.add_event = function() {
       
        //Get values stored in the current fields 
        var eventName = document.getElementById('eventNameBox').value;
        var isKey = document.getElementById('eventKeyBoxIn').checked;
        var isSecret = document.getElementById('eventSecretBoxIn').checked;
        var eventSnip = document.getElementById('snippet').value;
        var secretSnip = document.getElementById('secretSnippet').value;
        var tagTurn = document.getElementById('turnTagSel').value;
		
        this._add_event(eventName, isKey, isSecret, eventSnip, secretSnip, tagTurn);
		
		document.getElementById('eventNameBox').value = "";
        document.getElementById('eventKeyBoxIn').checked = "";
        document.getElementById('eventSecretBoxIn').checked = "";
        document.getElementById('snippet').value = "";
        document.getElementById('secretSnippet').value = "";
        document.getElementById('turnTagSel').value = "0";
    	var table = document.getElementById('eventsTagBody');
		var rowsLen = table.rows.length;
		for(i = 0; i < rowsLen; i++){
			table.deleteRow(0);
		}
		
		$('#secretCollapse').collapse('hide');
		
		//Enable the edit/delete buttons and highlight the selected row
		document.getElementById('eventEditBtn').disabled = true;
		document.getElementById('eventDelBtn').disabled = true;
		document.getElementById('eventTagEditBtn').disabled = true;
		document.getElementById('eventTagDelBtn').disabled = true;
	}

    this.edit_event = function() {
        
        var eventName = document.getElementById('eventNameBox').value;
        var isKey = document.getElementById('eventKeyBoxIn').checked;
        var isSecret = document.getElementById('eventSecretBoxIn').checked;     
		var eventSnip = document.getElementById('snippet').value;
        var secretSnip = document.getElementById('secretSnippet').value;
        var tagTurn = document.getElementById('turnTagSel').value;
		
		var editTarget = this.hashJSON[this.eventHash[window.currSelObj.pk]];
		
		editTarget.fields.name = eventName;
		editTarget.fields.turn = tagTurn;
		
		editTarget.description.key = isKey;
		editTarget.description.snippet = eventSnip;
		editTarget.secretDescription.key = isKey;
		editTarget.secretDescription.secret = isSecret;
		editTarget.secretDescription.snippet = secretSnip;
        
        // All of eventTags.
		editTarget.tags = this.eventTags.slice();
		
		var table = document.getElementById('eventsTableBody');
		var rowLen = table.rows.length - 1;
		table.rows[rowLen - editTarget.pk].cells[0].innerHTML = eventName;
		
		for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
		}
		
		document.getElementById('eventNameBox').value = "";
        document.getElementById('eventKeyBoxIn').checked = "";
        document.getElementById('eventSecretBoxIn').checked = "";
        document.getElementById('snippet').value = "";
        document.getElementById('secretSnippet').value = "";
        document.getElementById('turnTagSel').value = "0";
    	var table2 = document.getElementById('eventsTagBody');
		var rowsLen = table2.rows.length;
		for(i = 0; i < rowsLen; i++){
			table2.deleteRow(0);
		}
		
		$('#secretCollapse').collapse('hide');
		
        // Empties out eventTags.
		this.eventTags.splice(0,this.eventTags.length);
        
		//Enable the edit/delete buttons and highlight the selected row
		document.getElementById('eventEditBtn').disabled = true;
		document.getElementById('eventDelBtn').disabled = true;
		document.getElementById('eventTagEditBtn').disabled = true;
		document.getElementById('eventTagDelBtn').disabled = true;
    }

    this.del_event = function() {
        //change to currObj or whatever
		this.eventKey--;
		this.hashKey--;
		this.descbyKey-=2;
		this.descKey-=2;
		
		var pivotLoc = window.currSelObj.pk;
		
        for(var iEventHash in this.eventHash){
			if(iEventHash > pivotLoc && iEventHash != pivotLoc){
				this.hashJSON[this.eventHash[iEventHash]].pk--;
				this.eventHash[iEventHash]--;
			}
		}
		
		//delete the actual object using the splice method
        this.hashJSON.splice(this.eventHash[window.currSelObj.pk], 1);

        //remove the element the eventHash as well to lineup with hashJSON
        this.eventHash.splice(window.currSelObj.pk, 1);

        //finally delete the table element
        var table = document.getElementById("eventsTableBody");
        var currPos = (table.rows.length-1) - window.currSelObj.pk;
        table.deleteRow(currPos);
		
		document.getElementById('eventNameBox').value = "";
        document.getElementById('eventKeyBoxIn').checked = "";
        document.getElementById('eventSecretBoxIn').checked = "";
        document.getElementById('snippet').value = "";
        document.getElementById('secretSnippet').value = "";
        document.getElementById('turnTagSel').value = "0";
		
		for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
		}
		
    	var table = document.getElementById('eventsTagBody');
		var rowsLen = table.rows.length;
		for(i = 0; i < rowsLen; i++){
			table.deleteRow(0);
		}
		
		$('#secretCollapse').collapse('hide');
		
		this.eventTags.splice(0,this.eventTags.length);
		//Enable the edit/delete buttons and highlight the selected row
		document.getElementById('eventEditBtn').disabled = true;
		document.getElementById('eventDelBtn').disabled = true;
			
		document.getElementById('eventTagEditBtn').disabled = true;
		document.getElementById('eventTagDelBtn').disabled = true;
    }

	this._add_eventTag = function(tagTypeinput, selTarget) {
        var tagType = '';
        var currModel = '';
        var currTagKey = 0;
        var currTarget;
        var selTag = '';
        var selTargetText = '';
		
		//Iterate through the charactr/location hash arrays to find the key
        //with the desired target name in order to get the pk of that object
        var key;
        //Check if we need to check through character or location obejects 
        if(tagTypeinput == 0){
            for(key in this.charHash){
                if(this.hashJSON[this.charHash[key]].pk == selTarget){
                    currTarget = this.hashJSON[this.charHash[key]];
                }
            }
        }
        else{
            for(key in this.locHash){
                if(this.hashJSON[this.locHash[key]].pk == selTarget){
                    currTarget = this.hashJSON[this.locHash[key]];
                }
            }
        }
        
        //check if tag type is character or location and match values based on result
        //If selected index=0, then character was selected and involved tag is used
        if(tagTypeinput == 0){
            currModel = 'editor.involved';
            selTag = 'involved';
            tagType = 'Character';
            currTagKey= this.involvKey;
            this.involvKey++;
            //this.hashKey++;
        }

        else{
            currModel = 'editor.happenedat';
            selTag = 'happened at';
            tagType = 'Location';
            currTagKey = this.happatKey;
            this.happatKey++;
            //this.hashKey++;
        }

        //The event tag object 
        var eventTagObj = {
			pk: this.tagKey,
            tagmodel: currModel,
            tagpk: currTagKey,
            targetpk: currTarget.pk,
            tagtypeinput: tagType,
            targetinput: document.getElementById('targetSel')
        };
		
		this.tagKey++;

        //Update the table with the new tag element 
		
		var table = document.getElementById('eventsTagBody');
		for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
		}
		
        var newEventTagElement = document.getElementById("eventsTagBody").insertRow(0);
        TagName = newEventTagElement.insertCell(0);
        TargetName = newEventTagElement.insertCell(1);
        TagName.innerHTML = selTag;
        TargetName.innerHTML = currTarget.fields.name;

        //enable row selection 
        newEventTagElement.addEventListener("click", function(){selEventTag(eventTagObj);});
		
        //Push the event tag to the array event object uses
        this.eventTags.push(eventTagObj);
	}
	
    this.add_eventTag = function(){
        
        var tagTypeinput = document.getElementById('tagTypeSel').selectedIndex;
        var selTarget = document.getElementById('targetSel').value;
		
		this._add_eventTag(tagTypeinput, selTarget);

		document.getElementById('eventTagEditBtn').disabled = true;
		document.getElementById('eventTagDelBtn').disabled = true;
    }

    this.edit_eventTag = function(){
        var tagTypeinput = document.getElementById('tagTypeSel').selectedIndex;
        var tagType = '';
        var currModel = '';
        var currTagKey = 0;
        var currTarget;
        var selTag = '';
        var selTargetText = '';
        var selTarget = document.getElementById('targetSel');
		if(tagTypeinput == 0){
            for(key in this.charHash){
                if(this.hashJSON[this.charHash[key]].pk == selTarget.value){
                    currTarget = this.hashJSON[this.charHash[key]];
                }
            }
        }
        else{
            for(key in this.locHash){
                if(this.hashJSON[this.locHash[key]].pk == selTarget.value){
                    currTarget = this.hashJSON[this.locHash[key]];
                }
            }
        }
		
		//check if tag type is character or location and match values based on result
        //If selected index=0, then character was selected and involved tag is used
        if(tagTypeinput == 0){
            currModel = 'editor.involved';
            selTag = 'involved';
            tagType = 'Character';
            currTagKey= this.involvKey;
            //this.hashKey++;
        }

        else{
            currModel = 'editor.happenedat';
            selTag = 'happened at';
            tagType = 'Location';
            currTagKey = this.happatKey;
            //this.hashKey++;
        }
		
		var editTarget = this.eventTags[window.currSelTag.pk];
		
		editTarget.tagmodel = currModel;
		editTarget.tagpk = currTagKey;
		editTarget.targetpk = currTarget.pk;
		editTarget.tagtypeinput = tagType;
		editTarget.targetinput = selTarget;
		
		var table = document.getElementById('eventsTagBody');
		for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
		}
        table.rows[table.rows.length - 1 - window.currSelTag.pk].cells[0].innerHTML = selTag;
        table.rows[table.rows.length - 1 - window.currSelTag.pk].cells[1].innerHTML = currTarget.fields.name;
		
		document.getElementById('eventTagEditBtn').disabled = true;
		document.getElementById('eventTagDelBtn').disabled = true;
    }

	//IN PROGRESS
    this.del_eventTag = function(){
		this.tagKey --;
		
		var pivotLoc = window.currSelTag.pk;
		
		if(currSelTag.currModel == 'editor.happenedat'){
			this.happatKey--;
		}
		else{
			this.involvKey--;
		}
			
		for(var tag in this.eventTags){
			if(tag > pivotLoc && tag != pivotLoc){
				this.eventTags[tag].pk--;
			}
		}
		this.eventTags.splice([window.currSelTag.pk], 1);
		
		var table = document.getElementById("eventsTagBody");
        var currPos = (table.rows.length-1) - window.currSelTag.pk;
        table.deleteRow(currPos);
		
		for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
		}
		
		document.getElementById('eventTagEditBtn').disabled = true;
		document.getElementById('eventTagDelBtn').disabled = true;
    }

    /*
  	Suggested Locations (added by YJ)
		Functions like add_loc and get_sugChar, but with edits 

	This function, when run, will take one location's data
	from the database and place it in the table for the user
	to potentially add to their scenario.
    */
    this.get_sugLoc = function() {

	var locName; 
	var locCoordX;
	var locCoordY;
	// AJAX request to get suggested character name
	$.ajax({ // Relies on get_sugLocInfo(request) in views.py
        	url: '../location/get_sugLocInfo/', // url pattern in urls.py
        	data: {
          		'name': locName,
			'x': locCoordX,
			'y': locCoordY
        	},
        	dataType: 'json',
		async: false, 
        	success: function (data) {
			locName = data["name"];
			locCoordX = data["x"];
			locCoordY = data["y"];
        	}
      	});

	//Create a location object to be used by selSugLoc (below)
        var locObj = {
            model:"editor.location",
            pk:this.locKey,
            fields:{
                name: locName,
                x: locCoordX,
                y: locCoordY
            }
        };	

	// Add suggestion location to table --> delete last suggested location
	var totalRows = document.getElementById('sugLocsTableBody').rows.length;
	if(totalRows > 0){ // if table isn't empty
		// modified from del_char function
		//delete the table element
        	var table = document.getElementById("sugLocsTableBody");
        	table.deleteRow(0);
	}

	var newLocElement = document.getElementById("sugLocsTableBody").insertRow(0);
        nameCell = newLocElement.insertCell(0);
        xCell = newLocElement.insertCell(1);
        yCell = newLocElement.insertCell(2);
		
        //EventListener used when a row in the locations table is selected 
        newLocElement.addEventListener("click", function(){selSugLoc(locObj);});
        
        nameCell.innerHTML = locName;
        xCell.innerHTML = locCoordX;
        yCell.innerHTML = locCoordY;
	
	// return input fields to default and disable edit/delete buttons
	document.getElementById('locNameInput').value = "";
        document.getElementById('locXinput').value = "";
        document.getElementById('locYinput').value = "";	
	document.getElementById('locEditBtn').disabled = true;
	document.getElementById('locDelBtn').disabled = true;
    }


	this._add_loc = function (locName, locCoordX, locCoordY) {
		//Create a location object to match with the fixture.json format
        var locObj = {
            model:"editor.location",
            pk:this.locKey,
            fields:{
                name: locName,
                x: locCoordX,
                y: locCoordY
            }
        };

        this.hashJSON[this.hashKey] = locObj;
		
		//put the value into the hash array for later use
		this.locHash[this.locKey] = this.hashKey;

		var table = document.getElementById('locsTableBody');
		for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
		}
		
        var newLocElement = document.getElementById("locsTableBody").insertRow(0);
        nameCell = newLocElement.insertCell(0);
        xCell = newLocElement.insertCell(1);
        yCell = newLocElement.insertCell(2);
		
        //EventListener used when a row in the locations table is selected 
        newLocElement.addEventListener("click", function(){selLoc(locObj);});
        
        nameCell.innerHTML = locName;
        xCell.innerHTML = locCoordX;
        yCell.innerHTML = locCoordY;
        
        this.locKey++;
        this.hashKey++;
	}
    /*
        add_loc takes no arguments and is called when the add button is selected
        in the locations tab.

        it reacts similarly to the add_loc method, but with the unique
        fields associated with the location tab
    */
    this.add_loc = function() {
        
        var locName = document.getElementById('locNameInput').value;
        var locCoordX = document.getElementById('locXinput').value;
        var locCoordY = document.getElementById('locYinput').value;

        this._add_loc(locName, locCoordX, locCoordY);
		
		document.getElementById('locNameInput').value = "";
        document.getElementById('locXinput').value = "";
        document.getElementById('locYinput').value = "";
		
		document.getElementById('locEditBtn').disabled = true;
		document.getElementById('locDelBtn').disabled = true;
    }

    this.edit_loc = function() {
       
        var locName = document.getElementById('locNameInput').value;
        var locCoordX = document.getElementById('locXinput').value;
        var locCoordY = document.getElementById('locYinput').value;
        
        //Replace the currently selected object with the new fields
        var editLoc = this.hashJSON[this.locHash[window.currSelObj.pk]];
		editLoc.fields.name = locName;
		editLoc.fields.x = locCoordX;
		editLoc.fields.y = locCoordY;

        var editLocObj = this.hashJSON[this.locHash[window.currSelObj.pk]];

        //Store a reference to the table object
        var table = document.getElementById("locsTableBody");
        //Find the current position in order to update the table
        var currPos =(table.rows.length-1) - window.currSelObj.pk;
        
		//put the changes into the table
        table.rows[currPos].cells[0].innerHTML = locName;
		table.rows[currPos].cells[1].innerHTML = locCoordX;
		table.rows[currPos].cells[2].innerHTML = locCoordY;
        
		//clear the input fields
        document.getElementById('locNameInput').value = "";
        document.getElementById('locXinput').value = "";
        document.getElementById('locYinput').value = "";
		
		//reset the highlighting for the selection
		for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
		}
		document.getElementById('locEditBtn').disabled = true;
		document.getElementById('locDelBtn').disabled = true;
    }


    this.del_loc = function() {

        //Decrement the keys associated with a locaiton
        this.locKey--;
        this.hashKey--;

        //Store the pivot to update the keys
        var pivotLoc = window.currSelObj.pk;

        //Check values after pivot and decrement them
        for(var iLocHash in this. locHash){
            if(iLocHash > pivotLoc && iLocHash != pivotLoc){
                this.hashJSON[this.locHash[iLocHash]].pk--;
				this.locHash[iLocHash]--;
            }
        }

        //Delete the object in hashJSON
        this.hashJSON.splice(this.locHash[window.currSelObj.pk], 1);

        //Delete the object in the locHash array
        this.locHash.splice(window.currSelObj.pk,1);

        //Finally, delete the actual row 
        var table = document.getElementById("locsTableBody");
        var currPos = (table.rows.length-1) - window.currSelObj.pk;
        table.deleteRow(currPos);
		
		//clear the input fields
        document.getElementById('locNameInput').value = "";
        document.getElementById('locXinput').value = "";
        document.getElementById('locYinput').value = "";
		
		//reset the highlighting for the selection
		for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
		}
		document.getElementById('locEditBtn').disabled = true;
		document.getElementById('locDelBtn').disabled = true;
    }



	this.createJSONArray = function() {
		var finalarr = [];

        scenariomodel = {
            "model": "editor.scenario",
            "pk": null,
            "fields": {
                "name": this.name,
                "turn_num": this.turn_num,
                "point_num": this.point_num
            }
        };
        finalarr.push(scenariomodel);

        //Iterate through each object in the hashMap
        for(var key in this.hashJSON){
            
            var currModel = this.hashJSON[key].model;

            //if element is a character/location then just push as is
            if(currModel == "editor.character" || currModel == "editor.location"){ 
                //this.hashJSON[key].pk = null;
                var currJSONobj = this.hashJSON[key];
            
                var JSONcharloc = {
                    "model": currJSONobj.model,
                    "pk": currJSONobj.pk+1,
                    "fields": currJSONobj.fields
                };
                finalarr.push(JSONcharloc);
            }

            //Else, it's some other event object 
            else{

                var currJSONobj = this.hashJSON[key];
                //first create the event object
                //Matching all fields as specified in fixture.json
                JSONevent = {
                    "model": currJSONobj.model,
                    "pk": currJSONobj.pk+1,
                    "fields": {
                        "turn": currJSONobj.fields.turn
                    }
                };
                finalarr.push(JSONevent);

                //then create the description object 
                JSONdesc = {
                    "model": currJSONobj.description.descmodel,
                    "pk": currJSONobj.description.descpk+1,
                    "fields": {
                        "text": currJSONobj.description.snippet,
                        "hidden": false
                    }
                };
                finalarr.push(JSONdesc);

                //then create the described by objects
                JSONdescby = {
                    "model": currJSONobj.description.describedby.descbymodel,
                    "pk": currJSONobj.description.describedby.descbypk+1,
                    //"pk": null,
                    "fields": {
                        "event_id": currJSONobj.pk+1,
                        "description_id": currJSONobj.description.descpk+1
                    }
                };
                finalarr.push(JSONdescby);
				
				if(currJSONobj.secretDescription.secret)
				{
					JSONdesc2 = {
						"model": currJSONobj.secretDescription.descmodel,
						"pk": currJSONobj.secretDescription.descpk+1,
						"fields": {
							"text": currJSONobj.secretDescription.snippet,
							"hidden": true
						}
					}
					finalarr.push(JSONdesc2);
					
					//then create the described by objects
					JSONdescby2 = {
						"model": currJSONobj.secretDescription.describedby.descbymodel,
						"pk": currJSONobj.secretDescription.describedby.descbypk+1,
						//"pk": null,
						"fields": {
							"event_id": currJSONobj.pk+1,
							"description_id": currJSONobj.secretDescription.descpk+1
						}
					};
					finalarr.push(JSONdescby2);
				}

                //Iterate through the tags and create those objects
                var JSONtag = {};
                for(var element in currJSONobj.tags){

                    //The tags can only be involved or happened at, so match those
                    //formats based on the model
                    if(currJSONobj.tags[element].tagmodel == 'editor.involved'){

                        JSONtag = {
                            "model": currJSONobj.tags[element].tagmodel,
                            "pk": currJSONobj.tags[element].tagpk++,
                            //"pk": null, 
                            "fields": {
                                "event_id": currJSONobj.pk+1,
                                "character_id": currJSONobj.tags[element].targetpk+1
                            }
                        };

                    }

                    else{

                         JSONtag = {
                            "model": currJSONobj.tags[element].tagmodel,
                            "pk": currJSONobj.tags[element].tagpk+1,
                            //"pk": null, 
                            "fields": {
                                "event_id": currJSONobj.pk+1,
                                "location_id": currJSONobj.tags[element].targetpk+1
                            }
                        };                       
                    }

                    finalarr.push(JSONtag);
                }

            }
        }
		return finalarr;
	}
	
    /*
        submitJSON method - takes no arguments but is cast on the current object
        to stringify all elements being currently stored in hashJSON in order
        to create a JSON object. 

        Also, the fields associated with the field tab are stored in the object 
        as well. 
    */
    this.submitJSON = function(){
        
        //Assign the values in the title field 
        this.name = document.getElementById('titleBox').value;
        this.turn_num = document.getElementById('turnSpin').value;
        this.point_num = document.getElementById('pointSpin').value;
        //Getting the author field populated? Can be done later


        //Create a final array that will contain the JSON objects
        finalarr = this.createJSONArray();

        //Generate the JSON file using stringify on the JSON array after the 
        //hashmap has been iterated through
        var fileUpload = JSON.stringify(finalarr);

        //Trying to send the current hashmap to the dump request webpage
        var xhttp = new XMLHttpRequest();
        //xhttp.open('POST', "../accept_ajax_scenario/", false);
        xhttp.open('POST', "../accept_ajax_scenario/", false);
        xhttp.send(fileUpload);
    
        var response = xhttp.responseText;
        var dict = JSON.parse(response);
        console.log(dict);
        Graph.getData(dict.tables, JSON.parse(dict.schema), JSON.parse(dict.dump), dict.split);


        var response = xhttp.responseText;
        var dict = JSON.parse(response);
        Graph.getData(dict.tables, JSON.parse(dict.schema), 
                      JSON.parse(dict.dump), dict.split);

        //Print out the results of the dump in the dump location at the bottom
        //of the webpage
        //document.getElementById('dumpLoc').innerHTML = xhttp.responseText;
    }
	
	this.saveJSON = function(){
        
        //Assign the values in the title field 
        this.name = document.getElementById('titleBox').value;
        this.turn_num = document.getElementById('turnSpin').value;
        this.point_num = document.getElementById('pointSpin').value;
        //Getting the author field populated? Can be done later


        //Create a final array that will contain the JSON objects
        finalarr = this.createJSONArray();

        //Generate the JSON file using stringify on the JSON array after the 
        //hashmap has been iterated through
        var fileUpload = JSON.stringify(finalarr);

		var filename = this.name + ".json";
		save(filename, fileUpload);
    }
	
	// Adds an event and snippets. EventData becomes empty.
	this.addEventObject = function(EventData) {
		// eventName, isKey, isSecret, eventSnip, secretSnip, tagTurn
		if (EventData.length == 0) {
			// Left intentionally empty.
		}
		else if (EventData.length == 1){
			this._add_event(EventData[0].pk, false, false, "", "", EventData[0].fields.turn);
			
			EventData.pop();
		}
		else if (EventData.length == 3){
			this._add_event(EventData[0].pk, false, false, EventData[1].fields.text, "", EventData[0].fields.turn);
			
			EventData.pop();
			EventData.pop();
			EventData.pop();
		}
		else if (EventData.length == 5){
			this._add_event(EventData[0].pk, false, true, EventData[1].fields.text, EventData[3].fields.text, EventData[0].fields.turn);
			
			EventData.pop();
			EventData.pop();
			EventData.pop();
			EventData.pop();
			EventData.pop();
		}
	}
	
	this.processJSON = function(JSONObj) {

		// Need to reset the current data
		// Currently possibly a mem leak
		//Scenario properties
		this.name = 'NULL';
		this.turn_num = 20;
		this.point_num = 20;
		this.author = 'NULL';

		//Unique keys for each of the tabs to uniquely identify objects in the 
		//hashJSON structure
		this.hashKey = 0;
		this.charKey = 0;
		this.eventKey = 0;
		this.locKey = 0;

		//need event related keys as well...
		this.descKey = 0;
		this.descbyKey = 0;
		this.happatKey = 0;
		this.involvKey = 0;
		this.tagKey = 0;
		
		//Used for the event listeners 
		this.currSelObj = {};
		this.currSelTag = {};

		//Collection of event tags that will be stored in an event object
		this.eventTags = [];

		//key hashing arrays for the tab keys so that they can be used in the hashJSON structure
		this.charHash = [];
		this.eventHash = [];
		this.locHash = [];
		
		//hashMap to contain input received from the user  
		this.hashJSON = [];
		
		// Need to add scenario, chars, and locs first.
		for (var key in JSONobj)
		{
			try {
				console.log(key);
				console.log(JSONobj[key]);
				console.log("next");
				
				// Need to grab the pk probably. Can ignore, assuming they are in order...
				// Actually will need to subtract 1 from each id.
				if (JSONobj[key].model == "editor.scenario") {
					
					// Possibly something with the author needs to be done.

					this.name = JSONobj[key].fields.name;
					this.turn_num = JSONobj[key].fields.turn_num;
					this.point_num = JSONobj[key].fields.point_num;
					
					document.getElementById('titleBox').value = this.name;
					document.getElementById('turnSpin').value = this.turn_num;
					document.getElementById('pointSpin').value = this.point_num;
				}
				else if (JSONobj[key].model == "editor.character") {
					this._add_char(JSONobj[key].fields.name, JSONobj[key].fields.key, JSONobj[key].fields.notes);
				}
				else if (JSONobj[key].model == "editor.location") {
					this._add_loc(JSONobj[key].fields.name, JSONobj[key].fields.x, JSONobj[key].fields.y);
				}
			}
			catch(err) {
				console.log(err);
			}
		}
        
        var EventData = [];
        var eventNum = -1;
        
        // Need to add event data.
        for (var key in JSONobj)
		{
			try {
				console.log(key);
				console.log(JSONobj[key]);
				console.log("next");
				
				
				if (JSONobj[key].model == "editor.event") {
                    eventNum = JSONobj[key].pk;
                    this.addEventObject(EventData);
                    
					EventData.push(JSONobj[key]);
				}
				else if (JSONobj[key].model == "editor.description") { // Always followed by a described by
					EventData.push(JSONobj[key]);
					// Do something with these.
					// JSONobj[key].fields.text;
					// JSONobj[key].fields.hidden;
				}
				else if (JSONobj[key].model == "editor.describedby") {
					EventData.push(JSONobj[key]);
					// Do something with these.
					// JSONobj[key].fields.event_id;
					// JSONobj[key].fields.description_id;
				}
				else if (JSONobj[key].model == "editor.involved") {
					if (eventNum != JSONobj[key].fields.event_id) {
                        this.addEventObject(EventData);
                    }
                    
					this._add_eventTag(0, JSONobj[key].fields.character_id - 1);
					// Do something with these.
					//JSONobj[key].fields.character_id;
				}
				else if (JSONobj[key].model == "editor.happenedat") {
                    if (eventNum != JSONobj[key].fields.event_id) {
                        this.addEventObject(EventData);
                    }
					this._add_eventTag(1, JSONobj[key].fields.location_id - 1);
					// Do something with these.
					//JSONobj[key].fields.event_id;
					//JSONobj[key].fields.location_id;
				}
			}
			catch(err) {
				console.log(err);
			}
		}
        
        // Add last event if exists.
        this.addEventObject(EventData);
	}

	this.loadFile = function(file) {
		console.log(file);
		
		fr = new FileReader();
		fr.onload = (function(x) {
			return function() {
				try {
					JSONobj = JSON.parse(fr.result);
				}
				catch (err) {
					// Could not parse.
					return false;
				}
				
				x.currEdit.processJSON(JSONobj); // Seems odd, but it works...
			}
		})(this);
		
		fr.readAsText(file);
	}
	
	this.loadJSON = function(){
		
		// Need to figure out how to load a file from user localName   
        this.input.trigger('click');
		
		loop(this.input, this.loadFile);
		
		function loop(inputVar, callback) {
		
			if (inputVar[0].files.length == 0) {
				setTimeout(loop, 10, inputVar, callback);
			}
			else {
				callback(inputVar[0].files[0]);
			}
		}
	}


    //method to populate the target selection when character/location is slected
    this.populateTagTargets = function(){
        var loopKey = 0;
        //store the element for the type and target selectors
        var targetSel = document.getElementById('targetSel');
        var tagType = document.getElementById('tagTypeSel');
    
        //clear the selector options list
        targetSel.innerHTML = '';


        //loop through each element in hashJSON and find the
		//characters or locations depending on which is selected in tagType
        for(var key in this.hashJSON)
        {
			if(this.hashJSON[key].model=="editor.character" && tagType.selectedIndex == 0)
			{
				var tarOption = document.createElement("option");
				tarOption.text = this.hashJSON[key].fields.name;
                tarOption.value = this.hashJSON[key].pk;
				targetSel.add(tarOption);
			}
			else if (this.hashJSON[key].model=="editor.location" && tagType.selectedIndex == 1)
			{
				var tarOption = document.createElement("option");
				tarOption.text = this.hashJSON[key].fields.name;
                tarOption.value = this.hashJSON[key].pk;
				targetSel.add(tarOption);
			}
        }
    }   

}

//instantiate the toJSONClass to utilize the needed methods
var currEdit = new toJSONClass();

var prevChar =0;
var prevLoc =0;
var prevEvent=0;

/*
    Suggested Character Selection Highlight (added by YJ - Spring 2017) 
	Functions like selChar and selSugChar, but with edits

    When run, function will highlight the selected suggestion
    and show suggestion's information in input boxes
*/
function selSugChar(charObj) {
    //Store current/total rows in order to determine which row is highlighted
    var currRow = charObj.pk;
    
    //Set fields to those associated with the selected object
    document.getElementById('charNameBox').value = charObj.fields.name;
    document.getElementById('keyCharBox').checked = charObj.fields.key;
    document.getElementById('charComment').value = charObj.fields.notes;

    //Enable the edit/delete buttons and highlight the selected row
    document.getElementById('charEditBtn').disabled = true;
    document.getElementById('charDelBtn').disabled = true;

    //Highlight the currently selected item reseting the background of an object
    //that is no longer selected
    document.getElementById('sugCharsTableBody').rows[0].cells[0].style.backgroundColor='lightblue';
    if(this.last != null) { // change highlight in character table
	document.getElementById('charsTableBody').rows[this.last].cells[0].style.backgroundColor='white';
    }

    //set the current object to the currently selected one
    window.currSelObj = charObj;
}

/*
    Used to handle highlighting and row selection for the character table
*/
function selChar(charObj) {

    //Store current/total rows in order to determine which row is hilighted
    var currRow = charObj.pk;
    var totalRows = document.getElementById('charsTableBody').rows.length-1;
    
    //Need to account for case in which the preevious character is deleted
    if(this.prevChar>totalRows){
        this.prevChar = totalRows;
    }
    
    //Set fields to those associated with the selected object
    document.getElementById('charNameBox').value = charObj.fields.name;
    document.getElementById('keyCharBox').checked = charObj.fields.key;
    document.getElementById('charComment').value = charObj.fields.notes;

    //Enable the edit/delete buttons and highlight the selected row
    document.getElementById('charEditBtn').disabled = false;
    document.getElementById('charDelBtn').disabled = false;

    //Highlight the currently selected item reseting the background of an object
    //that is no longer selected
    document.getElementById('charsTableBody').rows[totalRows-currRow].cells[0].style.backgroundColor='lightblue';
    this.last = totalRows-currRow; // added by YJ - Spring 2017
    document.getElementById('sugCharsTableBody').rows[0].cells[0].style.backgroundColor='white'; 
    if (this.prevChar != null && this.prevChar != currRow) {
        document.getElementById('charsTableBody').rows[totalRows-this.prevChar].cells[0].style.backgroundColor='white';
    }
    this.prevChar = currRow;

    //set the current object to the currently selected one
    window.currSelObj = charObj;

}

/*
    Suggested Location Selection Highlight (added by YJ)
	Functions like selLoc, but with edits

    When run, function will highlight the selected suggestion
    and show suggestion's information in input boxes

    Doesn't currently work --> bug with lockey and rowCount
*/
function selSugLoc(locObj) {
    //Store current/total rows in order to determine which row is highlighted
    var currRow = locObj.pk;

    //Set fields to those associated with the selected object
    document.getElementById('locNameInput').value = locObj.fields.name;
    document.getElementById('locXinput').value = locObj.fields.x;
    document.getElementById('locYinput').value = locObj.fields.y;
    
    //Disable the edit/delete buttons and highlight the selected row
    document.getElementById('locEditBtn').disabled = true;
    document.getElementById('locDelBtn').disabled = true;

    //Highlight the currently selected item reseting the background of an object
    //that is no longer selected
    document.getElementById('sugLocsTableBody').rows[0].cells[0].style.backgroundColor='lightblue';
	document.getElementById('sugLocsTableBody').rows[0].cells[1].style.backgroundColor='lightblue';
	document.getElementById('sugLocsTableBody').rows[0].cells[2].style.backgroundColor='lightblue';

    if(this.last != null) { // change highlight in location table
	document.getElementById('locsTableBody').rows[this.last].cells[0].style.backgroundColor='white';
	document.getElementById('locsTableBody').rows[this.last].cells[1].style.backgroundColor='white';
	document.getElementById('locsTableBody').rows[this.last].cells[2].style.backgroundColor='white';
    }

    //set current object to the currently selected one
    window.currSelObj = locObj;
}

/*
    Used to handle highlighting and row selection for the location table
*/
function selLoc(locObj) {

    //Store current/total rows in order to determine which row is hilighted
    var currRow = locObj.pk;
    var totalRows = document.getElementById('locsTableBody').rows.length -1;
   
    //Account the case where previous location was deleted
    if(this.prevLoc>totalRows){
        this.prevLoc = totalRows;
    }

    //Set fields to those associated with the selected object
    document.getElementById('locNameInput').value = locObj.fields.name;
    document.getElementById('locXinput').value = locObj.fields.x;
    document.getElementById('locYinput').value = locObj.fields.y;
    
    //Enable the edit/delete buttons and highlight the selected row
    document.getElementById('locEditBtn').disabled = false;
    document.getElementById('locDelBtn').disabled = false;

    //Highlight the currently selected item reseting the background of an object
    //that is no longer selected
    document.getElementById('locsTableBody').rows[totalRows-currRow].cells[0].style.backgroundColor='lightblue';
	document.getElementById('locsTableBody').rows[totalRows-currRow].cells[1].style.backgroundColor='lightblue';
	document.getElementById('locsTableBody').rows[totalRows-currRow].cells[2].style.backgroundColor='lightblue';
    this.last = totalRows-currRow; // added by YJ - Spring 2017
    document.getElementById('sugLocsTableBody').rows[0].cells[0].style.backgroundColor='white';
	document.getElementById('sugLocsTableBody').rows[0].cells[1].style.backgroundColor='white';
	document.getElementById('sugLocsTableBody').rows[0].cells[2].style.backgroundColor='white';
    if (this.prevLoc != null && this.prevLoc != currRow) {
        document.getElementById('locsTableBody').rows[totalRows-this.prevLoc].cells[0].style.backgroundColor='white';
		document.getElementById('locsTableBody').rows[totalRows-this.prevLoc].cells[1].style.backgroundColor='white';
		document.getElementById('locsTableBody').rows[totalRows-this.prevLoc].cells[2].style.backgroundColor='white';
    }

    this.prevLoc = currRow;
    //set current object to the currently selected one
    window.currSelObj = locObj;
    
}

/*
    Used to handle highlighting and row selection for the event table
*/
function selEvent(eventObj) {

    //Store current/total rows in order to determine which row is hilighted
    var currRow = eventObj.pk;
    var totalRows = document.getElementById('eventsTableBody').rows.length -1;
    
	//Account the case where previous location was deleted
    if(this.prevEvent>totalRows){
        this.prevEvent = totalRows;
    }
	
	//var eventTags = eventObj.fields.tags;
	
    //Set fields to those associated with the selected object	
    document.getElementById('eventNameBox').value = eventObj.fields.name;
    document.getElementById('eventKeyBoxIn').checked = eventObj.description.key;
    document.getElementById('eventSecretBoxIn').checked = eventObj.secretDescription.secret;
	document.getElementById('snippet').value = eventObj.description.snippet;
	document.getElementById('secretSnippet').value = eventObj.secretDescription.snippet;
	document.getElementById('turnTagSel').value = eventObj.fields.turn;
	
	//had to use jquery here to get the bootstrap object instead of the html
	//recolapse/reshow the secret snippet text area if the secret box is checked
	if(!eventObj.secretDescription.secret){
		$('#secretCollapse').collapse('hide');
	}
	
	else{
		$('#secretCollapse').collapse('show');
	}
    
    //Enable the edit/delete buttons and highlight the selected row
    document.getElementById('eventEditBtn').disabled = false;
    document.getElementById('eventDelBtn').disabled = false;

    //Highlight the currently selected item reseting the background of an object
    //that is no longer selected
    document.getElementById('eventsTableBody').rows[totalRows-currRow].cells[0].style.backgroundColor='lightblue';
    if (this.prevEvent != null && this.prevEvent != currRow) {
        document.getElementById('eventsTableBody').rows[totalRows-this.prevEvent].cells[0].style.backgroundColor='white';
    }
    this.prevEvent = currRow;
	
	//load the selected eventObj tags into the global tags array
	this.currEdit.eventTags = eventObj.tags.slice();
	
	//clear the tags table
	var table = document.getElementById('eventsTagBody');
	var rowsLen = table.rows.length;
	for(i = 0; i < rowsLen; i++){
		table.deleteRow(0);
	}
	
	//load the tags for the event into the tags table
	for(let i=0; i < eventObj.tags.length; i++){
		//Update the event tags table with the event tags objects
        var newEventTagElement = table.insertRow(0);
        tagTypeCell = newEventTagElement.insertCell(0);
		tagTargetCell = newEventTagElement.insertCell(1);
        if(eventObj.tags[i].tagmodel == "editor.involved"){
			tagTypeCell.innerHTML = "Involved";
			tagTargetCell.innerHTML = this.currEdit.hashJSON[this.currEdit.charHash[eventObj.tags[i].targetpk]].fields.name;
		}
		else if(eventObj.tags[i].tagmodel == "editor.happenedat"){
			tagTypeCell.innerHTML = "Happened At";
			tagTargetCell.innerHTML = this.currEdit.hashJSON[this.currEdit.locHash[eventObj.tags[i].targetpk]].fields.name;
		}
		//enable row selection 
		newEventTagElement.addEventListener("click", function(){selEventTag(eventObj.tags[i]);});
	}
	currEdit.populateTagTargets();
	window.currSelObj = eventObj;
}

/*
    Used to handle highlighting and row selection for the event tag table
*/
function selEventTag(tagObj) {
    //Store current/total rows in order to determine which row is hilighted
	console.log(tagObj);
    var currRow = tagObj.pk;
    var table = document.getElementById('eventsTagBody')
	var totalRows = table.rows.length -1;
    //Set fields to those associated with the selected object
    document.getElementById('tagTypeSel').value = tagObj.tagtypeinput;
	
	//Need to account for case in which the preevious character is deleted
    if(this.prevTag>totalRows){
        this.prevTag = totalRows;
    }
   
    //Enable the edit/delete buttons and highlight the selected row
    document.getElementById('eventTagEditBtn').disabled = false;
    document.getElementById('eventTagDelBtn').disabled = false;

    //Highlight the currently selected item reseting the background of an object
    //that is no longer selected
    for(i = 0; i < table.rows.length; i++) {
			for(j = 0; j < table.rows[i].cells.length; j++)
			{
				table.rows[i].cells[j].style.backgroundColor='white';
			}
	}
	table.rows[totalRows-currRow].cells[0].style.backgroundColor='lightblue';
    table.rows[totalRows-currRow].cells[1].style.backgroundColor='lightblue';
	
	currEdit.populateTagTargets();
	document.getElementById('targetSel').selectedIndex = tagObj.targetpk;
	
    this.prevTag = currRow;
    //Might need to fix this
    window.currSelTag = tagObj;
}



