/**
 * REFS TO SORT
 * https://stackoverflow.com/questions/39565706/post-request-with-fetch-api
 * https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
 * https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
 * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/endsWith
 * https://fastapi.tiangolo.com/advanced/templates/#install-dependencies
 * https://stackoverflow.com/questions/1927593/cant-update-textarea-with-javascript-after-writing-to-it-manually (.value vs .innerText)
 * https://stackoverflow.com/questions/77553191/how-do-i-go-about-removing-an-event-handler-created-in-an-arrow-function-so-that
 * https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/removeEventListener
 * https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
*/

var engine = {

    init: function () {
        // apply handler to tabs:
        let tabber_elems = document.getElementsByClassName("panel_selector_tab");
        for (let x = 0; x < tabber_elems.length; x++) {
            tabber_elems[x].addEventListener("click", (e) => {
                engine.tabHandler(e, tabber_elems);
            })
        }

        // handle tab selection AFTER the click handlers are applied...
        if (window.location.pathname.indexOf("/configure") !== -1 && window.location.hash.length > 0) {
            // NOTE: I modified the hash so it wouldn't actually be a DOM ID, so we didn't get the anchor jump...
            elem = document.getElementById(window.location.hash.replace('#', '').replace("_selected", ""));
            if (elem) {
                // https://medium.com/@python-javascript-php-html-css/javascript-to-emulate-a-click-on-the-first-button-in-a-list-9c61f408b4b5
                let evt = new PointerEvent('click', {
                    bubbles: true,
                    cancelable: true,
                    view: window,
                    pointerType: 'mouse',
                });
                elem.dispatchEvent(evt);
            }
        }

        /** 
         * Handle the cases where a link from thje compass configuration screen has been followed
         * in order to edit that component. Eventually, the passed ID will reflect the actively 
         * selected item. Currently, it is the saved item. 
         * In order to achieve this, the passed ID will need to be updated to reflect that selected 
         * by the user.
         */
        if(window.location.search){
            // console.log(window.location.search);
            sp = new URLSearchParams(window.location.search);
            // console.log(sp);
            // console.log(sp.get("sector_id"));   // OK
            // call function to trigger the dropdown change to the specified ID:
            // This works to select the dropdown, but the subsequent events to populate the 
            // other data are not triggered, even with a .click();...
            // probably need a conditional here:
            this.setSectorDropdownOnNavigateTo(sp.get("sector_id"));
            this.setQuadrantDropdownOnNavigateTo(sp.get("quadrant_id"));
            this.setRatingDropdownOnNavigateTo(sp.get("rating_id"));
            this.setQuadrantTitleDropdownOnNavigateTo(sp.get("quadrant_title_id"));
            this.setSectorTitleDropdownOnNavigateTo(sp.get("sector_title_id"));
        }

        /**
         * Append event handlers to the submit buttons for each component type. 
         * The handler is the same for all, but the args passed in determine 
         * which component type is being submitted.
         */
        let ComponentButtonData = [
            { "btnId": "quadrant_component_submit" }
        ]
        let submitBtnQuadrant = document.getElementById("quadrant_component_submit");
        submitBtnQuadrant.addEventListener("click", (e) => {
            // we also use this DOM ID to select from a lookup object of endpoints
            // because we will use the same handler for all add/update actions:
            // second is dropdown ID holding the database ID. I'd like to manage the 
            // dynamic bit in one place, so having the args passed in here to determine API path etc.
            // TODO:
            this.submitComponent(e, "manage_quadrants_select");
        });

        let submitBtnQuadrantTitle = document.getElementById("quadrant_title_component_submit");
        submitBtnQuadrantTitle.addEventListener("click", (e) => {
            this.submitComponent(e, "manage_quadrant_titles_select");
        });

        let submitBtnSector = document.getElementById("sector_component_submit");
        submitBtnSector.addEventListener("click", (e) => {
            this.submitComponent(e, "manage_sectors_select");
        });

        let submitBtnSectorTitle = document.getElementById("sector_title_component_submit");
        submitBtnSectorTitle.addEventListener("click", (e) => {
            this.submitComponent(e, "manage_sector_titles_select");
        });

        let submitBtnRatings = document.getElementById("rating_component_submit");
        submitBtnRatings.addEventListener("click", (e) => {
            this.submitComponent(e, "manage_ratings_select");
        });

        // now add the bits that are specific to the component configure page:
        let dropdown_elem_quadrants = document.querySelector("[data-identifier='quadrant']");
        dropdown_elem_quadrants.addEventListener("click", (e) => {
            this.selectComponentUIChangeHandler(event = e, prefix = "quadrant", submitBtn = submitBtnQuadrant, hiddenDataElemsIdList = ["summary", "description"]);
        })

        let dropdown_elem_quadrant_titles = document.querySelector("[data-identifier='quadrant_title']");
        dropdown_elem_quadrant_titles.addEventListener("click", (e) => {
            this.selectComponentUIChangeHandler(event = e, prefix = "quadrant_title", submitBtn = submitBtnQuadrantTitle, hiddenDataElemsIdList = ["part"]);
        })

        let dropdown_elem_sectors = document.querySelector("[data-identifier='sector']");
        dropdown_elem_sectors.addEventListener("click", (e) => {
            this.selectComponentUIChangeHandler(event = e, prefix = "sector", submitBtn = submitBtnSector, hiddenDataElemsIdList = ["summary", "description"]);
        })

        let dropdown_elem_sector_titles = document.querySelector("[data-identifier='sector_title']");
        dropdown_elem_sector_titles.addEventListener("click", (e) => {
            this.selectComponentUIChangeHandler(event = e, prefix = "sector_title", submitBtn = submitBtnSectorTitle, hiddenDataElemsIdList = ["part"]);
        })

        let dropdown_elem_ratings = document.querySelector("[data-identifier='rating']");
        dropdown_elem_ratings.addEventListener("click", (e) => {   // TODO: add named args
            this.selectComponentUIChangeHandler(event = e, prefix = "rating", submitBtn = submitBtnRatings, hiddenDataElemsIdList = ["title", "description"])
        })
        /** END OF COMPONENTS PAGE HANDLERS */
    },

    
    /** 
     * Manage autoselection of dropdown if coming form the compass configure page 
     * */
    setSectorDropdownOnNavigateTo : function(sectorId){
        // get the sector dropdown by it's ID:
        let elem = document.getElementById('manage_sectors_select');

        for(child of elem.children){
            if(child.value === sectorId){
                child.setAttribute("selected","selected");
                // now retrieve the hidden data:
                document.getElementById("sector_summary").innerText = document.getElementById(`sector_summary_${sectorId}`).innerText;
                document.getElementById("sector_description").innerText = document.getElementById(`sector_description_${sectorId}`).innerText;
                document.getElementById("sector_component_submit").value = "Update existing sector";
                break;
            }
        }
    },

    setQuadrantDropdownOnNavigateTo: function(quadrantId){
        console.log(quadrantId);
        let elem = document.getElementById('manage_quadrants_select');
        for(child of elem.children){
            if(child.value === quadrantId){
                child.setAttribute("selected","selected");
                // now retrieve the hidden data:
                document.getElementById("quadrant_summary").innerText = document.getElementById(`quadrant_summary_${quadrantId}`).innerText;
                document.getElementById("quadrant_description").innerText = document.getElementById(`quadrant_description_${quadrantId}`).innerText;
                document.getElementById("quadrant_component_submit").value = "Update existing quadrant";
                break;
            }
        }
    },

    setRatingDropdownOnNavigateTo : function(ratingId){
        console.log(ratingId);
        let elem = document.getElementById('manage_ratings_select');
        for(child of elem.children){
            if(child.value === ratingId){
                child.setAttribute("selected","selected");
                // now retrieve the hidden data:
                document.getElementById("rating_title").value = document.getElementById(`rating_title_${ratingId}`).innerText;
                document.getElementById("rating_description").innerText = document.getElementById(`rating_description_${ratingId}`).innerText;
                document.getElementById("rating_component_submit").value = "Update existing rating";
                break;
            }
        }
    },

    setQuadrantTitleDropdownOnNavigateTo : function(quadrantTitleId){
        console.log(quadrantTitleId);
        let elem = document.getElementById('manage_quadrant_titles_select');
        for(child of elem.children){
            if(child.value === quadrantTitleId){
                child.setAttribute("selected","selected");
                // now retrieve the hidden data:
                document.getElementById("quadrant_title_part").value = document.getElementById(`quadrant_title_part_${quadrantTitleId}`).innerText;
                document.getElementById("quadrant_title_component_submit").value = "Update existing quadrant title";
                break;
            }
        }
    },

    setSectorTitleDropdownOnNavigateTo : function(sectorTitleId){
        console.log(sectorTitleId)
        let elem = document.getElementById('manage_sector_titles_select');
        for(child of elem.children){
            if(child.value === sectorTitleId){
                child.setAttribute("selected","selected");
                // now retrieve the hidden data:
                document.getElementById("sector_title_part").value = document.getElementById(`sector_title_part_${sectorTitleId}`).innerText;
                document.getElementById("sector_title_component_submit").value = "Update existing sector title";
                break;
            }
        }
    },

    /** 
     * MANAGE THE UPDATE/NEW DROPDOWN LOGIC FOR EACH COMPONENT TYPE:
     * 
     * Because I want the same javascript handler for each type of component update,
     * I want a simple way to map the form elements being submitted and the endpoint
     * to which they go. Therefore, I map the dropdown element ID to the endpoint.
     * Further, the code below decides whether it's an update or a new component by
     * virtue of the selected option value (-1, or positive integer)
     * 
     * We also map the element IDs of the individual fields in each tab, so we can 
     * retrieve the data for submission to API.
     * 
     * I don't need the _id 
     */
    ENDPOINT_MAPPER: {
        "manage_quadrants_select": { "endpoint": "/compass/quadrant/", "data_elems": ["quadrant_id", "quadrant_summary", "quadrant_description"] },
        "manage_quadrant_titles_select": { "endpoint": "/compass/quadrants/title/", "data_elems": ["quadrant_title_id", "quadrant_title_part"] },
        "manage_sectors_select": { "endpoint": "/compass/sectors/", "data_elems": ["sector_id", "sector_summary", "sector_description"] },
        "manage_sector_titles_select": { "endpoint": "/compass/sectors/title/", "data_elems": ["sector_title_id", "sector_title_part"] },
        "manage_ratings_select": { "endpoint": "/compass/rating/", "data_elems": ["rating_id", "rating_title", "rating_description"] },
    },

    /**
     * Also if I return the new thing, I might be able to append to the existing dropdown rather than reloading the page///
     * Useed by /configure page
     */
    submitComponent: async function (e, itemSelectDOMId) {
        // the DOM ID of the DROPDOWN
        let component_id = parseInt(document.getElementById(itemSelectDOMId).value);
        // and use the above as a key to determine which endpoint we send to...
        let endpoint = engine.ENDPOINT_MAPPER[itemSelectDOMId]["endpoint"];   // hacky!!
        if (component_id !== -1) {
            endpoint += "update/";
        }
        // once we have determined which endpoint to use, collect the data to POST:
        // [NOTE: I need to implement data integrity checking etc. and alert the
        // user if data is not present/wrong!!]
        let submit_data = {};
        /** 
         * Here, we iterate over the declared DOM elements in the field mapper above
         * for the component type being updated/created - (THIS is where we need a
         * better DOM ID to database ID mapping logic!!) - and extract the values
         * being submitted.
         * 
         * If the ID value from the select box is -1 (i.e. is NOT a database ID value)
         * we assume a NEW component is to be created, and we don't append this value.
         * The FastAPI has two models for each - one with and one without an ID and the
         * back-end processes accordingly (update or new).   
         */
        for (let idx = 0; idx < engine.ENDPOINT_MAPPER[itemSelectDOMId]["data_elems"].length; idx++) {

            let currentDataDOMEntry = document.getElementById(engine.ENDPOINT_MAPPER[itemSelectDOMId]["data_elems"][idx]);
            let _val = currentDataDOMEntry.value;
            
            // Assume we are updating...
            let _append = true;
            // but check if we are creating a new one: 
            if (engine.ENDPOINT_MAPPER[itemSelectDOMId]["data_elems"][idx].endsWith("_id")) {
                _val = parseInt(_val);
                if (_val === -1) _append = false;
            }

            /** Append fieldnames unless it is a NEW item request */
            if (_append) {
                // retrieve the database fieldname from the current DOM element:
                let currentFieldName = currentDataDOMEntry.getAttribute("data-database-field");
                submit_data[currentFieldName] = document.getElementById(engine.ENDPOINT_MAPPER[itemSelectDOMId]["data_elems"][idx]).value;
            }
        }

        const response = await fetch(endpoint, {
            method: "post",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(submit_data),
        }).then((response) => {
            /** TODO: APIs should return the new or updated component */
            return (response.json());    // pass to next 'then'

        }).then((data) => {
            console.log(data);
            // https://www.geeksforgeeks.org/javascript/javascript-fetch-method/
            // As long as the back-end returns the correct object...
            // THIS TODO!!
            // console.log(data);
            // // I should be able to update the dropdown if I use returned data.
            // // which will either be a direct update of the dropdown, or an amendment
            // // of the generated DOM elements with a reload call to update the elems?
            // // I cannot update via the Flask load of template - cos that's a reload - 
            // // but I should be able to identify and add/update the DOM element??
            // // This MIGHT be a PITA / SLOW!!! to do.
            // // do I get this scope?
            // console.log(engine.ENDPOINT_MAPPER[itemSelectDOMId]["data_elems"]);
            // // for(item in data){
            // for(let x=0;x < engine.ENDPOINT_MAPPER[itemSelectDOMId]["data_elems"].length;x++){
            //     let item = engine.ENDPOINT_MAPPER[itemSelectDOMId]["data_elems"][x];
            //     console.log(item);
            //     // if(item !== "id"){
            //         // console.log(data[item]);
            //         console.log(item);  // a string
            //         // anyway, lets try:
            //         let targetElem = document.getElementById(`${item}_${data['id']}`);
            //         // OK now we hit the datafield mismatch issue again...
            //         console.log(`${item}_${data['id']}`);
            //         console.log(console.log(data[item]));
            //         if(targetElem){
            //             targetElem.innerText = data[item];
            //         }
            //     // }
            // }
            // in the mean time:
            document.location.reload();
        });
    },

    // handle configure tabber
    tabHandler: function (evt, tablist) {
        // 
        // let panel_list = document.getElementsByClassName("gutterpanel");
        // Select the list of panels to show/hide - independent of class name:
        let panel_list = document.querySelectorAll("[data-identifier='gutterpanel']");
        for (x = 0; x < tablist.length; x++) {
            tablist[x].classList.remove("panel_selector_tab_selected");
            panel_list[x].classList.add("hidden");
            if (x === parseInt(evt.srcElement.getAttribute("data-tabid")) - 1) {    // because '0' will do odd things...
                tablist[x].classList.add("panel_selector_tab_selected");
                panel_list[x].classList.remove("hidden");
                // and add a hash to the URL:
                // NOTE: I added arbitrary string to the end of the hash to prevent
                // the annoying - in this instance - browser scroll-to-anchor
                // action. The code elsewhere that selected the tab based on the hash
                // in the URL acounts for this addition, but the page doesn't jump any
                // more because there is no anchor of this name in the markup...
                window.location.hash = evt.srcElement.getAttribute("id") + "_selected";
            }
        }
    },

    // dropdown handler for manage components page. We are populaing a form, so it is different to the 
    // full compass one above] The key is the lookup data in the hidden DOM elements 
    selectComponentUIChangeHandler: function (event = event, prefix = prefix, submitBtn = submitBtn, hiddenDataElemsIdList = hiddenDataElemsIdList) {
        console.log("select event handler triggered")
        // the database ID textbox. Will be hidden, is an int
        document.getElementById(`${prefix}_id`).value = event.srcElement[event.srcElement.selectedIndex].value;

        // now figure out whetehr we are ADDING or UPDATING, and change the UI accordingly
        if (event.srcElement[event.srcElement.selectedIndex].value !== "-1") {
            /** Retrieve the current data for the selected database ID from the jinja template markup rendered elems holding the current values */
            for (let elemCount = 0; elemCount < hiddenDataElemsIdList.length; elemCount++) {
                document.getElementById(`${prefix}_${hiddenDataElemsIdList[elemCount]}`).value = document.getElementById(`${prefix}_${hiddenDataElemsIdList[elemCount]}_${event.srcElement[event.srcElement.selectedIndex].value}`).innerText;
            }
            submitBtn.value = `Update existing ${prefix.replace('_', ' ')}`;
        }
        else {
            for (let elemCount = 0; elemCount < hiddenDataElemsIdList.length; elemCount++) {
                document.getElementById(`${prefix}_${hiddenDataElemsIdList[elemCount]}`).value = "";
            }
            submitBtn.value = `Create new ${prefix.replace('_', ' ')}`;    // `prefix` does not always have an underscore
        }
    },
};

document.addEventListener("DOMContentLoaded",
    (evt) => {
        // console.log(window.location);
        engine.init();  //no arg
    }
);

// I may need this as well as the init() loading of the querystring:
// window.addEventListener("focus",(evt)=>{
//     console.log("focus")
//     console.log(window.location);
// })
