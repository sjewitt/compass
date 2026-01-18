var compass_rating;
(function (compass_rating) {
    compass_rating[compass_rating["UNFAMILIAR"] = 1] = "UNFAMILIAR";
    compass_rating[compass_rating["NOVICE"] = 2] = "NOVICE";
    compass_rating[compass_rating["FOUNDATION"] = 3] = "FOUNDATION";
    compass_rating[compass_rating["COMPETENT"] = 4] = "COMPETENT";
    compass_rating[compass_rating["ADVANCED"] = 5] = "ADVANCED";
    compass_rating[compass_rating["MASTER"] = 6] = "MASTER";
})(compass_rating || (compass_rating = {}));

var engine = {
    /**
     * These properties are loaded from the fetch just prior to the call
     * to `init();`. The idea is to allow configurable data for both front-
     * and back-end data.
     * 
     * #47
     * Jan 2026: Adds configurable displayed texts titles - requires blank compass image 
     *  - each element of the title_parts is pushed to a corresponding SVG text element.
     *  - the target is worked out by mapping the indexes to each appropriately structured
     *    element ID.
     */
    rating_description_lookup:null,
    data_quadrant_titles: null,
    data_0:null,
    data_1:null,
    data_2: null,
    elems: [
        'q-1',
        's1-t',
        's1-1', 's1-2', 's1-3', 's1-4', 's1-5', 's1-6',
        's2-t',
        's2-1', 's2-2', 's2-3', 's2-4', 's2-5', 's2-6',
        's3-t',
        's3-1', 's3-2', 's3-3', 's3-4', 's3-5', 's3-6',
        's4-t',
        's4-1', 's4-2', 's4-3', 's4-4', 's4-5', 's4-6',
        's5-t',
        's5-1', 's5-2', 's5-3', 's5-4', 's5-5', 's5-6',
        'q-2',
        's6-t',
        's6-1', 's6-2', 's6-3', 's6-4', 's6-5', 's6-6',
        's7-t',
        's7-1', 's7-2', 's7-3', 's7-4', 's7-5', 's7-6',
        's8-t',
        's8-1', 's8-2', 's8-3', 's8-4', 's8-5', 's8-6',
        's9-t',
        's9-1', 's9-2', 's9-3', 's9-4', 's9-5', 's9-6',
        'q-3',
        's10-t',
        's10-1', 's10-2', 's10-3', 's10-4', 's10-5', 's10-6',
        's11-t',
        's11-1', 's11-2', 's11-3', 's11-4', 's11-5', 's11-6',
        's12-t',
        's12-1', 's12-2', 's12-3', 's12-4', 's12-5', 's12-6',
        's13-t',
        's13-1', 's13-2', 's13-3', 's13-4', 's13-5', 's13-6',
        'q-4',
        's14-t',
        's14-1', 's14-2', 's14-3', 's14-4', 's14-5', 's14-6',
        's15-t',
        's15-1', 's15-2', 's15-3', 's15-4', 's15-5', 's15-6',
        's16-t',
        's16-1', 's16-2', 's16-3', 's16-4', 's16-5', 's16-6',
        's17-t',
        's17-1', 's17-2', 's17-3', 's17-4', 's17-5', 's17-6'
    ],
    current_quad: -1,
    current_sector: -1,
    current_score: -1,
    current_rating: -1,
    current_data: [],

    // pass in loaded data here 
    init: function (display_data) {
        // and set the properties of the object from the loaded data:
        this.data_quadrant_titles = display_data.data_quadrant_titles;
        this.rating_description_lookup = display_data.rating_description_lookup;
        this.data_0 = display_data.data_0;
        this.data_1 = display_data.data_1;
        this.data_2 = display_data.data_2;
        console.log();
        var page = document.getElementsByTagName('body')[0].getAttribute('data-page');
        for (var _i = 0, _a = this.elems; _i < _a.length; _i++) {
            var id = _a[_i];
            var elem = document.getElementById(id);
            if (elem) {
                elem.addEventListener('mouseover', this.test_in);
                elem.addEventListener('mouseout', this.test_out);
                elem.addEventListener('click', this.test_handler);
            }
        };

        if(page==="add_user"){
            // append listener to add button:
            let btn_add_user = document.getElementById("btn_add_user");
            if(btn_add_user){
                btn_add_user.addEventListener("click",this.submitNewUserDataHandler)
            }
        };

        if(page==="update_user"){
            let btn_update_user = document.getElementById("btn_update_user");
            if(btn_update_user){
                btn_update_user.addEventListener("click",this.submitUpdateUserDataHandler)
            }
        };

        if (page === 'svg') {
            
            this.loadAndBuildUserDropdown();
        }

        /**  
         * load the dropdown with selecting and jumping to specific user page
         * */
        if(page === "home"){
            this.getStaticSectorTitlesDOM();
            this.renderDisplayedTexts();
            this.loadAndBuildUserDropdown();
        }
        
        if (page === "svg_template"){
            this.getStaticSectorTitlesDOM();

            /** render the static quadrant and sector texts */
            this.renderDisplayedTexts();

            /**  directly call the user load function:  */
            engine.loadUser();

            /** append handler to data download button */
            let btn_data_download = document.getElementById("data_download");
            if(btn_data_download){
                btn_data_download.addEventListener("click",this.retrieveUserData)
            }
        }

        /** add event listener for the user dropdown: */
        var user_dropdown_btn = document.getElementById("select_user_button");
        var user_dropdown = document.getElementById("select_user");

        if(user_dropdown_btn){
            user_dropdown_btn.addEventListener("click",() => {engine.selectAndLoadUser()});
        }
        if(user_dropdown){
            if(page==="home"){
                user_dropdown.addEventListener("change",() => {engine.redirectToUserTemplate()});
            }
            if(page="svg"){
                user_dropdown.addEventListener("change",() => {engine.selectAndLoadUser()});
            }
        }
    },

    buildOptionElem: function(header, userName, userId){
        let _elem = document.createElement('option');
        let _txt, _attr;
        if(header){
            _txt = document.createTextNode('-- Select yourself --')
            _attr = -1;
        }
        else{
            _txt = document.createTextNode(userName)
            _attr = userId;
        }
        _elem.setAttribute("value",_attr)
        _elem.appendChild(_txt)
        return(_elem);
    },

    loadAndBuildUserDropdown: function(){
        console.log("load users and build the dropdown:")
               fetch(`/users/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }).then(function (response) {
             return response.json(); 
        }).then(function (response) { 
            console.log(response);
            let targetElem = document.getElementById("select_user");

            /**  
             * Now iterate over users, create <option> elements and append to dropdown   
             * https://stackoverflow.com/questions/3955229/remove-all-child-elements-of-a-dom-node-in-javascript
             *  - and the argument rages on...
            */
            targetElem.innerHTML = "";
            targetElem.appendChild(engine.buildOptionElem(true,null,null));
            for(let x=0;x<response.length;x++){

                targetElem.appendChild(engine.buildOptionElem(false,response[x].username,response[x].id));
            }
        });
    },

    /** 
     * Generate DOM for static quadrant and sector compass titles. We don't want to duplicate hardcoded
     * HTML in > 1 template
     */
    getStaticSectorTitlesDOM: function(){
        // This is why it did not display:
        // https://stackoverflow.com/questions/23588384/dynamically-created-svg-element-not-displaying

        let _render_titles = document.getElementById("static_titles");
        _render_titles.innerHTML = "";

        // iterate over quadrants:
        for(let qt=0;qt<this.data_quadrant_titles.length;qt++){
            let _polygon = document.createElementNS("http://www.w3.org/2000/svg",'polygon');
            _polygon.setAttribute("class",`svg_title ${this.data_quadrant_titles[qt].class}`);
            _polygon.setAttribute("points",this.data_quadrant_titles[qt].points);

            // and append to the wrapper:
            _render_titles.appendChild(_polygon);
            
            // iterate over these lines of text, to generate a <text> element
            for(let qtp=0;qtp<this.data_quadrant_titles[qt].title_parts.length;qtp++){
                let _title = document.createElementNS("http://www.w3.org/2000/svg",'text');
                _title.setAttribute('id',`svg_title_${qt+1}_${qtp+1}`);
                _title.setAttribute('class',`svg_quad_title ${this.data_quadrant_titles[qt].class}`);
                _title.setAttribute('font-size','24');
                _title.setAttribute('x',this.data_quadrant_titles[qt].title_parts[qtp].coords[0]);
                _title.setAttribute('y',this.data_quadrant_titles[qt].title_parts[qtp].coords[1]);

                // and append to the wrapper:
                _render_titles.appendChild(_title);
            }

            // and for each quadrant, generate the sector titles:
            for(let stp=0;stp<this.data_quadrant_titles[qt].sector_parts.length;stp++){
                let sector_title_array = this.data_quadrant_titles[qt].sector_parts[stp];

                // and for each of these, generate a <text> element:
                for(let xx=0;xx<sector_title_array.length;xx++){

                    let _sector_title = document.createElementNS("http://www.w3.org/2000/svg",'text');
                    _sector_title.setAttribute('id',`svg_sector_${qt+1}_${stp+1}_${xx+1}`);
                    _sector_title.setAttribute('font-size','14');
                    _sector_title.setAttribute('font-family','times');
                    _sector_title.setAttribute('x',sector_title_array[xx].coords[0]);
                    _sector_title.setAttribute('y',sector_title_array[xx].coords[1]);
                    _render_titles.appendChild(_sector_title);
                }
            }
        }
        console.log(_render_titles);
    },

    renderDisplayedTexts: function(){
        // render texts that show always, rather than having static texts as part
        // of the image itself. also, find a way
        // of using the same image for /static and /templates.
        // This function assumes presence of DOM generated by above function.
        const quadrant_title_refs = [];
 
        // I'm using index 1 because of the way the element IDs are named.
        for(let x=1;x<=this.data_quadrant_titles.length;x++){
            // get the array of words for the current title elems:
            let current_words = this.data_quadrant_titles[x-1];

            // identify the text elements by ID:
            for(let y=1;y<=current_words.title_parts.length;y++){
                let elem_id = `svg_title_${x}_${y}`;
                try{
                    let elem = document.getElementById(elem_id);
                    let txt = document.createTextNode(current_words.title_parts[y-1].title);
                    elem.appendChild(txt);
                }
                catch(ex){
                    console.log(`Cannot process quadrant title parts: ${ex}`);
                }
            }

            // now get the segment titles: we do a double loop to get each segment, and the lines array for each:
            for(let z=1;z<=current_words.sector_parts.length;z++){
                for(let xx=1;xx<=current_words.sector_parts[z-1].length;xx++){
                    let elem_id = `svg_sector_${x}_${z}_${xx}`;
                    try{
                        let elem = document.getElementById(elem_id);
                        let txt = document.createTextNode(current_words.sector_parts[z-1][xx-1].title);
                        elem.appendChild(txt);
                    }
                    catch(ex){
                        console.log(`Cannot process segment title parts: ${ex}`);
                    }
                }
            }
        }
    },

    redirectToUserPage: function(){
        // TODO:
    },

    submitNewUserDataHandler: function(){
        let submit = true;
        data={}
        data['username'] = document.getElementById("new_user_login").value;
        data['name'] = document.getElementById("new_user_name").value;
        data['email'] = document.getElementById("new_user_email").value;
        data['password'] = document.getElementById("new_user_pwd").value;
        data['password_check'] = document.getElementById("new_user_pwd_repeat").value;
        console.log(data);
        if(data["password"] !== data["password_check"]){    // also checks on server
            submit = false;
        }
        // TODO: Do blur/change handlers and alert in real-time 
        if(submit){
            fetch('/users/new/', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            }).then(function (response) {
                return response.json(); 
                }).then(function (response) { 
                /** the ResponseRedirect from the server is failing, so
                 * try with JS instead:
                 */
                if(response.usercreated){
                    document.location.href=`/static/?user_id=${response.user_id}`
                }
            });
        }
    },

    submitUpdateUserDataHandler: function(){
        let submit = true;
        data={}
        data['username'] = document.getElementById("update_user_login").value;
        data['id'] = parseInt(document.getElementById("update_user_id").value);
        data['name'] = document.getElementById("update_user_name").value;
        data['email'] = document.getElementById("update_user_email").value;

        /** 
         * check if pwds are present, then are the same, then match existing pwd 
         * This needs to call a back-end check so we don't have the old pwd on
         * client...
        */
        // if(data["password"] !== data["password_check"]){    // also checks on server
        //     submit = false;
        // }
        // TODO: Do blur/change handlers and alert in real-time 
        if(submit){
            fetch(`/users/${data['id']}/edit/`, {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            }).then(function (response) {
                return response.json(); 
            }).then(function (response) { 
                /** the ResponseRedirect from the server is failing, so
                 * try with JS instead:
                 */
                if(response.username){  // check that it is a User object
                    document.location.href=`/${response.id}/`
                }
                else{
                    // render a message - wrong user ID etc
                    elem = document.getElementById("message")
                    elem.innerHTML = "Error"
                }
            });
        }
    },

    /** this is OLD, and not specific to a user */
    export_data: function () {
        var _out = [['quadrant', 'sector', 'rating']];
        for (var x = 0; x < engine.current_data.length; x++) {
            _out.push([engine.current_data[x].key[0], engine.current_data[x].key[1], engine.current_data[x].rating]);
        }
        var _return = "data:text/csv;charset=utf-8,";
        _out.forEach(function (arr) {
            _return += arr.join(",") + "\r\n";
        });
        var encodedUri = encodeURI(_return);
        var link = document.getElementById("download_hidden_link");
        if (link) {
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "compass.csv");
            link.click();
        }
    },

    retrieveUserData: function(){
        console.log(this.getAttribute('data-user-id').split(":")[1]);
        let user_id = this.getAttribute('data-user-id').split(":")[1];
        /** now call API endpoint: */
        fetch(`/${user_id}/data/`, {
                method: 'GET',
                // body: JSON.stringify(data),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                   // 'Content-Disposition': 'attachment',
                },
            }).then(function (response) {
                return response.json(); 
                }).then(function (response) { 
                console.log(response);
                /** the ResponseRedirect from the server is failing, so
                 * try with JS instead:
                 */
                if(response.usercreated){
                    document.location.href=`/static/?user_id=${response.user_id}`
                }
            });
    },

    test_load_data: function (user_id=0) {
        /** first, clear the current data */
        // https://developer.mozilla.org/en-US/docs/Web/API/NodeList
        var svg_compass = Array.from(document.getElementById("svg_compass").childNodes);
        for(let _x=0;_x<svg_compass.length; _x++){
            if(svg_compass[_x].tagName === "polygon"){
                /** ignore outer titles, because removing style from this causes an error */
                if(!svg_compass[_x].classList.contains("svg_title"))
                {
                    svg_compass[_x].classList.remove('svg_clicked');
                    svg_compass[_x].classList.remove('svg_show');
                }
            }
        }

        /** 
         * here, we get the ID of the selected User, and this is re-triggered
         * by the OK button...
         */

        /** get userdata from fastapi backend: */
        fetch(`/users/${user_id}/competencies/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }).then(function (response) {
             return response.json(); 
        }).then(function (response) { 
            currentData = [];
            for(let a=0;a<response.length;a++){
                currentData.push({
                    "key":[response[a].quadrant, response[a].sector,response[a].sector],
                    "rating":response[a].rating})
            }
            if (currentData) {
                var data = currentData;
                for (var a = 0; a < data.length; a++) {
                    if (engine.isQuadrant(data[a])) {
                        engine.addToUserdata(data[a].key, data[a].rating);
                        var elem = document.querySelector('[data-lookup="[' + data[a].key + ']"][data-rating="' + data[a].rating + '"]');
                        if (elem) {
                            elem.click();
                        }
                    }
                }
            }
        });
    },
    
    isQuadrant: function (data) {
        return data.rating >= 0 && data.rating <= 6;
    },
    
    test_handler: function (event) {
        if (this.current_score > -1) {
            engine.addToUserdata([this.current_quad, this.current_sector, this.current_score], this.current_rating);
            this.setAttribute('class', 'clicked');
        }
        engine.setSectorSVGClicked(this);
        event.preventDefault();
    },

    test_in: function () {
        var self = document.getElementById(this.getAttribute('id'));
        if (self) {
            engine.setSectorSVGDisplay(self, true);
            var sector_rating = -1;
            var lookup = JSON.parse(this.getAttribute('data-lookup'));
            this.current_quad = lookup[0];
            this.current_sector = lookup[1];
            this.current_score = lookup[2];
            var quad_description = "";
            var quad_title = "";
            var sector_title = "";
            if (lookup[0] > -1) {
                quad_description = engine.data_0[lookup[0]].description;
                quad_title = engine.data_0[lookup[0]].title;
            }
            var sector_title_description = '';
            if (lookup[1] > -1) {
                sector_title_description = engine.data_1[lookup[0]][lookup[1]].description;
                sector_title = engine.data_1[lookup[0]][lookup[1]].title;
            }
            var sector_block_description = '';
            if (lookup[2] > -1) {
                sector_title = engine.data_1[lookup[0]][lookup[1]].title;
                sector_rating = parseInt(this.getAttribute('data-rating'));
                this.current_rating = sector_rating;
                sector_block_description = engine.data_2[lookup[0]][lookup[2]];
            }
            var output_rating = '';
            if (sector_rating > -1) {
                output_rating = engine.rating_description_lookup[sector_rating].title;
            }
            var elem_quad_title = document.getElementById('quad_title');
            var elem_quad_description = document.getElementById('quad_description');
            var elem_sector_title = document.getElementById('sector_title');
            var elem_sector_title_description = document.getElementById('sector_title_description');
            var elem_block_description = document.getElementById('sector_block_description');
            var elem_rating = document.getElementById('rating');
            if (elem_quad_title)
                elem_quad_title.innerText = quad_title;
            if (elem_quad_description)
                elem_quad_description.innerText = quad_description;
            if (elem_sector_title)
                elem_sector_title.innerText = sector_title;
            if (elem_sector_title_description)
                elem_sector_title_description.innerText = sector_title_description;
            if (elem_block_description)
                elem_block_description.innerText = sector_block_description;
            if (elem_rating)
                elem_rating.innerText = output_rating;
            var elem_title = [];
            if (quad_title && lookup[2] === -1)
                elem_title.push(quad_title);
            if (quad_description && lookup[2] === -1)
                elem_title.push(quad_description);
            if (sector_title && lookup[2] === -1)
                elem_title.push(sector_title);
            if (sector_title_description && lookup[2] !== -1)
                elem_title.push(sector_title_description);
            if (sector_block_description && lookup[2] !== -1)
                elem_title.push(sector_block_description);
            self.setAttribute('title', elem_title.join('\n\n'));
        }
    },

    test_out: function () {
        var self = document.getElementById(this.getAttribute('id'));
        if (self) {
            engine.setSectorSVGDisplay(self, false);
            var _rating = document.getElementById('rating');
            if (_rating) {
                _rating.innerText = "";
            }
        }
    },
    
    /** for template, simplify the function */
    loadUser: function(){
        let selected_user = document.getElementById("select_user").value;
        engine.test_load_data(selected_user);
    },
    
    selectAndLoadUser: function(){
        var page = document.getElementsByTagName('body')[0].getAttribute('data-page');
        let selected_user = document.getElementById("select_user").value;

        /**  here we can loca the profile for the selected user:  */
        if (page === 'svg') {
            engine.test_load_data(selected_user);
            var export_data_elem = document.getElementById('flyout').firstChild;
            if (export_data_elem) {
                export_data_elem.addEventListener('click', this.export_data);
            }
        }
    },

    redirectToUserTemplate: function(){
        let selected_user = document.getElementById("select_user").value;
        console.log(selected_user)
        if(parseInt(selected_user) > 0){
            document.location.href = `/${selected_user}`;
        }
    },
    
    addToUserdata: function (lookup, rating) {
        /**  here we add the data to the database rather than localstorage. Therefore, this also 
         * needs to have an async promise handler: */
        /** get the ID of the user from the dropdown */
        let user_id = document.getElementById("select_user").value;
        data = {
            "user_id": user_id,
            "quadrant": lookup[0],
            "sector": lookup[1],
            "rating": rating,
        }

        fetch('/competencies/add/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }).then(function (response) {
             return response.json(); 
        }).then(function (response) { 
        
        });

        var append = true;
        for (var a = 0; a < engine.current_data.length; a++) {
            if (engine.current_data[a].key[0] === lookup[0] 
                    && engine.current_data[a].key[1] === lookup[1] 
                    && engine.current_data[a].key[2] === lookup[2])
                {
                append = false;
                engine.current_data[a].rating = rating;
            };
        }
        if (append) {
            engine.current_data.push({ 'key': lookup, 'rating': rating });
        }
        this.renderRatings();
    },
    
    setSectorSVGClicked: function (elem) {
        var id_prefix = elem.getAttribute('id').split('-')[0];
        var max_id = parseInt(elem.getAttribute('id').split('-')[1]);
        for (var a = 1; a <= 6; a++) {
            document.getElementById('svg_' + id_prefix + '-' + a).classList.remove('svg_clicked');
            document.getElementById('svg_' + id_prefix + '-' + a).classList.remove('svg_show');
        }
        for (var x = 1; x <= max_id; x++) {
            document.getElementById('svg_' + id_prefix + '-' + x).classList.add('svg_clicked');
            document.getElementById('svg_' + id_prefix + '-' + x).classList.add('svg_show');
        }
    },
    
    setSectorSVGDisplay: function (elem, show) {
        var id_prefix = elem.getAttribute('id').split('-')[0];
        var max_id = parseInt(elem.getAttribute('id').split('-')[1]);
        for (var x = 1; x <= max_id; x++) {
            var elem_1 = document.getElementById('svg_' + id_prefix + '-' + x);
            if (elem_1) {
                if (show) {
                    elem_1.classList.add('svg_hover');
                }
                else {
                    elem_1.classList.remove('svg_hover');
                }
            }
        }
    },
    
    renderRatings: function () {
        var target = document.getElementById('userdata');
        target.innerText = "";
        engine.current_data.sort(function (a, b) {
            if (a.key[0] > b.key[0]) {
                return (1);
            }
            else {
                return (-1);
            }
        });
        for (var a = 0; a < engine.current_data.length; a++) {
            var row = document.createElement('div');
            row.appendChild(document.createTextNode(engine.data_0[engine.current_data[a].key[0]].title
                + ', '
                + engine.data_1[engine.current_data[a].key[0]][engine.current_data[a].key[1]].title
                + ': '
                + engine.rating_description_lookup[engine.current_data[a].rating].title
                + ' (' + engine.rating_description_lookup[engine.current_data[a].rating].description + ')'));
            target.appendChild(row);
        }
    },
    
    fish: function () {
        var fish = 1255;
        return (fish);
    }
};

document.addEventListener("DOMContentLoaded",
    (evt) => {
        // load data then call init:
        // https://www.geeksforgeeks.org/javascript/read-json-file-using-javascript/
        function fetchJSONData() {
            console.log('loading data...'); 
            fetch('../static/data/display_data.json')
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();  
                })
                .then(display_data => {
                    // apply data as required:
                    engine.init(display_data);  // put this into callback
                })  
                .catch(error => console.error('Failed to fetch data:', error)); 
        }
        fetchJSONData(); 
        // 
    }
)
