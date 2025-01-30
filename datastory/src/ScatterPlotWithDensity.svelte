<script>
  import * as d3 from 'd3';

  export let data = [];
  export let selectedLabels = new Set();  

  const colorScale = d3.scaleOrdinal(d3.schemeCategory10); 

  const drawChart = () => {
    const width = 800;
    const height = 500;
  
    d3.select('#scatter-plot').html('');

    const filteredData = data.filter(d => selectedLabels.size === 0 || selectedLabels.has(d.label));

    const svgScatter = d3.select('#scatter-plot')
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    const xScale = d3.scaleLinear()
      .domain([d3.min(filteredData, d => d.image_width), d3.max(filteredData, d => d.image_width)])
      .range([50, width - 50]);

    const yScale = d3.scaleLinear()
      .domain([d3.min(filteredData, d => d.image_height), d3.max(filteredData, d => d.image_height)])
      .range([height - 50, 50]);


    svgScatter.selectAll('circle')
      .data(filteredData)
      .enter().append('circle')
      .attr('cx', d => xScale(d.image_width))
      .attr('cy', d => yScale(d.image_height))
      .attr('r', 5)
      .attr('fill', d => selectedLabels.has(d.label) ? colorScale(d.label) : '#ddd')
      .attr('stroke', '#000')
      .attr('stroke-width', 1);

    svgScatter.append('g')
      .attr('transform', `translate(0, ${height - 50})`)
      .call(d3.axisBottom(xScale));

    svgScatter.append('g')
      .attr('transform', `translate(50, 0)`)
      .call(d3.axisLeft(yScale));
  };

  const toggleLabel = (label) => {
    if (selectedLabels.has(label)) {
      selectedLabels.delete(label);
    } else {
      selectedLabels.add(label);
    }
    drawChart();  
  };

  const resetFilter = () => {
    selectedLabels.clear();
    drawChart();
  };

  $: data, drawChart();
</script>

<style>
  .scatter-container {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
    margin-top: 20px;
  }

  #scatter-plot {
    flex: 3;
  }

  .legend {
    margin-top: 20px;
    display: flex;
    gap: 10px;
    justify-content: center;
  }

  .legend button {
    padding: 10px 20px;
    cursor: pointer;
    background-color: #ddd;
    border: none;
    border-radius: 5px;
  }

  .legend button:hover {
    background-color: #bbb;
  }
</style>

<div class="scatter-container">
  <div id="scatter-plot"></div>
</div>

<div class="legend">
  <button on:click={() => toggleLabel('HGSC')}>HGSC</button>
  <button on:click={() => toggleLabel('CC')}>CC</button>
  <button on:click={() => toggleLabel('EC')}>EC</button>
  <button on:click={() => toggleLabel('LGSC')}>LGSC</button>
  <button on:click={() => toggleLabel('MC')}>MC</button>
  <button on:click={resetFilter}>Reset</button>
</div>
