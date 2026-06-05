// import { export_test, getElems } from "./common.js";

var engine = {

    // This is the coordiate lookup for the title positions:
    CONSTANTS_URL: "/static/data/compass_titles.json",
    coordinate_lookup: null,
    data_quadrant: null,
    
    /** retrieve the list of DOM element IDs */
    elems: getElems(),

    init: function () {

        // lets make it funky!:
        for (var _i = 0, _a = this.elems; _i < _a.length; _i++) {
            var id = _a[_i];
            var elem = document.getElementById(id);
            // console.log(id, elem);
            if (elem) {
                elem.addEventListener('mouseover', this.test_in);
                elem.addEventListener('mouseout', this.test_out);
                elem.addEventListener('click', this.doFunkyStuff );
            }
        };

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

    /** 
     * short version uses single title per quad. Maybe revert, so I can use common JS?
     * There's a risk of diverging different versions of the same function here...
     */
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

    toggle_circle :false,
    current_radius: -1,
    doFunkyStuff: function(){
        if(engine.toggle_circle){
            engine.toggle_circle = false;
        }
        else{
            engine.toggle_circle = true;
        }
        let curr = this.getAttribute("id");
        console.log(curr);
        // now get all at this radius:
        let radius = curr.split('-')[1];
        if(engine.current_radius !== parseInt(radius)){
            engine.toggle_circle = true;
            engine.current_radius = parseInt(radius)
        }

        console.log(parseInt(radius))
        if(!isNaN(parseInt(radius))){
            console.log(`Radius: ${radius}`)
            // now get all sector bits at this radius:
            let test = new RegExp("s[0-9]{1,}-"+radius, "g");
            
            // clear them all:
            for(let n=0;n<engine.elems.length;n++){
                engine.setSectorSVGDisplay(document.getElementById(engine.elems[n]), false);
            }
            let counter = 0;
            for(let n=0;n<engine.elems.length;n++){
                // console.log(engine.elems[n])
                let slice = document.getElementById(engine.elems[n]);
                
                if(engine.elems[n].match(test)){
                    counter++;
                    console.log(engine.elems[n], counter);
                    engine.setSectorSVGDisplay(document.getElementById(engine.elems[n]), engine.toggle_circle, false);
                }
            }
        }
    },

    // Cut down version just animates the compass:
    test_in: function () {
        var self = document.getElementById(this.getAttribute('id'));
        if (self) {
            engine.setSectorSVGDisplay(self, true);
        }
    },

    test_out: function () {
        var self = document.getElementById(this.getAttribute('id'));
        if (self) {
            engine.setSectorSVGDisplay(self, false);
        }
    },

    setSectorSVGDisplay: function (elem, show,recurse=true) {
        var id_prefix = elem.getAttribute('id').split('-')[0];
        var max_id = parseInt(elem.getAttribute('id').split('-')[1]);
        // animate hovered and all back to centre:
        console.log(`animating sector #${elem.getAttribute('id')}`)
        if(recurse){
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
        }
        else{
            var elem_1 = document.getElementById('svg_' + id_prefix + '-' + max_id);
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
        export_test();
        console.log(engine.fish);
    }
)
