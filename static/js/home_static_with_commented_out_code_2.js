var engine = {

    API_URL: "/compass/1/", 

    // This is the coordiate lookup for the title positions:
    CONSTANTS_URL: "/static/data/compass_titles.json",
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
        // this is the function that draws the skewed boxes:
        this.getStaticSectorTitlesDOM();

        // and THIS is the function that renders the texts:
        // So this needs to be replaced with something else

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

   
    // /** for template, simplify the function */
    // loadUser: function(){
    //     let selected_user = document.getElementById("select_user").value;
    //     engine.test_load_data(selected_user);
    // },
    
    // selectAndLoadUser: function(){
    //     var page = document.getElementsByTagName('body')[0].getAttribute('data-page');
    //     let selected_user = document.getElementById("select_user").value;

    //     /**  here we can loca the profile for the selected user:  */
    //     if (page === 'svg') {
    //         engine.test_load_data(selected_user);
    //         var export_data_elem = document.getElementById('flyout').firstChild;
    //         if (export_data_elem) {
    //             export_data_elem.addEventListener('click', this.export_data);
    //         }
    //     }
    // },

    redirectToUserTemplate: function(){
        let selected_user = document.getElementById("select_user").value;
        if(parseInt(selected_user) > 0){
            document.location.href = `/${selected_user}`;
        }
    },
    
    // addToUserdata: function (lookup, rating) {
    //     /**  here we add the data to the database rather than localstorage. Therefore, this also 
    //      * needs to have an async promise handler: */
    //     /** get the ID of the user from the dropdown */
    //     let user_id = document.getElementById("select_user").value;
    //     data = {
    //         "user_id": user_id,
    //         "quadrant": lookup[0],
    //         "sector": lookup[1],
    //         "rating": rating,
    //     }

    //     fetch('/competencies/add/', {
    //         method: 'POST',
    //         body: JSON.stringify(data),
    //         headers: {
    //             'Accept': 'application/json',
    //             'Content-Type': 'application/json'
    //         },
    //     }).then(function (response) {
    //          return response.json(); 
    //     }).then(function (response) { 
        
    //     });

    //     var append = true;
    //     for (var a = 0; a < engine.current_data.length; a++) {
    //         if (engine.current_data[a].key[0] === lookup[0] 
    //                 && engine.current_data[a].key[1] === lookup[1] 
    //                 && engine.current_data[a].key[2] === lookup[2])
    //             {
    //             append = false;
    //             engine.current_data[a].rating = rating;
    //         };
    //     }
    //     if (append) {
    //         engine.current_data.push({ 'key': lookup, 'rating': rating });
    //     }
    //     this.renderRatings();
    // },
    
    // setSectorSVGClicked: function (elem) {
    //     var id_prefix = elem.getAttribute('id').split('-')[0];
    //     var max_id = parseInt(elem.getAttribute('id').split('-')[1]);
    //     for (var a = 1; a <= 6; a++) {
    //         document.getElementById('svg_' + id_prefix + '-' + a).classList.remove('svg_clicked');
    //         document.getElementById('svg_' + id_prefix + '-' + a).classList.remove('svg_show');
    //     }
    //     for (var x = 1; x <= max_id; x++) {
    //         document.getElementById('svg_' + id_prefix + '-' + x).classList.add('svg_clicked');
    //         document.getElementById('svg_' + id_prefix + '-' + x).classList.add('svg_show');
    //     }
    // },
    
    // setSectorSVGDisplay: function (elem, show) {
    //     var id_prefix = elem.getAttribute('id').split('-')[0];
    //     var max_id = parseInt(elem.getAttribute('id').split('-')[1]);
    //     for (var x = 1; x <= max_id; x++) {
    //         var elem_1 = document.getElementById('svg_' + id_prefix + '-' + x);
    //         if (elem_1) {
    //             if (show) {
    //                 elem_1.classList.add('svg_hover');
    //             }
    //             else {
    //                 elem_1.classList.remove('svg_hover');
    //             }
    //         }
    //     }
    // },
    
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
