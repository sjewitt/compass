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

    /** This is the coordiates lookup for the title positions: */
    CONSTANTS_URL: "/static/data/compass_titles.json",
    
    rating_description_lookup: null,
    coordinate_lookup: null,
    data_quadrant: null,

    /** retrieve the list of DOM element IDs */
    elems: getElems(),

    current_quad: -1,
    current_sector: -1,
    current_score: -1,
    current_rating: -1,
    current_data: [],

    // pass in loaded data here 
    init: function (display_data) {

        // Set the properties of the object from the loaded data:
        if (display_data) {
            this.data_quadrants = display_data.data_quadrants;
            this.rating_description_lookup = display_data.rating_description_lookup;

            for (var _i = 0, _a = this.elems; _i < _a.length; _i++) {
                var id = _a[_i];
                var elem = document.getElementById(id);
                if (elem) {
                    elem.addEventListener('mouseover', this.test_in);
                    elem.addEventListener('mouseout', this.test_out);
                    elem.addEventListener('click', this.test_handler);
                }
            };

            this.getStaticSectorTitlesDOM();

            /** render the static quadrant and sector texts */
            this.renderDisplayedTexts();

            /**  directly call the user load function:  */
            engine.loadUser();

            /** append handler to data download button */
            let btn_data_download = document.getElementById("data_download");
            if (btn_data_download) {
                btn_data_download.addEventListener("click", this.retrieveUserData)
            }
        }
        else{
            // NOTE: See slightly hacky pushing of the User object onto the engine instance
            // at the end of the template
            console.log(`no compass found for user '${engine.user.name}'`);
        }
    },

    loadConstantData: function (data) {
        engine.coordinate_lookup = data;
    },

    /** 
     * Generate DOM for static quadrant and sector compass titles. We don't want to duplicate hardcoded
     * HTML in > 1 template
     */
    getStaticSectorTitlesDOM: function () {
        // This is why it did not display:
        // https://stackoverflow.com/questions/23588384/dynamically-created-svg-element-not-displaying

        let _render_titles = document.getElementById("static_titles");
        _render_titles.innerHTML = "";

        // iterate over quadrants:
        for (let qt = 0; qt < this.data_quadrants.length; qt++) {
            let _polygon = document.createElementNS("http://www.w3.org/2000/svg", 'polygon');

            _polygon.setAttribute("class", `svg_title svg_quadrant_${qt + 1}`);
            _polygon.setAttribute("points", engine.coordinate_lookup.quadrants[qt].points);

            // and append to the wrapper:
            _render_titles.appendChild(_polygon);

            // iterate over title parts for each quadrant (0, 1 or 2):
            for (let qtp = 0; qtp < this.data_quadrants[qt].title.length; qtp++) {
                let _title = document.createElementNS("http://www.w3.org/2000/svg", 'text');
                _title.setAttribute('id', `svg_title_${qt + 1}_${qtp + 1}`);
                _title.setAttribute('class', `svg_quad_title svg_quadrant_${qt + 1}`);
                _title.setAttribute('font-size', '24');
                _title.setAttribute('x', engine.coordinate_lookup.quadrants[qt].title[qtp].coords[0]);
                _title.setAttribute('y', engine.coordinate_lookup.quadrants[qt].title[qtp].coords[1]);

                _render_titles.appendChild(_title);
            }

            // and for each quadrant, generate the sector titles:
            for (let stp = 0; stp < this.data_quadrants[qt].sectors.length; stp++) {
                let sector_title_array = this.data_quadrants[qt].sectors[stp].title;
                // and for each of these, generate a <text> element:
                for (let xx = 0; xx < sector_title_array.length; xx++) {
                    let _sector_title = document.createElementNS("http://www.w3.org/2000/svg", 'text');
                    _sector_title.setAttribute('id', `svg_sector_${qt + 1}_${stp + 1}_${xx + 1}`);
                    _sector_title.setAttribute('font-size', '14');
                    _sector_title.setAttribute('x', engine.coordinate_lookup.quadrants[qt].sectors[stp][xx].coords[0]);
                    _sector_title.setAttribute('y', engine.coordinate_lookup.quadrants[qt].sectors[stp][xx].coords[1]);
                    _render_titles.appendChild(_sector_title);
                }
            }
        }
    },

    /** 
     * render the titles of the Compass bits, based on the compass currently assigned
     * to the user being displayed
     */
    renderDisplayedTexts: function () {
        for (let x = 1; x <= this.data_quadrants.length; x++) {
            // get the array of words for the current title elems:
            let current_words = this.data_quadrants[x - 1];

            // identify the text elements by ID:
            for (let y = 1; y <= current_words.title.length; y++) {
                let elem_id = `svg_title_${x}_${y}`;
                try {
                    let elem = document.getElementById(elem_id);
                    let txt = document.createTextNode(current_words.title[y - 1].title_part);
                    elem.appendChild(txt);
                }
                catch (ex) {
                    console.log(`Cannot process quadrant title parts: ${ex}`);
                }
            }

            // now get the segment titles: we do a double loop to get each segment, and the lines array for each:
            for (let z = 1; z <= current_words.sectors.length; z++) {
                for (let xx = 1; xx <= current_words.sectors[z - 1].title.length; xx++) {
                    let elem_id = `svg_sector_${x}_${z}_${xx}`;
                    try {
                        let elem = document.getElementById(elem_id);
                        let txt = document.createTextNode(current_words.sectors[z - 1].title[xx - 1].title_part);
                        elem.appendChild(txt);
                    }
                    catch (ex) {
                        console.log(`Cannot process segment title parts: ${ex}`);
                    }
                }
            }
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

    retrieveUserData: function () {
        let user_id = this.getAttribute('data-user-id').split(":")[1];
        /** now call API endpoint: */
        fetch(`/${user_id}/data/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                // 'Content-Disposition': 'attachment',
            },
        }).then(function (response) {
            return response.json();
        }).then(function (response) {
            /** the ResponseRedirect from the server is failing, so
             * try with JS instead:
             */
            if (response.usercreated) {
                document.location.href = `/static/?user_id=${response.user_id}`
            }
        });
    },

    test_load_data: function (user_id = 0) {
        /** first, clear the current data */
        // https://developer.mozilla.org/en-US/docs/Web/API/NodeList
        var svg_compass = Array.from(document.getElementById("svg_compass").childNodes);
        for (let _x = 0; _x < svg_compass.length; _x++) {
            if (svg_compass[_x].tagName === "polygon") {
                /** ignore outer titles, because removing style from this causes an error */
                if (!svg_compass[_x].classList.contains("svg_title")) {
                    svg_compass[_x].classList.remove('svg_clicked');
                    svg_compass[_x].classList.remove('svg_show');
                }
            }
        }

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
            for (let a = 0; a < response.length; a++) {
                currentData.push({
                    "key": [response[a].quadrant, response[a].sector, response[a].sector],
                    "rating": response[a].rating
                })
            }
            if (currentData) {
                var data = currentData;
                for (var a = 0; a < data.length; a++) {
                    if (engine.isQuadrant(data[a])) {
                        engine.addToUserdata(
                            data[a].key,
                            data[a].rating
                        );
                        var elem = document.querySelector('[data-lookup="['
                            + data[a].key
                            + ']"][data-rating="'
                            + data[a].rating
                            + '"]');
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

    getQuadrantTitleFromData: function (titleParts) {
        let out = "";
        for (let a = 0; a < titleParts.length; a++) {
            out += titleParts[a].title_part + " ";
        }
        return out;
    },

    test_in: function () {
        /**
         * This is scrappy AF. It's confusing and needs rationalising and making clearer!
         * i.e. split into branching out to explicit sub-functions. 
         */
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
                quad_description = engine.data_quadrants[lookup[0]].summary;
                quad_title = engine.getQuadrantTitleFromData(engine.data_quadrants[lookup[0]].title);
            }
            var sector_title_description = '';
            if (lookup[1] > -1) {

                // DATABASE DATA
                sector_title_description = engine.data_quadrants[lookup[0]].sectors[lookup[0]].description;
                sector_title = engine.data_quadrants[lookup[0]].sectors[lookup[0]].title;
            }
            var sector_block_description = '';
            if (lookup[2] > -1) {
                sector_title = engine.data_quadrants[lookup[0]].sectors[lookup[0]].title;
                sector_rating = parseInt(this.getAttribute('data-rating'));
                this.current_rating = sector_rating;
                sector_block_description = engine.getQuadrantTitleFromData(engine.data_quadrants[lookup[0]].sectors[lookup[2]].title);
            }
            // special case for outer titles: TO SORT!
            if (lookup[1] > -1 && lookup[2] === -1) {
                try {
                    // DATABASE DATA:
                    sector_title = engine.getQuadrantTitleFromData(engine.data_quadrants[lookup[0]].sectors[lookup[1]].title);
                    sector_block_description = engine.data_quadrants[lookup[0]].sectors[lookup[1]].description;
                }
                catch (e) {
                    console.log(e);
                }
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
            if (quad_description && lookup[2] === -1 && lookup[1] === -1)   //quad hover titles
                elem_title.push(quad_description);
            if (quad_description && lookup[2] === -1 && lookup[1] > -1)   //sector hover titles
                elem_title.push(sector_block_description);
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

    /** load the data for the current user */
    loadUser: function () {
        let selected_user = document.getElementById("current_user").value;
        engine.test_load_data(selected_user);
    },

    addToUserdata: function (lookup, rating) {
        /**  here we add the data to the database: */
        let user_id = document.getElementById("current_user").value;
        let compass_id = document.getElementById("compass_id").value;
        data = {
            "user_id": user_id,
            "compass_id": compass_id,
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
        }).then(function (response) {  /** ? */ });

        var append = true;
        for (var a = 0; a < engine.current_data.length; a++) {
            if (engine.current_data[a].key[0] === lookup[0]
                && engine.current_data[a].key[1] === lookup[1]
                && engine.current_data[a].key[2] === lookup[2]) {
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
            row.appendChild(document.createTextNode(engine.getQuadrantTitleFromData(engine.data_quadrants[engine.current_data[a].key[0]].title)
                + ', '
                + engine.getQuadrantTitleFromData(engine.data_quadrants[engine.current_data[a].key[0]].sectors[engine.current_data[a].key[1]].title)
                + ': '
                + engine.rating_description_lookup[engine.current_data[a].rating].title
                + ' (' + engine.rating_description_lookup[engine.current_data[a].rating].description + ')'));
            target.appendChild(row);
        }
    },
};

// User management and auth has not yet been addressed... A BIG TODO:!
document.addEventListener("DOMContentLoaded",
    (evt) => {
        // load data then call init:
        // https://www.geeksforgeeks.org/javascript/read-json-file-using-javascript/
        function fetchJSONData() {
            fetch(`/compass/${document.getElementById("compass_id").value}`)
                .then(response => {
                    if (!response.ok) {
                        // throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(display_data => {
                    // apply data as required:
                    engine.init(display_data);  // put this into callback
                })
                .catch(error => {
                    console.error('Failed to fetch data:', error);
                    return ({ "status": "error", "message": 'Failed to fetch data:', error });
                }
                );
        }
        /** Retrieve the coordinate data from the JSON file: */ 
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
                    engine.loadConstantData(constant_data);
                })
                .catch(error => console.error('Failed to fetch constant data:', error));
        }
        fetchJSONData();
        fetchConstantData();
    }
);