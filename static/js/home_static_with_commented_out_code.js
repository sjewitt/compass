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

    API_URL: "/compass/1/", 

    // This is the coordiate lookup for the title positions:
    CONSTANTS_URL: "/static/data/compass_titles.json",
    // rating_description_lookup:null,
    coordinate_lookup: null,
    data_quadrant: null,

    // pass in loaded data here 
    // I need to decouple `display_data` from the quadrant SVG definition
    init: function (display_data) {
        console.log("homepage javascript file")
        // this originates from the database:
        console.log(display_data);
        // and set the properties of the object from the loaded data:
        this.data_quadrants = display_data.data_quadrants;
        // this.rating_description_lookup = display_data.rating_description_lookup;
        // this is the function that draws the skewed boxes:
        this.getStaticSectorTitlesDOM();

        // and THIS is the function that renders the texts:
        // So this needs to be replaced with something else
        // this.renderDisplayedTexts();

        this.loadAndBuildUserDropdown();
        var user_dropdown = document.getElementById("select_user");

        if(user_dropdown){
            user_dropdown.addEventListener("change",() => {engine.redirectToUserTemplate()});
        }
    },

    /** 
     * Generate DOM for static quadrant and sector compass titles. We don't want to duplicate hardcoded
     * HTML in > 1 template
     */
    getStaticSectorTitlesDOM: function(){

        // this is the elem in the page:
        let _render_titles = document.getElementById("static_titles");
        _render_titles.innerHTML = "";

        // iterate over quadrants:
        for(let qt=0;qt<this.data_quadrants.length;qt++){
            let _polygon = document.createElementNS("http://www.w3.org/2000/svg",'polygon');
            _polygon.setAttribute("class",`svg_title svg_quadrant_${qt+1}`);
            _polygon.setAttribute("points",engine.coordinate_lookup.quadrants[qt].points);

            // and append to the wrapper:
            _render_titles.appendChild(_polygon);
            
            for(let qtp=0;qtp<this.data_quadrants[qt].title.length;qtp++){
                let _title = document.createElementNS("http://www.w3.org/2000/svg",'text');
                _title.setAttribute('id',`svg_title_${qt+1}_${qtp+1}`);
                _title.setAttribute('class',`svg_quad_title svg_quadrant_${qt+1}`);
                _title.setAttribute('font-size','24');
                
                console.log(engine.coordinate_lookup.quadrants[qt].title, qt, qtp);
                _title.setAttribute('x',engine.coordinate_lookup.quadrants[qt].title[qtp].coords[0]);
                _title.setAttribute('y',engine.coordinate_lookup.quadrants[qt].title[qtp].coords[1]);
                
                // and append to the wrapper:
                _render_titles.appendChild(_title);
            }

            // and for each quadrant, generate the sector titles:
            for(let stp=0;stp<this.data_quadrants[qt].sectors.length;stp++){
                let sector_title_array = this.data_quadrants[qt].sectors[stp].title;
                // and for each of these, generate a <text> element:
                for(let xx=0;xx<sector_title_array.length;xx++){

                    let _sector_title = document.createElementNS("http://www.w3.org/2000/svg",'text');
                    _sector_title.setAttribute('id',`svg_sector_${qt+1}_${stp+1}_${xx+1}`);
                    _sector_title.setAttribute('font-size','14');

                    // DATABASE DATA
                    // with static lookups:
                    _sector_title.setAttribute('x',engine.coordinate_lookup.quadrants[qt].sectors[stp][xx].coords[0]);
                    _sector_title.setAttribute('y',engine.coordinate_lookup.quadrants[qt].sectors[stp][xx].coords[1]);
                    _render_titles.appendChild(_sector_title);
                }
            }
        }
    },

    loadConstantData: function(data){
        console.log(data);
        engine.coordinate_lookup = data;
    },

    // // populate data for routes that require it from JSON data file:
    // populateCompassImageData: function(){

    // },

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
        fetch(`/users/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }).then(function (response) {
             return response.json(); 
        }).then(function (response) { 
            let targetElem = document.getElementById("select_user");

            /**  
             * Now iterate over users, create <option> elements and append to dropdown   
             * https://stackoverflow.com/questions/3955229/remove-all-child-elements-of-a-dom-node-in-javascript
             *  - and the argument rages on...
            */
            targetElem.innerHTML = "";
            targetElem.appendChild(engine.buildOptionElem(true,null,null));
            for(let x=0;x<response.length;x++){
                targetElem.appendChild(engine.buildOptionElem(false,response[x].name,response[x].id));
            }
        });
    },


    // TODO: This needs replacing with the same logic, but with static homepage titles (e.g.):
    // renderDisplayedTexts: function(){
    //     // render texts that show always, rather than having static texts as part
    //     // of the image itself. also, find a way
    //     // of using the same image for /static and /templates.
    //     // This function assumes presence of DOM generated by above function.
 
    //     // I'm using index 1 because of the way the element IDs are named.
    //     for(let x=1;x<=this.data_quadrants.length;x++){
    //         // get the array of words for the current title elems:
    //          let current_words = this.data_quadrants[x-1];

    //         // identify the text elements by ID:
    //         // for(let y=1;y<=current_words.title_parts.length;y++){
    //         for(let y=1;y<=current_words.title.length;y++){
    //             let elem_id = `svg_title_${x}_${y}`;
    //             try{
    //                 let elem = document.getElementById(elem_id);
    //                 // static data:
    //                 // let txt = document.createTextNode(current_words.title_parts[y-1].title);

    //                 // database data:
    //                 let txt = document.createTextNode(current_words.title[y-1].title_part);
    //                 elem.appendChild(txt);
    //             }
    //             catch(ex){
    //                 console.log(`Cannot process quadrant title parts: ${ex}`);
    //             }
    //         }

    //         // now get the segment titles: we do a double loop to get each segment, and the lines array for each:
    //         for(let z=1;z<=current_words.sectors.length;z++){
    //             // console.log(`ln 306 `)
    //             console.log(current_words.sectors);
    //             console.log(x,z)
    //             console.log(z-1)
    //             console.log(current_words.sectors[z-1].title.length)
    //             for(let xx=1;xx<=current_words.sectors[z-1].title.length;xx++){
    //                 console.log(xx)
    //                 let elem_id = `svg_sector_${x}_${z}_${xx}`;
    //                 console.log(elem_id);
    //                 try{
    //                     let elem = document.getElementById(elem_id);
    //                     console.log(elem);
    //                     console.log(current_words.sectors[z-1].title);
    //                     let txt = document.createTextNode(current_words.sectors[z-1].title[xx-1].title_part);
    //                     elem.appendChild(txt);
    //                 }
    //                 catch(ex){
    //                     console.log(`Cannot process segment title parts: ${ex}`);
    //                 }
    //             }
    //         }
    //     }
    // },

    // redirectToUserPage: function(){
    //     // TODO:
    // },

    // submitNewUserDataHandler: function(){
    //     let submit = true;
    //     data={}
    //     data['username'] = document.getElementById("new_user_login").value;
    //     data['compass_id'] = document.getElementById("compass_id").value;
    //     data['name'] = document.getElementById("new_user_name").value;
    //     data['email'] = document.getElementById("new_user_email").value;
    //     data['password'] = document.getElementById("new_user_pwd").value;
    //     data['password_check'] = document.getElementById("new_user_pwd_repeat").value;
    //     if(data["password"] !== data["password_check"]){    // also checks on server
    //         submit = false;
    //     }
    //     console.table(data);
    //     // TODO: Do blur/change handlers and alert in real-time 
    //     if(submit){
    //         fetch('/users/new/', {
    //             method: 'POST',
    //             body: JSON.stringify(data),
    //             headers: {
    //                 'Accept': 'application/json',
    //                 'Content-Type': 'application/json'
    //             },
    //         }).then(function (response) {
    //             return response.json(); 
    //             }).then(function (response) { 
    //             /** the ResponseRedirect from the server is failing, so
    //              * try with JS instead:
    //              */
    //             if(response.usercreated){
    //                 document.location.href=`/static/?user_id=${response.user_id}`
    //             }
    //         });
    //     }
    // },

    // submitUpdateUserDataHandler: function(){
    //     console.log(document.getElementById("compass_id"));
    //     let submit = true;
    //     data={}
    //     data['username'] = document.getElementById("update_user_login").value;
    //     data['id'] = parseInt(document.getElementById("update_user_id").value);
    //     data['compass_id'] = parseInt(document.getElementById("compass_id").value);
    //     data['name'] = document.getElementById("update_user_name").value;
    //     data['email'] = document.getElementById("update_user_email").value;
    //     console.log(data);
    //     /** 
    //      * TODO: check if pwds are present, then are the same, then match existing pwd 
    //      * This needs to call a back-end check so we don't have the old pwd on
    //      * client...
    //     */
    //     // if(data["password"] !== data["password_check"]){    // also checks on server
    //     //     submit = false;
    //     // }
    //     // TODO: Do blur/change handlers and alert in real-time 
    //     if(submit){
    //         fetch(`/users/${data['id']}/edit/`, {
    //             method: 'POST',
    //             body: JSON.stringify(data),
    //             headers: {
    //                 'Accept': 'application/json',
    //                 'Content-Type': 'application/json'
    //             },
    //         }).then(function (response) {
    //             return response.json(); 
    //         }).then(function (response) { 
    //             /** the ResponseRedirect from the server is failing, so
    //              * try with JS instead:
    //              */
    //             if(response.username){  // check that it is a User object
    //                 document.location.href=`/${response.id}/`
    //             }
    //             else{
    //                 // render a message - wrong user ID etc
    //                 elem = document.getElementById("message")
    //                 elem.innerHTML = "Error"
    //             }
    //         });
    //     }
    // },

    // /** this is OLD, and not specific to a user */
    // export_data: function () {
    //     var _out = [['quadrant', 'sector', 'rating']];
    //     for (var x = 0; x < engine.current_data.length; x++) {
    //         _out.push([engine.current_data[x].key[0], engine.current_data[x].key[1], engine.current_data[x].rating]);
    //     }
    //     var _return = "data:text/csv;charset=utf-8,";
    //     _out.forEach(function (arr) {
    //         _return += arr.join(",") + "\r\n";
    //     });
    //     var encodedUri = encodeURI(_return);
    //     var link = document.getElementById("download_hidden_link");
    //     if (link) {
    //         link.setAttribute("href", encodedUri);
    //         link.setAttribute("download", "compass.csv");
    //         link.click();
    //     }
    // },

    // retrieveUserData: function(){
    //     let user_id = this.getAttribute('data-user-id').split(":")[1];
    //     /** now call API endpoint: */
    //     fetch(`/${user_id}/data/`, {
    //             method: 'GET',
    //             headers: {
    //                 'Accept': 'application/json',
    //                 'Content-Type': 'application/json',
    //                // 'Content-Disposition': 'attachment',
    //             },
    //         }).then(function (response) {
    //             return response.json(); 
    //             }).then(function (response) { 
    //             /** the ResponseRedirect from the server is failing, so
    //              * try with JS instead:
    //              */
    //             if(response.usercreated){
    //                 document.location.href=`/static/?user_id=${response.user_id}`
    //             }
    //         });
    // },

    // test_load_data: function (user_id=0) {
    //     /** first, clear the current data */
    //     // https://developer.mozilla.org/en-US/docs/Web/API/NodeList
    //     var svg_compass = Array.from(document.getElementById("svg_compass").childNodes);
    //     for(let _x=0;_x<svg_compass.length; _x++){
    //         if(svg_compass[_x].tagName === "polygon"){
    //             /** ignore outer titles, because removing style from this causes an error */
    //             if(!svg_compass[_x].classList.contains("svg_title"))
    //             {
    //                 svg_compass[_x].classList.remove('svg_clicked');
    //                 svg_compass[_x].classList.remove('svg_show');
    //             }
    //         }
    //     }

    //     /** 
    //      * here, we get the ID of the selected User, and this is re-triggered
    //      * by the OK button...
    //      */

    //     /** get userdata from fastapi backend: */
    //     fetch(`/users/${user_id}/competencies/`, {
    //         method: 'GET',
    //         headers: {
    //             'Accept': 'application/json',
    //             'Content-Type': 'application/json'
    //         },
    //     }).then(function (response) {
    //          return response.json(); 
    //     }).then(function (response) { 
    //         currentData = [];
    //         for(let a=0;a<response.length;a++){
    //             currentData.push({
    //                 "key":[response[a].quadrant, response[a].sector,response[a].sector],
    //                 "rating":response[a].rating})
    //         }
    //         if (currentData) {
    //             var data = currentData;
    //             for (var a = 0; a < data.length; a++) {
    //                 if (engine.isQuadrant(data[a])) {
    //                     engine.addToUserdata(
    //                         data[a].key, 
    //                         data[a].rating
    //                     );
    //                     var elem = document.querySelector('[data-lookup="[' 
    //                         + data[a].key 
    //                         + ']"][data-rating="' 
    //                         + data[a].rating 
    //                         + '"]');
    //                     if (elem) {
    //                         elem.click();
    //                     }
    //                 }
    //             }
    //         }
    //     });
    // },
    
    // isQuadrant: function (data) {
    //     return data.rating >= 0 && data.rating <= 6;
    // },
    
    // test_handler: function (event) {
    //     if (this.current_score > -1) {
    //         engine.addToUserdata([this.current_quad, this.current_sector, this.current_score], this.current_rating);
    //         this.setAttribute('class', 'clicked');
    //     }
    //     engine.setSectorSVGClicked(this);
    //     event.preventDefault();
    // },

    // getQuadrantTitleFromData: function(titleParts){
    //     let out = "";
    //     for(let a=0;a<titleParts.length;a++){
    //         // out += titleParts[a].title + " ";
    //         out += titleParts[a].title_part + " ";
    //     }
    //     return out;
    // },

    // test_in: function () {
    //     // TODO: Update the use of data_0 title with data_quadrant_titles title_parts
    //     /**
    //      * This is scrappy AF. It's confusing and needs rationalising and making clearer!
    //      * i.e. split into branching out to explicit sub-functions. 
    //      */
    //     var self = document.getElementById(this.getAttribute('id'));
    //     if (self) {
    //         engine.setSectorSVGDisplay(self, true);
    //         var sector_rating = -1;
    //         var lookup = JSON.parse(this.getAttribute('data-lookup'));
    //         this.current_quad = lookup[0];
    //         this.current_sector = lookup[1];
    //         this.current_score = lookup[2];
    //         var quad_description = "";
    //         var quad_title = "";
    //         var sector_title = "";
    //         if (lookup[0] > -1) {
    //             quad_description = engine.data_quadrants[lookup[0]].summary;
    //             // quad_title = engine.getQuadrantTitleFromData(engine.data_quadrants[lookup[0]].title_parts);
    //             quad_title = engine.getQuadrantTitleFromData(engine.data_quadrants[lookup[0]].title);
    //         }
    //         var sector_title_description = '';
    //         if (lookup[1] > -1) {
                
    //             // STATIC DATA
    //             // sector_title_description = engine.data_quadrants[lookup[0]].sector_summaries[lookup[0]].description;
    //             // sector_title = engine.data_quadrants[lookup[0]].sector_summaries[lookup[0]].title;
    //             // DATABASE DATA
    //             sector_title_description = engine.data_quadrants[lookup[0]].sectors[lookup[0]].description;
    //             sector_title = engine.data_quadrants[lookup[0]].sectors[lookup[0]].title;
    //         }
    //         var sector_block_description = '';
    //         if (lookup[2] > -1) {
    //             console.log(engine.data_quadrants[lookup[0]]);
    //             // sector_title = engine.data_quadrants[lookup[0]].sector_summaries[lookup[1]].title;
    //             sector_title = engine.data_quadrants[lookup[0]].sectors[lookup[0]].title;
    //             sector_rating = parseInt(this.getAttribute('data-rating'));
    //             this.current_rating = sector_rating;
    //             // sector_block_description = engine.data_quadrants[lookup[0]].sector_descriptions[lookup[2]];
    //             // TODO RENAME THIS FUNCTION!!
    //             sector_block_description = engine.getQuadrantTitleFromData(engine.data_quadrants[lookup[0]].sectors[lookup[2]].title);
    //                            console.log(engine.data_quadrants[lookup[0]].sectors[lookup[2]]);
    //         }
    //         // special case for outer titles: TO SORT!
    //         if(lookup[1] > -1 && lookup[2]===-1){
    //             try{
    //                 // STATIC DATA:
    //                 // sector_title =             engine.data_quadrants[lookup[0]].sector_summaries[lookup[1]].title;
    //                 // sector_block_description = engine.data_quadrants[lookup[0]].sector_summaries[lookup[1]].description;
    //                 // DATABASE DATA:
    //                 sector_title =             engine.getQuadrantTitleFromData(engine.data_quadrants[lookup[0]].sectors[lookup[1]].title);
    //                 sector_block_description = engine.data_quadrants[lookup[0]].sectors[lookup[1]].description;

    //             }
    //             catch(e){
    //                 console.log(e);
    //             }
    //         }
    //         var output_rating = '';
    //         if (sector_rating > -1) {
    //             output_rating = engine.rating_description_lookup[sector_rating].title;
    //         }
    //         var elem_quad_title = document.getElementById('quad_title');
    //         var elem_quad_description = document.getElementById('quad_description');
    //         var elem_sector_title = document.getElementById('sector_title');
    //         var elem_sector_title_description = document.getElementById('sector_title_description');
    //         var elem_block_description = document.getElementById('sector_block_description');
    //         var elem_rating = document.getElementById('rating');
    //         if (elem_quad_title)
    //             elem_quad_title.innerText = quad_title;
    //         if (elem_quad_description)
    //             elem_quad_description.innerText = quad_description;
    //         if (elem_sector_title)
    //             elem_sector_title.innerText = sector_title;
    //         if (elem_sector_title_description)
    //             elem_sector_title_description.innerText = sector_title_description;
    //         if (elem_block_description)
    //             elem_block_description.innerText = sector_block_description;
    //         if (elem_rating)
    //             elem_rating.innerText = output_rating;
    //         var elem_title = [];
    //         if (quad_title && lookup[2] === -1)
    //             elem_title.push(quad_title);
    //         if (quad_description && lookup[2] === -1 && lookup[1] === -1)   //quad hover titles
    //             elem_title.push(quad_description);
    //         if (quad_description && lookup[2] === -1 && lookup[1] > -1)   //sector hover titles
    //             elem_title.push(sector_block_description);
    //         if (sector_title && lookup[2] === -1)
    //             elem_title.push(sector_title);
    //         if (sector_title_description && lookup[2] !== -1)
    //             elem_title.push(sector_title_description);
    //         if (sector_block_description && lookup[2] !== -1)
    //             elem_title.push(sector_block_description);
    //         self.setAttribute('title', elem_title.join('\n\n'));
    //     }
    // },

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
    
    // renderRatings: function () {
    //     var target = document.getElementById('userdata');
    //     target.innerText = "";
    //     engine.current_data.sort(function (a, b) {
    //         if (a.key[0] > b.key[0]) {
    //             return (1);
    //         }
    //         else {
    //             return (-1);
    //         }
    //     });
    //     for (var a = 0; a < engine.current_data.length; a++) {
    //         var row = document.createElement('div');
    //         //engine.getQuadrantTitleFromData(engine.data_quadrants[lookup[0]].title_parts);
    //         // STATIC DATA
    //         // row.appendChild(document.createTextNode(engine.getQuadrantTitleFromData(  engine.data_quadrants[engine.current_data[a].key[0]].title_parts)
    //         // DATABASE DATA:

    //         row.appendChild(document.createTextNode(engine.getQuadrantTitleFromData(  engine.data_quadrants[engine.current_data[a].key[0]].title)
    //         // row.appendChild(document.createTextNode(engine.data_quadrants[engine.current_data[a].key[0]].summary.title
    //             + ', '
    //             // STATIC DATA
    //             // + engine.data_quadrants[engine.current_data[a].key[0]].sector_summaries[engine.current_data[a].key[1]].title
    //             // DATABASE DATA:
    //             + engine.getQuadrantTitleFromData(engine.data_quadrants[engine.current_data[a].key[0]].sectors[engine.current_data[a].key[1]].title)
    //             + ': '
    //             + engine.rating_description_lookup[engine.current_data[a].rating].title
    //             + ' (' + engine.rating_description_lookup[engine.current_data[a].rating].description + ')'));

    //         target.appendChild(row);
    //     }
    // },
};

document.addEventListener("DOMContentLoaded",
    (evt) => {
        // load data then call init:
        // https://www.geeksforgeeks.org/javascript/read-json-file-using-javascript/
        function fetchJSONData() {
            fetch(engine.API_URL)
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
                .catch(error => {
                    console.error('Failed to fetch data:', error);
                    return({"status":"error", "message":'Failed to fetch data:', error});
                }
                ); 
        }
        // THIS NEEDS TO BE REPLACED WITH THE STATIC DATA RETURNED BY THE /compass/{id} ENDPOINT
        function fetchConstantData() {
            fetch(engine.CONSTANTS_URL)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();  
                })
                .then(constant_data => {
                    // apply data as required:
                    engine.loadConstantData(constant_data);  // put this into callback
                })  
                .catch(error => console.error('Failed to fetch constant data:', error)); 
        }
        fetchJSONData(); 
        // test:
        // THIS NEEDS TO BE REPLACED WITH THE STATIC DATA RETURNED BY THE /compass/{id} ENDPOINT
        fetchConstantData();
    }
)
