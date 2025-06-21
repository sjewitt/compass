let engine = {
	/* do an array mapping data-rating to a colour, and set the element background colour to be that...
	TODO:
	 - main titles data attr
	 = sector description (to add, all )
	 - rating (to collect, per concentric thing)
	 [
	     quadrant, if not -1
	     sector TITLE if not -1
	     sector BODY if not -1
	 ]
	*/
	
	/* display data */
/** 
 * quadrant descriptions
 
 I need to be REALLY careful to map these indexes correctly!
 Assume hotspots are defined clockwise from 12:00, but the spreadsheet 
 data is not that order...
 
 */
/** TODO: make self-contained data structure that is not dependent on ORDER */
//	all_data : {
//		'q1':{'title':'Product &amp; service design', 'description':'Includes Proposition Design, Product Design, Digital and Physical Experience Design'},
//		'q2':{'title':'Management &amp; leadership', 'description':'How we influence people to get stuff done'},
//		'q3':{'title':'Capability building', 'description':'Providing clients with the tools they need to achieve their goals.'},
//		'q4':{'title':'Transforming organizations', 'description':'What skills do you have that can support our clients in their ambitions to change their business?'}
//	},

/**
COMPLETELY UNFAMILIAR
Little to no understanding of the topic and no experience. 

NOVICE
You are open to learning as much as you can about the skill, from all internal and external sources. You share your learning with your peers, who may not be so inquisitive or up-to-date given their more established views and expertise.

Client role comparison (you should be able to comfortably guide and challenge) - graduates, junior

FOUNDATION
You are aware of the regularly used skills and have observed them in action. You have a technical understanding of key elements but not a great deal of experience. You can be relied upon to receive a brief, and contribute to its delivery.

Client role comparison (you should be able to comfortably guide and challenge) -  executive


COMPETENT
You are adept at the key, common skills - ones that are well known and regularly used at Magnetic (and other organisations). You can be relied upon to receive a brief, respond to and shape it, and then deliver.

Client role comparison (you should be able to comfortably guide and challenge) -  senior executive

ADVANCED
You are adept at a broad range range of skills, knowing what's possible and available and appropriate for any given situation. You are able to coach and train others in those skills and approaches. You are able to write briefs for your team to execute. You are able to develop unique positions and approaches for Magnetic.

Client role comparison (you should be able to comfortably guide and challenge) - head of...

MASTER
You are seen as the best in your craft on an industry-wide stage and are a thought-leader publicly. You are able to identify when new skills or methods need to be introduced and developed based on the task or customer need. You are comfortable sitting in C-Suite situations and explain, challenge and recruit in this craft.

Client role comparison (you should be able to comfortably guide and challenge) - C-suite, Director
 */

	rating_description_lookup : [
		{'title':'unrated','description':'n/a'},
		{'title':'Competely unfamiliar','description':'Little to no understanding of the topic and no experience.'},
		{'title':'Novice','description':'You are open to learning as much as you can about the skill, from all internal and external sources. You share your learning with your peers, who may not be so inquisitive or up-to-date given their more established views and expertise.\n\nClient role comparison (you should be able to comfortably guide and challenge) - graduates, junior'},
		{'title':'Foundation','description':'You are aware of the regularly used skills and have observed them in action. You have a technical understanding of key elements but not a great deal of experience. You can be relied upon to receive a brief, and contribute to its delivery.\n\nClient role comparison (you should be able to comfortably guide and challenge) -  executive'},
		{'title':'Competent','description':'You are adept at the key, common skills - ones that are well known and regularly used at Magnetic (and other organisations). You can be relied upon to receive a brief, respond to and shape it, and then deliver.\n\nClient role comparison (you should be able to comfortably guide and challenge) -  senior executive'},
		{'title':'Advanced','description':'You are adept at a broad range range of skills, knowing what\'s possible and available and appropriate for any given situation. You are able to coach and train others in those skills and approaches. You are able to write briefs for your team to execute. You are able to develop unique positions and approaches for Magnetic.\n\nClient role comparison (you should be able to comfortably guide and challenge) - head of...'},
		{'title':'Master','description':'You are seen as the best in your craft on an industry-wide stage and are a thought-leader publicly. You are able to identify when new skills or methods need to be introduced and developed based on the task or customer need. You are comfortable sitting in C-Suite situations and explain, challenge and recruit in this craft.\n\nClient role comparison (you should be able to comfortably guide and challenge) - C-suite, Director'}
	],
	
	/** quadrant description and title */
	data_0 : [
	    {'description':'Includes Proposition Design, Product Design, Digital and Physical Experience Design','title':'Product & service design'},
	    {'description':'How we influence people to get stuff done','title':'Management & leadership'},
	    {'description':'Providing clients with the tools they need to achieve their goals.','title':'Capability building'},
	    {'description':'What skills do you have that can support our clients in their ambitions to change their business?','title':'Transforming organizations'}
	],

	/** sector title descriptions within each quadrant */
	data_1 : [
	    [
	        {'description': 'Understanding how to originate, encourage and communicate complex ideas and concepts with simplicity and clarity.', 'title':'Ideas & concepts'},
	        {'description': 'Ability to use tools that will reduce uncertainty and test hypotheses', 'title':'Prototypes & experiments'},
	        {'description': 'Skills in the creation and definition of functional, usable and simplified user experiences', 'title':'UX design'},
	        {'description': 'Skills in the creation of beautiful and functional things using the right tools.', 'title':'Visual design'},
	        {'description': 'Skills in the creation of interactions over time that make our clients stand out in the minds of their customers', 'title':'Service design'}
	    ],
	    [
	        {'description': 'Building effective, successful and long lasting relationships','title':'Client & account management'},
	        {'description': 'Understanding the impact of decisions we make on the business from a financial, risk and regulatory perspective.','title':'Commerials'},
	        {'description': 'Effective use of the tools and rituals involved in running lean and agile projects with a focus on people and results','title':'Agile PM/coaching'},
	        {'description': 'Skills in running virtual and in person workshops to smoothly and simply achieve the stated goals.','title':'Facilitation'}
	    ],
	    [
			{'description': 'Know how to enable our clients businesses to become more innovative','title':'Innovation capabilities'},
			{'description': 'Understand the skills our client needs to exceed expectations in their next role. Know how to support them to get there.','title':'Leadership readiness'},
	        {'description':  'Ability to share knowledge and guide people to reach their full potential','title':'Mentoring & coaching'},
	        {'description':  'Creation and delivery of training in our tools and techniques','title':'Innovation training'}
	        
	    ],
	    [
	        {'description': 'How you research, define and bring to life the desired future state of our client.','title':'Strategy & vision'},
	        {'description': 'Using powerful storytelling to influence the behaviours of people who make up the client’s business.','title':'Culture & experience'},
	        {'description':  'Understanding which tools will accelerate the client’s ability to achieve their future vision and using them to predict the effect on customer behaviour.','title':'Business design & growth'},
	        {'description':  'Use of varied research skills to understand the needs, wants and desires of customers.','title':'Customer insights'}
	    ],
	],

	/** sector area descriptions - applies to all concentric levels */
	data_2 : [
	    [
	        'Has experience of using a variety of tools to generate ideas and concepts. Can plan and lead an ideation workshop. Understands how to create \'just enough\' to show the viability / art of the possible in the idea we are communicating.',
	        'Use tools that will reduce uncertainty and test hypotheses. Understand the different types of experiments and their suitability. Communicate the plan, hypothesis and outcomes with clients Analyse results in various formats.',
	        'Independently create and define functional, usable and simplified user experiences. Understand of the importance of designing for accessibility Communicate the thought behind the design and work collaboratively to achieve sign off.',
	        'Shape and drive of visual outcomes throughout the course of a project Communicate the thought behind the design and work collaboratively to achieve sign off. Review the work of junior designers and give feedback to improve',
	        'Own end-to-end user journey Understand the user needs and foresee painpoints to deliver desired organisational needs Ability to communicate the thought behind the design and work collaboratively to achieve sign off.'
	    ],
	    [
	        'build relationships with prospective clients, maintain relationships with existing clients, regularly share interesting insights with their network, spot and qualify opportunities. broker introductions to relevant Magnets and others in the Magnetic network.',
			'Liasie effectively and in a timely manner with finance, produce high-quality commercial documentation and reports such as SOW and project tracker. Keep track of the numbers week in and week out. Understanding of contracts and procurement. They understand the impact of commercial decisions on the wider business',
	        'Coach others and gain buy-in from clients and teams (client and internal) for Agile ways of working. Deliver medium-sized projects successfully. Manage simultaneous engagements successfully',
	        'Demonstrate the ability to plan lead, facilitate, and deliver a workshop with positive, on-brief outcomes Lead and sign off on the work of others.'
	    ],
	    [
			'Is able to assess the current innovation capability of a department / group / team and advise on what structural changes and training is needed to enable them to become more innovative.',
			'Role models soft skills, values and behaviours the clients can emulate (Setting a great example). Receive feedback from clients saying they\'ve learned by doing when they worked with you. Confidently coach others',
			'Share their skills with colleagues and set a good example as needed. Actively listen to colleagues and asks questions to help guide them to their own solutions. Understands the difference between coaching and mentoring and when to use that approach',
	        'Is able to lead training sessions on our core tools. Is confident in using real life stories in training. Gets the balance right between showing and telling and leads training sessions with a focus on interaction and discussion over lecturing and slideware. Is able to pivot a session to meet the requirements of the trainees.',
   	    ],
	    [
	        'Define the strategic change for a project within a well defined scope. Define the strategy for a part of a business or product',
	        'Independently create a plan for influencing cultural change. Use tools like experience mapping to define and plan a new or improved experience. Be able to use storytelling to influence adoption of new behaviours.',
	        'Understands the intersection between viability, desirability, feasibility and integrity (impact). Knows how to bridge the gap between customer desirability and business-model viability. Plans and communicates what the business impact of our projects will be. ',
	        'Independently carry out customer interviews and actively participate in synthesis sessions. Contribute to creation of discussion guides and development of other research/insight techniques. Carry out research on customers within a well understood scope. Research and create insights about an aspect of a service'
	    ]
	],

	/* map element id data */
	elems : [
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
	
	current_quad : -1,
	current_sector : -1,
	current_score : -1,
	current_rating : -1,
	
	current_data : {},
	
	init : function(){
		let page = document.getElementsByTagName('body')[0].getAttribute('data-page');
		this.current_data = [];	
		/** TODO: switch on pag type ? */
		/** onload, retrieve the current data 
		 * This will require soe refactoring to account for async call to rertieve the data
		*/
				
		for(id of this.elems){
			elem = document.getElementById(id)
			elem.addEventListener('mouseover',this.test_in);
			elem.addEventListener('mouseout',this.test_out);
			elem.addEventListener('click',this.test_handler);
		};
		//TEST
//		let in_data = [
//			{'key':[1,3,3],'rating':1},
//			{'key':[1,2,2],'rating':1},
//			{'key':[3,0,0],'rating':6},
//			{'key':[0,0,0],'rating':5}
//			]
		
		if(page === 'svg'){
			engine.test_load_data();
			
			/** data export from localstorage */
			let export_data_elem = document.getElementById('flyout');
			export_data_elem.addEventListener('click', this.export_data)
		}
//		let svg = document.getElementById('svg_compass');
	},
	
	/**
	 * https://stackoverflow.com/questions/14964035/how-to-export-javascript-array-info-to-csv-on-client-side
	 */
	export_data: function(){
		
		/** test POST to proxy handler: */
		fetch('/handler.php', {
		    method: 'POST',
		    headers: {
		        'Accept': 'application/json',
		        'Content-Type': 'application/json'
		    },
		    body: JSON.stringify(engine.current_data)
		})
	   .then(response => response.json())
	   .then(response => console.log(response));
	   /** end test */
		
		/** collect data from localstorage (or database, eventually) and return as CSV */
		let _out = [];
		_out.push(['quadrant','sector','rating']);
		for(let x=0; x < engine.current_data.length; x++){
			_out.push([engine.current_data[x].key[0], engine.current_data[x].key[1],engine.current_data[x].rating])
		}

		/** now generate CSV data: */
		let _return = "data:text/csv;charset=utf-8,";
		_out.forEach(function(arr){	//'arr' is the 'each'...
		    _return += arr.join(",") + "\r\n";
		})
		
		//test - crude - 'download.csv'
		var encodedUri = encodeURI(_return);
		//window.open(encodedUri);
		
		/** better option - named download, but needs an anchor tag */
		let link = document.getElementById("download_hidden_link");
		link.setAttribute("href", encodedUri);
		link.setAttribute("download", "compass.csv");
		link.click();
	},
	
	/** call API endpoint to return currently stored data
	 * This will be a call to a back-end storage of previously stored data for current user.
	 * NOTE: this may need to be refactored if something becomes dependent on this data being loaded first
	 * 
	 * replace this with localStorage.get();?
	 */
	test_load_data : function(){
		let data = JSON.parse(localStorage.getItem('compassData'));
		for(let a=0;a<data.length;a++){
			engine.addToUserdata(data[a].key,data[a].rating);
			
			/**
			 * and identify the elements to autoclick:
			 * https://stackoverflow.com/questions/29937768/document-queryselector-multiple-data-attributes-in-one-element
			 */
			let elem = document.querySelector('[data-lookup="['+data[a].key+']"][data-rating="'+data[a].rating+'"]');
			elem.click();
		}

//		fetch("/test_data/data.txt")
//		.then(
//			(response) => response.json()
//		)
//		.then(function(data){
//			for(let a=0;a<data.length;a++){
//				engine.addToUserdata(data[a].key,data[a].rating);
//				
//				/**
//				 * and identify the elements to autoclick:
//				 * https://stackoverflow.com/questions/29937768/document-queryselector-multiple-data-attributes-in-one-element
//				 */
//				let elem = document.querySelector('[data-lookup="['+data[a].key+']"][data-rating="'+data[a].rating+'"]');
//				elem.click();
//			}
//		});
	},
	
	test_handler : function(event){
		if(this.current_score > -1){
			engine.addToUserdata([this.current_quad,this.current_sector,this.current_score], this.current_rating);
			this.setAttribute('class','clicked');
		}
		/** also need to set the class so the mouse leave only hides if the given item has NOT been clicked */
		engine.setSectorSVGDClicked(this);
		/** suppress the scrolling to top on click */
		event.preventDefault();
	},

	test_in : function(){
		let self = document.getElementById(this.getAttribute('id'))
		// document.getElementById('svg_'+this.getAttribute('id')).classList.add('svg_show');
		engine.setSectorSVGDDisplay(self,true);
		let sector_rating = -1;
	    let lookup = JSON.parse(this.getAttribute('data-lookup')); // expects a string of '[n,n,n]' where n is integer
	    this.current_quad = lookup[0];
		this.current_sector = lookup[1];
		this.current_score = lookup[2];
	    
	    /** quadrant */
	    let quad_description = false;
	    let quad_title = false;
	    let sector_title = '';
	    if(lookup[0] > -1){
		    quad_description = engine.data_0[lookup[0]].description;
	        quad_title = engine.data_0[lookup[0]].title;
	    }
	    
	    /** sector titles */
	    let sector_title_description = '';
		if(lookup[1] > -1){
		    sector_title_description = engine.data_1[lookup[0]][lookup[1]].description;
		    sector_title = engine.data_1[lookup[0]][lookup[1]].title;
		}
		
		/** sector blocks (all) */
		let sector_block_description = '';
		if(lookup[2] > -1){
			sector_title = engine.data_1[lookup[0]][lookup[1]].title;
			sector_rating = parseInt(this.getAttribute('data-rating'));
			this.current_rating = sector_rating;
		    sector_block_description = engine.data_2[lookup[0]][lookup[2]];
		}

		let output_rating = '';
		if(sector_rating > -1){
			output_rating = engine.rating_description_lookup[sector_rating].title;
		}

		document.getElementById('quad_title').innerText = quad_title;
		document.getElementById('quad_description').innerText = quad_description;
		document.getElementById('sector_title').innerText = sector_title;
		document.getElementById('sector_title_description').innerText = sector_title_description;
		document.getElementById('sector_block_description').innerText = sector_block_description;
		document.getElementById('rating').innerText = output_rating;
		let elem_title = [];

		if(quad_title && lookup[2] === -1) elem_title.push(quad_title);
		if(quad_description && lookup[2] === -1) elem_title.push(quad_description);
		if(sector_title && lookup[2] === -1) elem_title.push(sector_title);
		if(sector_title_description  && lookup[2] !== -1) elem_title.push(sector_title_description);
		if(sector_block_description && lookup[2] !== -1) elem_title.push(sector_block_description);
		
		self.setAttribute('title',elem_title.join('\n\n'))
	},
	
	test_out : function(){
		let self = document.getElementById(this.getAttribute('id'))
		engine.setSectorSVGDDisplay(self,false);
		//document.getElementById('svg_'+this.getAttribute('id')).classList.remove('svg_show');
		document.getElementById('rating').innerText = "";
	},
	
	addToUserdata : function(lookup,rating){
		//if(lookup[2]>-1){
		let append = true;
		for(let a=0;a<engine.current_data.length;a++){
			if(engine.current_data[a].key[0] === lookup[0] && engine.current_data[a].key[1] === lookup[1] && engine.current_data[a].key[2] === lookup[2]){
				append = false;
				engine.current_data[a].rating = rating;
			}
		}
		if(append){
			engine.current_data.push({'key':lookup,'rating':rating})
		}
		console.log(engine.current_data);
		/** hook in API database update call here */
		
		/** or push to localstorage... */
		localStorage.removeItem('compassData')
		localStorage.setItem('compassData',JSON.stringify(engine.current_data));
		this.renderRatings();
		//}
	},
	
	/** 
	 * set a 'clicked' flag on a sector from the clicked element to the centre. This flag is used
	 * to suppress the hover off removal of the colour:
	 */
	setSectorSVGDClicked : function(elem){
		let id_prefix = elem.getAttribute('id').split('-')[0];
		let max_id = parseInt(elem.getAttribute('id').split('-')[1]);
		
		/** first, remove ALL */
		for(let a=1;a<=6;a++){
			document.getElementById('svg_'+id_prefix + '-'+a).classList.remove('svg_clicked');
			document.getElementById('svg_'+id_prefix + '-'+a).classList.remove('svg_show');
		}
		/** then set the currently clicked element: */
		for(let x=1;x<=max_id;x++){
			document.getElementById('svg_'+id_prefix + '-'+x).classList.add('svg_clicked');
			document.getElementById('svg_'+id_prefix + '-'+x).classList.add('svg_show');
		}
	},
	
	/** 
	 * Take a hover element, and set the visibility of all LOWER rated ones
	 */
	setSectorSVGDDisplay : function(elem,show){
		let id_prefix = elem.getAttribute('id').split('-')[0];
		let max_id = parseInt(elem.getAttribute('id').split('-')[1]);

		/** build IDs: */
		for(let x=1;x<=max_id;x++){
			let elem = document.getElementById('svg_'+id_prefix + '-'+x);
			if(elem){
				if(show){
					//document.getElementById('svg_'+id_prefix + '-'+x).classList.add('svg_show');
					//elem.classList.add('svg_show');
					elem.classList.add('svg_hover');
				}
				else{
//					if(!elem.classList.contains('svg_clicked')){
//						elem.classList.remove('svg_show');
//					}
					elem.classList.remove('svg_hover');
//					if(!document.getElementById('svg_'+id_prefix + '-'+x).classList.contains('svg_clicked')){
//						document.getElementById('svg_'+id_prefix + '-'+x).classList.remove('svg_show');
//					}
				}				
			}
		}
		//document.getElementById('svg_'+elem.getAttribute('id')).classList.add('svg_show');
	},
	
	renderRatings : function(){
		let target = document.getElementById('userdata');
		target.innerText = "";
		engine.current_data.sort((a,b) => (a.key[0] > b.key[0]) ? 1 : -1);
		for(let a=0;a<engine.current_data.length;a++){
			let row = document.createElement('div');
			/** do as better DOM elements! */
			row.appendChild(document.createTextNode(
				engine.data_0[engine.current_data[a].key[0]].title
				+', '
				+engine.data_1[engine.current_data[a].key[0]][engine.current_data[a].key[1]].title
				+': '
				+engine.rating_description_lookup[engine.current_data[a].rating].title
				+ ' (' + engine.rating_description_lookup[engine.current_data[a].rating].description + ')'
			));
			target.appendChild(row);
		}
	},
}

engine.init();
