<script>
    import * as d3 from 'd3';
    import {legendColor} from 'd3-svg-legend';

    export let data;
    export let fullData;

    let width = 500;
    let height = 500;

    let proj = d3.geoMercator()
        .scale(40000)
        .center([-73.55, 40.48])
        .translate([width, height]);
    let path = d3.geoPath().projection(proj);

    $: scale = d3.scaleLinear()
    .domain([d3.min(data.map((d) => +d.properties['Incident Count'])), 
             d3.median(data.map((d) => +d.properties['Incident Count'])), 
             d3.max(data.map((d) => +d.properties['Incident Count']))])
    .range(['blue', 'white', 'red']);
let legend;
    $: {	
            const colorLegend = legendColor()
                .shape('rect')
                .cells(9)
                .scale(scale);
            
            d3.select(legend)
                .call(colorLegend);
        }
</script>

<main>
    <svg {width} {height}>
        {#each data as d}
          <path style = "fill: {scale(+d.properties['Incident Count'])};"
            d={path(d)}/>
        {/each}
        {#each fullData as d}
          <path class = "geooverlay"
            d={path(d)}/>
        {/each}

        <g transform="translate({width - 67}, 30)"
              bind:this={legend} />
      </svg>
</main>

<style>
    .geooverlay {
      stroke: grey;
      stroke-width: 1px;
      fill: none;
    }
  </style>