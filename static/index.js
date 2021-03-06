
var start = function(name){

    console.log(name);

    d3.csv(name, function(error, links) {

        var nodes = {};

        var a = links.reduce(function (acc, curr) {

            Object.values(curr).forEach(function(it){

                if(typeof acc[it] == 'undefined') {
                    acc[it] = 1;
                }
                else {
                    acc[it] += 1;
                }
            })
                return acc;
            }, {});

        console.log(a);



        // Compute the distinct nodes from the links.
        links.forEach(function(link) {
            link.source = nodes[link.source] ||
                (nodes[link.source] = {name: link.source});
            link.target = nodes[link.target] ||
                (nodes[link.target] = {name: link.target});

        });

        var width = 960,
            height = 500,
            colors = d3.scale.category10(),
            count = 10;


        var force = d3.layout.force()
            .nodes(d3.values(nodes))
            .links(links)
            .size([width, height])
            .linkDistance(90)
            .charge(-300)
            .on("tick", tick)
            .start();

        var svg = d3.select("#append").append("svg:svg")
            .attr("width", width)
            .attr("height", height);



        // build the arrow.
        svg.append("svg:defs").selectAll("marker")
            .data(["end"])      // Different link/path types can be defined here
            .enter().append("svg:marker")    // This section adds in the arrows
            .attr("id", String)
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 15)
            .attr("refY", -1.5)
            .attr("markerWidth", 10)
            .attr("markerHeight", 10)
            .attr("orient", "auto")
            .append("svg:path")
            .attr("d", "M0,-5L10,0L0,5");

        // add the links and the arrows
        var path = svg.append("svg:g").selectAll("path")
            .data(force.links())
            .enter().append("svg:path")
            //    .attr("class", function(d) { return "link " + d.type; })
            .attr("class", "link")
            .attr("marker-end", "url(#end)");

        // define the nodes
        var node = svg.selectAll(".node")
            .data(force.nodes())
            .enter().append("g")
            .attr("class", "node")
            .call(force.drag);

        // add the nodes
        node.append("circle")
            .attr("r", function(d) { return d.radius = 10 * (a[d.name]/2)})
            .style("fill", function(d, i) { return colors(i); });


        // add the text
        node.append("text")
            .attr("x", 12)
            .attr("dy", ".35em")
            .text(function(d) { return d.name; });

        // add the curvy lines
        function tick() {
            path.attr("d", function(d) {
                var dx = d.target.x - d.source.x,
                    dy = d.target.y - d.source.y,
                    dr = Math.sqrt(dx * dx + dy * dy);
                    offsetX = (dx * d.target.radius) / 300;
                    offsetY = (dy * d.target.radius) / 300;

                return "M" +
                    d.source.x + "," +
                    d.source.y + "A" +
                    dr + "," + dr + " 0 0,1 " +
                    d.target.x + "," +
                    d.target.y;
            });

            node
                .attr("transform", function(d) {
                    return "translate(" + d.x + "," + d.y + ")"; });
        }

    });

}
