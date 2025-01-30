<script>
  import * as d3 from 'd3';
	import {onMount} from 'svelte';
  import Map from './Map.svelte';
  import Histogram from './Histogram.svelte';

	let data = [];
  let fullData = [];
  let filter1 = [];
  let filter2 = [];
  let filter3 = [];

  let var1 = 'percentRooster';
  let var2 = 'percentUnsolved';
  let var3 = 'percent2024Year';

	onMount(async function() {
    let table = d3.csv('nyc-illegal-pets.csv', (d) => ({
          ...d,
          'Incident Zip': d['Incident Zip'].substring(0, 5),
          'Rooster Ratio': +d['Rooster Ratio'],
          'Ongoing Ratio': +d['Ongoing Ratio'],
          'Current Ratio': +d['Current Ratio']
        }));

    let geocoord = d3.json('nyc-zip-code.geojson')
      .then((d) => d.features);
    
    await Promise.all([table, geocoord]).then((values) => {
      let table = values[0];
      let geocoord = values[1];
      for (let i = 0; i < geocoord.length; i++) {
        let tract = geocoord[i].properties.postalCode;
        let found = false;
        let j = 0;
        while (!found && table.length > j) {
          if (table[j]['Incident Zip'] == tract) {
            found = true;
            data.push(geocoord[i]);
            data[data.length - 1].properties['Incident Count'] = table[j]['Incident Count']
            data[data.length - 1].properties['percentRooster'] = table[j]['Rooster Ratio']
            data[data.length - 1].properties['percentUnsolved'] = table[j]['Ongoing Ratio']
            data[data.length - 1].properties['percent2024Year'] = table[j]['Current Ratio']
            // grab other variables as needed
          } else {
            j++;
          }
        }
      }
      fullData = [...data];
    });
	});

function updateData() {
    if (filter1.length > 0 && filter2.length > 0 && filter3.length > 0) {
        data = fullData.filter((d) => (
            d.properties[var1] >= filter1[0] && d.properties[var1] < filter1[1] &&
            d.properties[var2] >= filter2[0] && d.properties[var2] < filter2[1] &&
            d.properties[var3] >= filter3[0] && d.properties[var3] < filter3[1]
        ));
    } else if (filter1.length > 0 && filter2.length > 0 && filter3.length == 0) {
        data = fullData.filter((d) => (
            d.properties[var1] >= filter1[0] && d.properties[var1] < filter1[1] &&
            d.properties[var2] >= filter2[0] && d.properties[var2] < filter2[1]
        ));
    } else if (filter1.length > 0 && filter3.length > 0 && filter2.length == 0) {
        data = fullData.filter((d) => (
            d.properties[var1] >= filter1[0] && d.properties[var1] < filter1[1] &&
            d.properties[var3] >= filter3[0] && d.properties[var3] < filter3[1]
        ));
    } else if (filter2.length > 0 && filter3.length > 0 && filter1.length == 0) {
        data = fullData.filter((d) => (
            d.properties[var2] >= filter2[0] && d.properties[var2] < filter2[1] &&
            d.properties[var3] >= filter3[0] && d.properties[var3] < filter3[1]
        ));
    } else if (filter1.length > 0 && filter2.length == 0 && filter3.length == 0) {
        data = fullData.filter((d) => (
            d.properties[var1] >= filter1[0] && d.properties[var1] < filter1[1]
        ));
    } else if (filter2.length > 0 && filter1.length == 0 && filter3.length == 0) {
        data = fullData.filter((d) => (
            d.properties[var2] >= filter2[0] && d.properties[var2] < filter2[1]
        ));
    } else if (filter3.length > 0 && filter1.length == 0 && filter2.length == 0) {
        data = fullData.filter((d) => (
            d.properties[var3] >= filter3[0] && d.properties[var3] < filter3[1]
        ));
    } else {
        data = [...fullData];
    }
}

</script>

<main>
  <h1>New York Illegal Pets</h1>
  <div class="flex-container row">
    <div class="map"><Map data={data} fullData={fullData}></Map></div>
    <div class="flex-container col">
      <div class="hist"><Histogram data={data} fullData={fullData} variable={var1} bind:filter={filter1} update={updateData}></Histogram></div>
      <div class="hist"><Histogram data={data} fullData={fullData} variable={var2} bind:filter={filter2} update={updateData}></Histogram></div>
      <div class="hist"><Histogram data={data} fullData={fullData} variable={var3} bind:filter={filter3} update={updateData}></Histogram></div>
    </div>
  </div>
</main>

<style>
  .flex-container {

    display: flex;
    
    justify-content: center;  
    /* flex-flow: row; */ 
    

    height: 100%;
    padding: 15px;
    gap: 5px;

  }

  .flex-container > div{
    padding: 8px;
  }

  .flex-container .row {
    flex-direction: row;  
  }

  .flex-container .col {
    flex-direction: column;  
  }

  .map { 
    /* flex:1 1 auto; */
    flex-grow:1;
  }
			
  .hist { 
    /* flex:0 1 auto; */
    flex-grow:0;
  }
			

</style>

