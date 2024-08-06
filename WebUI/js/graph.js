// graph.js

// Initialize the graph visualization
function initializeGraph() {
    // Constants for graph width and height
    const width = 800;
    const height = 600;

    // Load the graph data from a JSON file
    d3.json('data/graph-data.json').then(graph => {
        console.log('Graph data loaded:', graph);

        // Create an SVG element
        const svg = d3.select('svg')
            .attr('width', '100%')
            .attr('height', '100%');

        // Create a simulation with forces
        const simulation = d3.forceSimulation(graph.nodes)
            .force('link', d3.forceLink(graph.links).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-200))
            .force('center', d3.forceCenter(width / 2, height / 2));

        // Create links
        const link = svg.append('g')
            .attr('class', 'links')
            .selectAll('line')
            .data(graph.links)
            .enter().append('line')
            .attr('stroke-width', 2); // Set stroke width for visibility

        // Create nodes
        const node = svg.append('g')
            .attr('class', 'nodes')
            .selectAll('circle')
            .data(graph.nodes)
            .enter().append('circle')
            .attr('r', 10)
            .attr('fill', d => color(d.group))
            .call(drag(simulation))
            .on('click', showMenu)  // Add click event listener
            .each(d => {
                // Initialize chat messages for each node
                chatMessages[d.id] = [];
                createChatTab(d.id); // Create a chat tab for each node
            });

        // Add labels to the nodes
        const label = svg.append('g')
            .attr('class', 'labels')
            .selectAll('text')
            .data(graph.nodes)
            .enter().append('text')
            .attr('class', 'node-label')
            .attr('dy', -15)
            .attr('dx', 12)
            .text(d => d.id);

        // Update positions of links and nodes on each tick
        simulation.on('tick', () => {
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);

            node
                .attr('cx', d => d.x)
                .attr('cy', d => d.y);

            label
                .attr('x', d => d.x)
                .attr('y', d => d.y);
        });

        // Color scale for the nodes
        function color(group) {
            const scale = d3.scaleOrdinal(d3.schemeSet3); // Using colorblind-friendly palette
            return scale(group);
        }

        // Drag functionality
        function drag(simulation) {
            function dragstarted(event, d) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }

            function dragged(event, d) {
                d.fx = event.x;
                d.fy = event.y;
            }

            function dragended(event, d) {
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }

            return d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended);
        }

        // Function to show menu on node click
        function showMenu(event, d) {
            event.stopPropagation();  // Prevents the immediate closing of the menu
            const menu = document.getElementById('menu');
            menu.style.display = 'block';
            menu.style.left = `${event.pageX}px`;
            menu.style.top = `${event.pageY}px`;

            // Close menu on clicking outside
            window.addEventListener('click', function closeMenu(e) {
                if (!menu.contains(e.target) && e.target.tagName !== 'circle') {
                    menu.style.display = 'none';
                    window.removeEventListener('click', closeMenu);
                }
            }, true);  // Use capture phase to avoid immediate close
        }

        // Function to handle menu options
        function handleOption(option) {
            alert(`Selected: ${option}`);
            const menu = document.getElementById('menu');
            menu.style.display = 'none';
        }
    }).catch(error => {
        console.error('Error loading the graph data:', error);
    });
}
