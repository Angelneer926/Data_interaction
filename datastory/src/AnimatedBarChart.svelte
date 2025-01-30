<script>
  import { onMount } from "svelte";
  import * as d3 from "d3";

  let svg;
  let data1 = [
    { label: "HGSC", value: 217 },
    { label: "EC", value: 119 },
    { label: "MC", value: 41 },
    { label: "CC", value: 94 },
    { label: "LGSC", value: 42 },
  ];
  let data2 = [
    { label: "HGSC", value: 0.8571 },
    { label: "EC", value: 0.4167 },
    { label: "MC", value: 0.75 },
    { label: "CC", value: 1 },
    { label: "LGSC", value: 0.75 },
  ];

  let width = 900; // 600 * 1.5
  let height = 600; // 400 * 1.5
  let margin = { top: 20, right: 20, bottom: 60, left: 90 }; 
  let xScale, yScale;
  let isAnimating = false;
  let useData1 = true;

  const renderChart = () => {
    const svgSelection = d3.select(svg);
    svgSelection.selectAll("*").remove(); 

    xScale = d3
      .scaleBand()
      .domain(data1.map((d) => d.label))
      .range([margin.left, width - margin.right])
      .padding(0.3);

    const maxY = d3.max(data1, (d) => d.value);
    yScale = d3
      .scaleLinear()
      .domain([0, maxY])
      .nice()
      .range([height - margin.bottom, margin.top]);

    svgSelection
      .append("g")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(xScale).tickSize(10))
      .selectAll("text")
      .style("font-size", "16px"); 

    const yAxisGroup = svgSelection
      .append("g")
      .attr("class", "y-axis")
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(yScale));

    yAxisGroup
      .selectAll("text")
      .style("font-size", "10px");

    svgSelection
      .append("text")
      .attr("class", "y-axis-label")
      .attr("transform", "rotate(-90)")
      .attr("x", -height / 2 - 20) 
      .attr("y", margin.left / 2)
      .style("text-anchor", "middle")
      .style("font-size", "18px") 
      .text("Sample Counts");

    svgSelection
      .selectAll("rect")
      .data(data1)
      .enter()
      .append("rect")
      .attr("x", (d) => xScale(d.label))
      .attr("y", (d) => yScale(d.value))
      .attr("height", (d) => height - margin.bottom - yScale(d.value))
      .attr("width", xScale.bandwidth())
      .attr("fill", "#4CAF50");

    svgSelection
      .selectAll("text.label")
      .data(data1)
      .enter()
      .append("text")
      .attr("class", "label")
      .attr("x", (d) => xScale(d.label) + xScale.bandwidth() / 2)
      .attr("y", (d) => yScale(d.value) - 5)
      .attr("text-anchor", "middle")
      .style("font-size", "16px") // 增大柱子标签的字体大小
      .text((d) => d.value);
  };

  const animate = () => {
    if (isAnimating) return;
    isAnimating = true;

    const newData = useData1 ? data2 : data1; 
    const maxY = d3.max(newData, (d) => d.value);
    yScale.domain([0, maxY]); 

    const svgSelection = d3.select(svg);


    svgSelection
      .selectAll("rect")
      .data(newData)
      .transition()
      .duration(1000)
      .attr("y", (d) => yScale(d.value))
      .attr("height", (d) => height - margin.bottom - yScale(d.value));


    svgSelection
      .selectAll("text.label")
      .data(newData)
      .transition()
      .duration(1000)
      .attr("y", (d) => yScale(d.value) - 5)
      .text((d) => d.value);


svgSelection
  .select(".y-axis")
  .transition()
  .duration(1000)
  .call(d3.axisLeft(yScale))
  .selectAll("text")  
  .style("font-size", "16px");


    svgSelection
      .select(".y-axis-label")
      .transition()
      .duration(1000)
      .text(useData1 ? "Test Accuracy" : "Sample Counts");

  
    svgSelection
      .select(".y-axis")
      .transition()
      .duration(1000)
      .call(d3.axisLeft(yScale))
      .on("end", () => {
        isAnimating = false;
        useData1 = !useData1; 
      });
  };

  const reset = () => {
    useData1 = true; 
    renderChart();
  };

  onMount(() => {
    renderChart();
  });
</script>

<div>
  <svg bind:this={svg} width={width} height={height}></svg>
  <div style="margin-top: 20px;">
    <button on:click={animate}>Animate</button>
    <button on:click={reset}>Reset</button>
  </div>
</div>

<style>
  button {
    margin-right: 10px;
    padding: 10px 15px;
    font-size: 16px;
    cursor: pointer;
  }

  button:hover {
    background-color: #ddd;
  }
</style>
