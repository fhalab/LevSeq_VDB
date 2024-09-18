// Function to update the color scale and redraw the heatmap
function updateColor(selectedColumn, svg, myColor, data, div_id) {
    let currentColumn = selectedColumn;
    const colorDomain = d3.extent(data, function (d) {
        return +d[currentColumn];
    });
    myColor.domain(colorDomain);
    let colourScale = myColor;
    const domain = colourScale.domain();

    svg.selectAll("rect")
        .transition()
        .duration(500)
        .style("fill", function (d) {
            return myColor(d[currentColumn]);
        });

    // Add in the colour scale
    const width = 100;
    const height = 150;
    
    const paddedDomain = fc.extentLinear()
  		.pad([0.1, 0.1])
  		.padUnit("percent")(domain);
		const [min, max] = paddedDomain;
		const expandedDomain = d3.range(min, max, (max - min) / height);
    
    const xScale = d3
    	.scaleBand()
    	.domain([0, 1])
    	.range([0, width]);
    
    const yScale = d3
    	.scaleLinear()
    	.domain(paddedDomain)
    	.range([height, 0]);
    
    const svgBar = fc
      .autoBandwidth(fc.seriesSvgBar())
      .xScale(xScale)
      .yScale(yScale)
      .crossValue(0)
      .baseValue((_, i) => (i > 0 ? expandedDomain[i - 1] : 0))
      .mainValue(d => d)
      .decorate(selection => {
        selection.selectAll("path").style("fill", d => colourScale(d));
      });
    
    const axisLabel = fc
      .axisRight(yScale)
      .tickValues([...domain, (domain[1] + domain[0]) / 2])
      .tickSizeOuter(0);
      
    // Clear before we add it
    d3.select(div_id).select('#legendID').remove();

    const legendSvg = d3.select(div_id).append("svg")
        .attr('id', 'legendID')
    	.attr("height", height)
    	.attr("width", width);
    
    const legendBar = legendSvg
    	.append("g")
    	.datum(expandedDomain)
    	.call(svgBar);
    
    legendSvg.append("g")
    	.attr("transform", `translate(${width/4})`)
      .datum(expandedDomain)
      .call(axisLabel)
      .select(".domain")
      .attr("visibility", "hidden");

}


function make_heatmap(all_data, div_id, dropdown_id, colour_column, plate_id, currentPlateId) {
    // Creates a headmap based on a dataframe
    let currentColumn = colour_column;
    // If no plate ID has been provided then use the first plate
    plateids = Array.from(new Set(all_data.map(d => d.Plate))) // just get the first element

    if (currentPlateId === '') {
        currentPlateId = plateids[0]
    }
    // Update the data to only be the data associated with the current plate
    let data = []
    for (let di in all_data) {
        d = all_data[di]
        if (d.Plate === currentPlateId) {
            data.push(d)
        }
    }
    // Create a dropdown
    d3.select(plate_id)
        .selectAll("select")
        .data([null]) // Empty data for binding
        .enter()
        .append("select")
        .on("change", function (event) {
            // Remake the heatmap
            make_heatmap(all_data, div_id, dropdown_id, colour_column, plate_id, this.value);
        })
        .selectAll("option")
        .data(plateids)
        .enter()
        .append("option")
        .text(function (d) {
            return d;
    });

    const margin = {top: 80, right: 25, bottom: 30, left: 40},
        width = 800 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

    // append the svg object to the body of the page after checking we have removed it
    d3.select(div_id).select("svg").remove();

    const svg = d3.select(div_id)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);


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
    // Clear first 
    d3.select(dropdown_id).selectAll("*").remove();

    // Create a dropdown
    d3.select(dropdown_id)
        .selectAll("select")
        .data([null]) // Empty data for binding
        .enter()
        .append("select")
        .on("change", function (event) {
            updateColor(this.value, svg, myColor, data, div_id);
        })
        .selectAll("option")
        .data(columnNames)
        .enter()
        .append("option")
        .text(function (d) {
            return d;
        });

    // Initial column for coloring

    // Color scale - Update this in the updateColor function
    const myColor = d3.scaleSequential()
        .interpolator(d3.interpolateViridis);

    // Initial call to update colors
    updateColor(currentColumn, svg, myColor, data, div_id);

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
            return myColor(d.value)
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
        .text("Plate " + currentPlateId);

    // Add subtitle to graph
    svg.append("text")
        .attr("x", 0)
        .attr("y", -20)
        .attr("text-anchor", "left")
        .style("font-size", "14px")
        .style("fill", "grey")
        .style("max-width", 400)
        .text("Variant and activity data");

    updateColor(currentColumn, svg, myColor, data);
}
