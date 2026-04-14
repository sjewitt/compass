var engine = {

    // This is the coordiate lookup for the title positions:
    CONSTANTS_URL: "/static/data/compass_titles.json",
    coordinate_lookup: null,
    data_quadrant: null,

    init: function () {
        // this is the function that draws the skewed boxes:
        this.getStaticSectorTitlesDOM();

        // and THIS is the function that renders the texts:
        this.renderDisplayedTexts();

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

        // this is the elem in the HTML page:
        let _render_titles = document.getElementById("static_titles");
        _render_titles.innerHTML = "";

        // iterate over quadrants:
        for(let qt=0; qt<4; qt++){
            let _polygon = document.createElementNS("http://www.w3.org/2000/svg",'polygon');
            // set CSS class so we can style it from the stylesheet:
            _polygon.setAttribute("class",`svg_title svg_quadrant_${qt+1}`);
            // draw the bounding box:
            _polygon.setAttribute("points",engine.coordinate_lookup.quadrants[qt].points);

            // and append to the wrapper:
            _render_titles.appendChild(_polygon);
            
            // just draw one box for single line title
            let _title = document.createElementNS("http://www.w3.org/2000/svg",'text');
            _title.setAttribute('id',`svg_title_${qt+1}_1`);
            _title.setAttribute('class',`svg_quad_title svg_quadrant_${qt+1}`);
            _title.setAttribute('font-size','24');
            // place the title texts inside the bounding boxes (defined in the static data JSON):
            _title.setAttribute('x',engine.coordinate_lookup.quadrants[qt].title[0].coords[0]);
            _title.setAttribute('y',engine.coordinate_lookup.quadrants[qt].title[0].coords[1]);
            
            // and append to the wrapper:
            _render_titles.appendChild(_title);
        }
    },

    renderDisplayedTexts: function(){
        // I'm using index 1 because of the way the element IDs are named.
        for(let x=1; x<=4;x++){
            let elem_id = `svg_title_${x}_1`;
            try{
                let elem = document.getElementById(elem_id);
                // and render the static texts from the static data file:
                elem.appendChild(document.createTextNode(engine.coordinate_lookup.quadrants[x-1].homepage_title))
            }
            catch(ex){
                console.log(`Cannot process quadrant title parts: ${ex}`);
            }
        }
    },

    loadConstantData: function(data){
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

    // This will load the data in the database for the users, so we can still generate the dropdown:
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
            */
            targetElem.innerHTML = "";
            targetElem.appendChild(engine.buildOptionElem(true,null,null));
            for(let x=0;x<response.length;x++){
                targetElem.appendChild(engine.buildOptionElem(false,response[x].name,response[x].id));
            }
        });
    },

    // handle the dropdown change
    redirectToUserTemplate: function(){
        let selected_user = document.getElementById("select_user").value;
        if(parseInt(selected_user) > 0){
            document.location.href = `/${selected_user}`;
        }
    },
};

document.addEventListener("DOMContentLoaded",
    (evt) => {
        function fetchConstantData() {
            fetch(engine.CONSTANTS_URL)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();  
                })
                .then(constant_data => {
                    engine.loadConstantData(constant_data);
                    // we need to call init() AFTER we have the contant data available: 
                    engine.init();
                })  
                .catch(error => console.error('Failed to fetch constant data:', error)); 
        }
        fetchConstantData();
    }
)
