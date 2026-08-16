// APIResponseMessage = {
//     message:"",
//     success:true,
//     source:"",
//     data:{},
// }


function isAPIResponseMessage(obj){
    console.log(Object.keys(obj))
    if("message" in obj && "success" in obj && "source" in obj && "data" in obj){
        console.log("its an APIResponseMessage")
        return(true);
    }
    else{
        console.log("its not an APIResponseMessage")
        return(false);
    }
}
var engine = {

    init: function () {

        var page = document.getElementsByTagName('body')[0].getAttribute('data-page');
        
        if (page === "configure") {
            // apply handler to tabs:
            let tabber_elems = document.getElementsByClassName("panel_selector_tab");
            for (let x = 0; x < tabber_elems.length; x++) {
                tabber_elems[x].addEventListener("click", (e) => {
                    engine.tabHandler(e, tabber_elems);
                })
            }


            // Add handlers for edit sectors links (POC)
            let sector_edit_links = document.querySelectorAll("[data-identifier='sector_edit_links']");
            for(let x=0;x<sector_edit_links.length;x++){
                sector_edit_links[x].addEventListener("click",(event)=>{
                    window.open(`/configure/components?sector_id=${event.target.getAttribute("data-current-id")}#tab_3_selected`,"components")
                    event.preventDefault();
                })
            }

            // Add handlers for edit quadrant links (POC)
            let quadrant_edit_links = document.querySelectorAll("[data-identifier='quadrant_edit_links']");
            for(let x=0;x<quadrant_edit_links.length;x++){
                quadrant_edit_links[x].addEventListener("click",(event)=>{
                    window.open(`/configure/components?quadrant_id=${event.target.getAttribute("data-current-id")}#tab_1_selected`,"components")
                    event.preventDefault();
                })
            }

            // Add handlers for edit quadrant title links (POC)
            let quadrant_title_edit_links = document.querySelectorAll("[data-identifier='quadrant_title_edit_links']");
            for(let x=0;x<quadrant_title_edit_links.length;x++){
                quadrant_title_edit_links[x].addEventListener("click",(event)=>{
                    window.open(`/configure/components?quadrant_title_id=${event.target.getAttribute("data-current-id")}#tab_2_selected`,"components")
                    event.preventDefault();
                })
            }

            // add handlers for sector component title edit links:
            let sector_title_edit_links = document.querySelectorAll("[data-identifier='sector_title_edit_links']");
            for(let x=0;x<sector_title_edit_links.length;x++){
                sector_title_edit_links[x].addEventListener("click",(event)=>{
                    window.open(`/configure/components?sector_title_id=${event.target.getAttribute("data-current-id")}#tab_4_selected`,"components")
                    event.preventDefault();
                })
            }

            let rating_edit_links = document.querySelectorAll("[data-identifier='rating_edit_links']");
            for(let x=0;x<rating_edit_links.length;x++){
                rating_edit_links[x].addEventListener("click",(event)=>{
                    window.open(`/configure/components?rating_id=${event.target.getAttribute("data-current-id")}#tab_5_selected`,"components")
                    event.preventDefault();
                })
            }

            // and apply handler for submit button (accounts for add and update actio/compassns)
            let btn_submit_compass_data = document.getElementById("btn_submit_compass_data");
            if (btn_submit_compass_data) {
                btn_submit_compass_data.addEventListener("click", this.btnSubmitCompassData)
            }

            // add event listener to the ratings dropdowns, to handle onchange
            // to display the long descriptions from jinja loaded array:
            // why am I doing a querySelectorAll()???
            let dropdown_elems = document.querySelectorAll("[data-identifier='rating_dropdown']");
            for (let x = 0; x < dropdown_elems.length; x++) {
                let current_option_value = dropdown_elems[x].selectedIndex;   // initial value
                dropdown_elems[x].addEventListener("click", (e) => {
                    this.selectHandler(e, dropdown_elems, current_option_value, x, "rating");
                })
            }

            let dropdown_elems_sectors = document.querySelectorAll("[data-identifier='sector_dropdown']");
            for (let x = 0; x < dropdown_elems_sectors.length; x++) {
                let current_option_value = dropdown_elems_sectors[x].selectedIndex;   // initial value
                dropdown_elems_sectors[x].addEventListener("click", (e) => {
                    this.selectHandler(e, dropdown_elems_sectors, current_option_value, x, "sector");
                })
            }

            let dropdown_elems_quadrants = document.querySelectorAll("[data-identifier='quadrant_dropdown']");
            for (let x = 0; x < dropdown_elems_quadrants.length; x++) {
                let current_option_value = dropdown_elems_quadrants[x].selectedIndex;   // initial value
                dropdown_elems_quadrants[x].addEventListener("click", (e) => {
                    this.selectHandler(e, dropdown_elems_quadrants, current_option_value, x, "quadrant");
                })
            }

            // HOVER HANDLERS FOR DESCRIPTIONS:
            let ratings_descriptions = document.querySelectorAll("[data-identifier='rating_description'], [data-identifier='sector_description'], [data-identifier='quadrant_description']");
            for (let x = 0; x < ratings_descriptions.length; x++) {
                ratings_descriptions[x].addEventListener("mouseover", (e) => {
                    this.descriptionHoverHandler(e);
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
        // The dropdown elem ID:
        // I might need to convert the array of strings into an array of objects, to prevent ambiguity on submission of data to the API:
        "manage_quadrants_select": { "endpoint": "/compass/quadrant/", "data_elems": ["quadrant_id", "quadrant_summary", "quadrant_description"] },
        "manage_quadrant_titles_select": { "endpoint": "/compass/quadrants/title/", "data_elems": ["quadrant_title_id", "quadrant_title_part"] },
        "manage_sectors_select": { "endpoint": "/compass/sectors/", "data_elems": ["sector_id", "sector_summary", "sector_description"] },
        "manage_sector_titles_select": { "endpoint": "/compass/sectors/title/", "data_elems": ["sector_title_id", "sector_title_part"] },
        "manage_ratings_select": { "endpoint": "/compass/rating/", "data_elems": ["rating_id", "rating_title", "rating_description"] },
    },
    /**
     * Also if I return the new thing, I might be able to append to the exisitng dropdown rather than reloading the page///
     * Used by /configure page
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

        /** submit the new or update data */
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

    btnSubmitCompassData: function (evt) {
        // they are all dropdowns...
        let elems = document.getElementsByTagName("select");
        let compass_id = parseInt(document.getElementById("compass_id").value);
        let taskTypeString = "add";
        if (compass_id === NaN) {
            compass_id = null;
        }
        let compass_name = document.getElementById("compass_name").value;
        let compass_description = document.getElementById("compass_description").value;
        let data = {}
        for (let elem of elems) {
            let field = elem.getAttribute("data-fieldname");
            let value = elem.value;
            data[field] = parseInt(value);
        }
        data["id"] = compass_id;
        data["name"] = compass_name;
        data["description"] = compass_description;
        console.log(data);
        /** determine whether to add or update */
        let submitURL = '/compass/';    // the add endpoint (if POST)
        if (compass_id > 0) {
            taskTypeString = "update";
            submitURL = '/compass/update/';
        }
        if (data) {
            let api_response_code;
            let api_response_message;
            console.log(data);
            fetch(submitURL, {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            }).then(function (response) {
                // this is the response object:
                console.log(response)
                api_response_code = response.status;
                return response.json();
            }).then(function (response) {
                // and THIS is the JSON returned from the create endpoint:
                console.log(response);
                // console.log(evt.srcElement)
                /** TODO get better data in the response */
                // if (response.compass_updated) {
                if (response.id > 0) {
                    // becauise I am now returning a negative int on duplicated name - which is NOT a validation error
                    // I need to test for that here.
                    // document.location.href = `${document.location.hostname}?id=${response.id}`;
                    api_response_message = `Compass ${taskTypeString} successful.`;
                }else{
                    // Ideally I want to return APIResponseMessage for anything that does not return compass data, and check the
                    // `success` field
                    // TODO: alert the user that the update failed, and why. This will depend on the 
                    // back-end returning a better response object with error messages etc.
                    // let msg = JSON.parse(response.message)
                    // console.log(typeof(msg))
                    // here, `response` may be the dummy CompassSummary object with id=-1 and name="compass name already exists. Cannot add new compass definition."
                    // or may be actual error object with status_code, error, message etc. - depending on the back-end implementation.
                    // if(response.status_code || response.id < 0){
                    if(isAPIResponseMessage(response) || response.status_code || response.id < 0){
                        console.log(response.status_code);
                        console.log(response.error);
                        console.log(response.message);
                        api_response_code = response.status_code;
                        let x = JSON.stringify(response);
                        console.log(x);
                        let y = JSON.parse(x);
                        console.log(y);
                        api_response_message = response.message;
                        console.log(api_response_message);
                    }
                    if(response.id){
                        // if we get back the dummy CompassSummary, with ID=-1, we
                        // know that an error occurred. The only one atthe moment is
                        // checking for a duplicated compass name, so we need to set the
                        // error message to that, and that it FAILED. Because it doesn't
                        // create it...:
                        api_response_message = response.name;
                    }
                    console.log(api_response_message);
                }
                console.log(api_response_message);
                let msgBox = document.getElementById("message");
                let submitBtn = document.getElementById("btn_submit_compass_data");
                if(api_response_code !== 200 || response.id === -1){   
                    msgBox.innerText = `Save failed: ${api_response_message} (response code: ${api_response_code})`;
                    // msgBox.classList.remove("hidden");  
                }
                else{
                    msgBox.innerText = `Update succeeded: ${api_response_message} (response code: ${api_response_code})`;
                    // msgBox.classList.add("hidden"); 
                    // submitBtn.classList.add("disabled");
                    // submitBtn.setAttribute("disabled","");
                }
            });
        }
    },

    // handle configure tabber
    tabHandler: function (evt, tablist) {
        // we also need the list of panels to show/hide:
        let panel_list = document.querySelectorAll("[data-identifier='gutterpanel']");
        // let panel_list = document.getElementsByClassName("gutterpanel");
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

    /**
     * @param {*} evt - the DOM event ('click' etc.)
     * @param {*} selectlist - all possible selects for this type
     * @param {*} current_option_value - str, the text value
     * @param {*} current_dropdown_index - int, which of the possible items is it?
     * @param {*} prefix - str, determine type of dropdown (ENUM!!!) - sector or rating
     * Push the description of the selected thing into the corresponding DIV. Depends HEAVILY
     * on the correct DOM structure!!
     * OK... I render the list of descriptions in a named list of DOM elements (hidden) and
     * when a rating or sector is selected, the title is shown in the dropdown, but we need
     * to get the descriprion for the one we select from the hidden list of DOM elements that 
     * contain the descriptions for ALL the ratings or sectors that have been defined.
     * The specifics of the DOM element attributes allow identification and mapping of the
     * thing to its corresponding description. Trust me, it makes sense...
     * Used by /configure page:
     */
    selectHandler: function (evt, selectlist, current_option_value, current_dropdown_index, prefix) {
        // let id = selectlist[current_dropdown_index].id;
        // console.log(evt)
        // console.log(`${selectlist[current_dropdown_index].id}_description_changed`);
        // document.getElementById(`${selectlist[current_dropdown_index].id}_description_changed`).innerText = "";
        document.getElementById(`${selectlist[current_dropdown_index].id}_description`).getElementsByTagName("span")[0].classList.remove("changed");
        if (current_option_value !== selectlist[current_dropdown_index].selectedIndex) {
            document.getElementById(`${selectlist[current_dropdown_index].id}_description`).getElementsByTagName("span")[0].classList.add("changed");
            // document.getElementById(`${selectlist[current_dropdown_index].id}_description_changed`).innerText = "*"
        }
        // apply description to display DIV:
        document.getElementById(`${selectlist[current_dropdown_index].id}_description`).getElementsByTagName("span")[0].innerText = document.getElementById(`${prefix}_description_${selectlist[current_dropdown_index].selectedIndex + 1}`).innerText;
        // and apply the title attribute to the dropdown itself, so the user can hover and see the description:
        // console.log(`${prefix}_description_${selectlist[current_dropdown_index].selectedIndex + 1}`);
        // console.log(document.getElementById(`${prefix}_description_${selectlist[current_dropdown_index].selectedIndex + 1}`))
        selectlist[current_dropdown_index].setAttribute("title", document.getElementById(`${prefix}_description_${selectlist[current_dropdown_index].selectedIndex + 1}`).innerText);
    },

    descriptionHoverHandler: function (evt) {
        // console.log(evt.srcElement );
        evt.srcElement.setAttribute("title", evt.srcElement.innerText);
    },
};

// This may not need to be loaded ALWAYS, or for every page. JUST the data display page
// and homepage? - i.e. the compass itself.
// We DO need to call the API endpoint related to the current user's compass though, so thet
// see the correct titles etc.
// I can get the URL positional variable for the compass from the data-attribute on the page
// but ideally this should be done with a user session variable. User management and auth 
// has not yet been addressed... A BIG TODO:!
document.addEventListener("DOMContentLoaded",
    (evt) => {
        engine.init(); 
    }
)
