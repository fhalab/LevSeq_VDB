
// Uses: https://github.com/wilzbach/msa which is now dead alas.
// parsed array of the sequences
// Note had to use an updated version of msa viewer: https://github.com/wilzbach/msa/issues/257
// Bless the souls of MrTomRod from 2021 and https://github.com/guignonv
//if (msadata !== undefined) {
 //   var seqs =  msa.io.fasta.parse(fasta);
//
//       var m = msa({
//           el: document.getElementById("msadiv"),
//          seqs: seqs
 //   });
  //  m.render();
//}
// Assuming this JavaScript is in your_script.js mentioned in the HTML
var div2 = document.getElementById("msadiv");
div2.style.display = "block"; // Change this depending on how you want the div to be displayed

const cellSize = 20; // Size of the cell for each nucleotide or amino acid
const margin2 = {top: 80, right: 25, bottom: 30, left: 40},
  width2 = 1000 - margin2.left - margin2.right,
  height2 = 600 - margin2.top - margin2.bottom;

// append the svg object to the body of the page
const svg2 = d3.select("#msadiv")
.append("svg")
  .attr("width", width2 + margin2.left + margin2.right)
  .attr("height", height2 + margin2.top + margin2.bottom)
.append("g")
  .attr("transform", `translate(${margin2.left}, ${margin2.top})`);

const sequenceGroup = svg2.selectAll("g")
  .data(msadata)
  .enter()
  .append("g")
  .attr("transform", (d, i) => `translate(0, ${i * cellSize})`);

sequenceGroup.each(function(d, i) {
  const sequence = d.seqs;
  const g = d3.select(this);
  g.selectAll("rect")
    .data(seqs.split(''))
    .enter()
    .append("rect")
    .attr("x", (d, i) => i * cellSize)
    .attr("width", cellSize)
    .attr("height", cellSize)
    .attr("class", "cell")
    .style("fill", d => d === "-" ? "#ddd" : "#eee");

  g.selectAll("text")
    .data(seqs.split(''))
    .enter()
    .append("text")
    .attr("x", (d, i) => i * cellSize + cellSize / 2)
    .attr("y", cellSize / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", "middle")
    .text(d => d)
    .attr("class", "sequence");
});


        const margin = {top: 80, right: 25, bottom: 30, left: 40},
            width = 1000 - margin.left - margin.right,
            height = 600 - margin.top - margin.bottom;

        // append the svg object to the body of the page
        const svg = d3.select("#my_dataviz")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${margin.left}, ${margin.top})`);

        var data = {{df | safe}};

        // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
        const myGroups = Array.from(new Set(data.map(d => d.group)))
        const myVars = Array.from(new Set(data.map(d => d.variable)))

        // Build X scales and axis:
        const x = d3.scaleBand()
            .range([0, width])
            .domain(myGroups)
            .padding(0.05);
        svg.append("g")
            .style("font-size", 15)
            .attr("transform", `translate(0, ${height})`)
            .call(d3.axisBottom(x).tickSize(0))
            .select(".domain").remove()

        // Build Y scales and axis:
        const y = d3.scaleBand()
            .range([height, 0])
            .domain(myVars)
            .padding(0.05);
        svg.append("g")
            .style("font-size", 15)
            .call(d3.axisLeft(y).tickSize(0))
            .select(".domain").remove()

        // Extract column names for the dropdown
        const columnNames = columns.map(column => column.title).filter(function (title) {
            return title !== "group" && title !== "variable";
        });

        // Create a dropdown
        d3.select("#dropdown")
            .selectAll("select")
            .data([null]) // Empty data for binding
            .enter()
            .append("select")
            .on("change", function (event) {
                updateColor(this.value);
            })
            .selectAll("option")
            .data(columnNames)
            .enter()
            .append("option")
            .text(function (d) {
                return d;
            });

        // Initial column for coloring
        let currentColumn = 'RT [min]';

        // Color scale - Update this in the updateColor function
        const myColor = d3.scaleSequential()
            .interpolator(d3.interpolateInferno);

        // Function to update the color scale and redraw the heatmap
        function updateColor(selectedColumn) {
            currentColumn = selectedColumn;
            const colorDomain = d3.extent(data, function (d) {
                return +d[currentColumn];
            });
            myColor.domain(colorDomain);

            svg.selectAll("rect")
                .transition()
                .duration(500)
                .style("fill", function (d) {
                    return myColor(d[currentColumn]);
                });
        }

        // Initial call to update colors
        updateColor(currentColumn);

        // create a tooltip
        const tooltip = d3.select("#tooltip")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "2px")
            .style("border-radius", "5px")
            .style("padding", "5px")

        // Three function that change the tooltip when user hover / move / leave a cell
        const mouseover = function (event, d) {
            tooltip
                .style("opacity", 1)
            d3.select(this)
                .style("stroke", "black")
                .style("opacity", 1)
        }
        const mousemove = function (event, d) {
            tooltip
                .html(currentColumn + ": " + d[currentColumn])
                .style("left", (event.x) + "px")
                .style("top", (event.y) + "px")
                .style("position", "absolute")
        }
        const mouseleave = function (event, d) {
            tooltip
                .style("opacity", 0)
            d3.select(this)
                .style("stroke", "none")
                .style("opacity", 0.8)
        }

        // add the squares
        svg.selectAll()
            .data(data, function (d) {
                return d.group + ':' + d.variable;
            })
            .join("rect")
            .attr("x", function (d) {
                return x(d.group)
            })
            .attr("y", function (d) {
                return y(d.variable)
            })
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("width", x.bandwidth())
            .attr("height", y.bandwidth())
            .style("fill", function (d) {
                return myColor(d[currentColumn])
            })
            .style("stroke-width", 4)
            .style("stroke", "none")
            .style("opacity", 0.8)
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave)

        // Assuming you have the previous heatmap setup, right after the rectangles are added and styled:
        svg.selectAll()
            .data(data, function (d) {
                return d.group + ':' + d.variable;
            })
            .join("text")  // Add this line to create text elements for each data point
            .attr("x", function (d) {
                return x(d.group) + x.bandwidth() / 2;
            })  // Position in the center of the cell
            .attr("y", function (d) {
                return y(d.variable) + y.bandwidth() / 2;
            })  // Position in the center of the cell
            .attr("dy", ".35em")  // Vertically center align the text
            .attr("text-anchor", "middle")  // Horizontally center the text
            .text(function (d) {
                return d.Mutations;
            })  // Set the text to the value of the cell
            .style("fill", "black")  // Set the text color
            .style("font-size", "10px")  // Set the text size
            .style("pointer-events", "none")  // Make text non-interactive


        // Add title to graph
        svg.append("text")
            .attr("x", 0)
            .attr("y", -50)
            .attr("text-anchor", "left")
            .style("font-size", "22px")
            .text("Plate 1");

        // Add subtitle to graph
        svg.append("text")
            .attr("x", 0)
            .attr("y", -20)
            .attr("text-anchor", "left")
            .style("font-size", "14px")
            .style("fill", "grey")
            .style("max-width", 400)
            .text("Variant and activity data");