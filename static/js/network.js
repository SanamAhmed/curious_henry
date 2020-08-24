// create an array with nodes
var nodes = new vis.DataSet([
	{
		id: 1,
		label: 'JohnCena',
		title: `<div>
			<code>
				<a href="createProject.html">Filename.whatever</a>
			</code>
		</div>`,
		url: 'index.html'
	},
	{
		id: 2,
		label: 'Undertaker',
		title: `<div>
			<code>
				<a href="createProject.html">Filename.whatever</a>
			</code>
		</div>`,
		url: 'index.html'
	},
	{
		id: 3,
		label: 'ReyMysterio',
		title: `<div>
			<code>
				<a href="createProject.html">Filename.whatever</a>
			</code>
		</div>`,
		url: 'index.html'
	},
	{
		id: 4,
		label: 'Batista',
		title: `<div>
			<code>
				<a href="createProject.html">Filename.whatever</a>
			</code>
		</div>`,
		url: 'index.html'
	},
	{
		id: 5,
		label: 'Roman',
		title: `<div>
			<code>
				<a href="createProject.html">Filename.whatever</a>
			</code>
		</div>`,
		url: 'index.html'
	},
	{
		id: 6,
		label: 'Omaga',
		title: `<div>
			<code>
				<a href="createProject.html">Filename.whatever</a>
			</code>
		</div>`,
		url: 'index.html'
	},
	{
		id: 7,
		label: 'Rausev',
		title: `<div>
			<code>
				<a href="createProject.html">Filename.whatever</a>
			</code>
		</div>`,
		url: 'index.html'
	},
	{
		id: 8,
		label: 'Sheamus',
		title: `<div>
			<code>
				<a href="createProject.html">Filename.whatever</a>
			</code>
		</div>`,
		url: 'index.html'
	}
]);

// create an array with edges
var edges = new vis.DataSet([
	{ from: 1, label: 'Fights', to: 3 },
	{ from: 1, label: 'Fights', to: 2 },
	{ from: 2, to: 4 },
	{ from: 2, to: 5 },
	{ from: 4, to: 3 },
	{ from: 5, to: 1 },
	{ from: 5, to: 8 },
	{ from: 6, to: 7 },
	{ from: 3, to: 7 },
	{ from: 6, to: 1 }
]);

// create a network
var container = document.getElementById('mynetwork');

// provide the data in the vis format
var data = {
	nodes: nodes,
	edges: edges
};
var options = {
	manipulation: {
		enabled: false,
		initiallyActive: false,
		addNode: true,
		addEdge: true,
		editNode: undefined,
		editEdge: true,
		deleteNode: true,
		deleteEdge: true,
		controlNodeStyle: {
			// all node options are valid.
		}
	},
	interaction: {
		tooltipDelay: 3600000,
		selectable: true,
		hover: true // Set a really big delay - one hour
	},
	physics: true,
	edges: {
		smooth: {
			enabled: true,
			roundness: 0
		},
		width: 1,
		font: {
			color: '#111',
			size: 16,
			face: 'Rubik'
		},
		arrows: {
			to: {
				enabled: true,
				scaleFactor: 1
			},
			middle: {
				enabled: false,
				scaleFactor: 1
			},
			from: {
				enabled: false,
				scaleFactor: 1
			}
		}
	},

	nodes: {
		shape: 'box',
		borderWidth: 3,
		color: {
			background: '#5780b2',
			border: '#238a91'
		},
		font: {
			color: '#ffffff',
			size: 18,
			face: 'Rubik'
		},
		shadow: {
			enabled: true,
			color: 'rgba(0,0,0,0.3)',
			size: 5,
			x: 3,
			y: 5
		}
	}
};

function addNetwork() {
	try {
		nodes.add({
			id: 15,
			label: 'Jeff Hardy'
		});
		nodes.add({
			id: 16,
			label: 'TripleH'
		});
		nodes.add({
			id: 17,
			label: 'Miz'
		});
		edges.add({
			id: 15,
			from: '15',
			to: '16'
		});
		edges.add({
			id: 16,
			from: '16',
			to: '17'
		});
	} catch (err) {
		alert(err);
	}
}

// initialize your network!
var network = new vis.Network(container, data, options);

// Intercept the click event
network.on('hoverNode', function(params) {
	// Check if you clicked on a node; if so, display the title (if any) in a popup
	network.interactionHandler._checkShowPopup(params.pointer.DOM);
});

network.on('selectNode', function(params) {
	if (params.nodes.length === 1) {
		var node = nodes.get(params.nodes[0]);
		window.open(node.url, '_blank');
	}
});
