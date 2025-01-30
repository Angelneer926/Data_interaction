---
toc: false
---

<div class="hero">
  <h1>Computational Neuroscience</h1>
  <h2>The goal of computational neuroscience is to reverse-engineer the brain, to understand how it works, and then how to apply that understanding to artificial intelligence.</h2>
</div>

<div class="subtitle-container">
  <h3 class="subtitle">Time Dimension</h3>
</div>

```js
const fruit = (await FileAttachment("./data/fruit.csv").csv({ typed: true }))
```

```js
const fruitdata = fruit.flatMap(d => fruit.columns.slice(1).map(fruit => ({date: d.date, fruit, value: d[fruit]})));

```

```js
const events = FileAttachment("./data/events.json").json();
```
```js
const forecast = FileAttachment("./data/forecast.json").json();
```

```js
const width = 500;
  const height = Math.min(500, width/2 );
const outerRadius = height / 2 - 10;
const innerRadius = outerRadius * 0.75;


const tau = 2 * Math.PI;


const svg = d3.create("svg")
    .attr("viewBox", [0, 0, width, height + 50]); 


svg.append("text")
    .attr("x", width / 2) 
    .attr("y", 20) 
    .attr("text-anchor", "middle") 
    .attr("font-size", "10px") 
    .attr("font-weight", "bold") 
    .attr("fill", "black") 
    .text("Multiple Disciplines Proportion");

const g = svg.append("g")
    .attr("transform", "translate(" + width / 2 + "," + (height / 2 + 25) + ")"); // 
const arc = d3.arc()
      .innerRadius(innerRadius)
      .outerRadius(outerRadius)
      .startAngle(0);

const background = g.append("path")
      .datum({endAngle: tau})
      .style("fill", "#ddd")
      .attr("d", arc);


const foreground = g.append("path")
      .datum({endAngle: 0})
      .style("fill", "orange")
      .attr("d", arc);

const yearLabel = g.append("text")
    .attr("x", 0) 
    .attr("y", 0) 
    .attr("text-anchor", "middle")
    .attr("font-size", "14px")
    .attr("font-weight", "bold")
    .attr("fill", "black");


function updateArc(angleFraction, year) {
  const newAngle = angleFraction * tau;


  foreground.transition()
      .duration(750)
      .attrTween("d", arcTween(newAngle));


  yearLabel.text(year);
}


function arcTween(newAngle) {
  return function(d) {
    const interpolate = d3.interpolate(d.endAngle, newAngle);
    return function(t) {
      d.endAngle = interpolate(t);
      return arc(d);
    };
  };
}


const anglesAndYears = [
  { angle: 0.0312, year: "2000" },
  { angle: 0.0114, year: "2005" },
  { angle: 0.0382, year: "2010" },
  { angle: 0.2099, year: "2015" },
  { angle: 0.2269, year: "2020" },
  { angle: 0.2412, year: "2024" }
];
let currentIndex = 0;


function cycleAngles() {
  const current = anglesAndYears[currentIndex];
  updateArc(current.angle, current.year); 
  currentIndex = (currentIndex + 1) % anglesAndYears.length; 
  setTimeout(cycleAngles, 1000); 
}


cycleAngles();


display(svg.node());


  
```

<div class="grid grid-cols-2" style="grid-auto-rows: 400px;">
  <div class="card">${
    resize((width) => Plot.plot({
  x: {line: true, insetRight: 70},
  y: {domain: [100, 1400], axis: null},
  marks: [
    Plot.line(fruitdata, {x: "date", y: "value", stroke: "fruit"}),
    Plot.text(fruitdata, {x: "date", y: "value", text: "value", fill: "currentColor", stroke: "#f4f5f6", strokeWidth: 8}),
    Plot.text(fruitdata, Plot.selectLast({x: "date", y: "value", text: "fruit", z: "fruit", textAnchor: "start", dx: 12, fontWeight: "bold"})) 
  ]
}))
  }</div>
  <div class="card">${
     svg.node()
  }</div>
</div>

```js
const length = (path) => d3.create("svg:path").attr("d", path).node().getTotalLength()
```



<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Embedding Observable Chart</title>
</head>
<body>
  <iframe width="80%" height="400" frameborder="0"
    src="https://observablehq.com/embed/a94c53cc57742cf2?cells=chart"></iframe>
</body>
</html>


<div class="subtitle-container">
  <h3 class="subtitle">Spatial Dimension</h3>
</div>

```js
const Scholar_Counts = FileAttachment("./data/country_counts.csv").csv({typed: true});
```

```js
const global = FileAttachment("./data/countries.json").json();
```
```js
const namemap = new Map(global.objects.countries.geometries.map(d => [d.properties.name, d.id]));
```
```js
const valuemap = new Map(Scholar_Counts.map(d => [d.Country, d.Count]));
```


```js
const Scholar_Counts_new = FileAttachment("./data/country_counts_new.csv").csv({typed: true});
```

```js
const valuemap_new = new Map(Scholar_Counts_new.map(d => [d.Country, d.Count]));
```



<div class="grid grid-cols-2" style="grid-auto-rows: 400px;">
  <div class="card">${
    resize((width) => Plot.plot({
  projection: "equal-earth",
  width: 600,
  height: 600/2,
  color: {scheme: "YlGnBu", unknown: "#ccc", label: "Scholar Counts", legend: true},
  marks: [
    Plot.geo(topojson.feature(global, global.objects.countries), Plot.centroid({
      fill: d => valuemap.get(d.properties.name),
      title: d => `${d.properties.name}\n${valuemap.get(d.properties.name)}`,
      tip: true
    })),
    Plot.geo(topojson.mesh(global, global.objects.countries, (a, b) => a !== b), {stroke: "white"})
 ]
}))
  }</div>
  <div class="card">${
    resize((width) => Plot.plot({
  projection: "equal-earth",
  width: 600,
  height: 600/2,
  color: {scheme: "YlGnBu", unknown: "#ccc", label: "Scholar Counts", legend: true},
  marks: [
    Plot.geo(topojson.feature(global, global.objects.countries), Plot.centroid({
      fill: d => valuemap_new.get(d.properties.name),
      title: d => `${d.properties.name}\n${valuemap_new.get(d.properties.name)}`,
      tip: true
    })),
    Plot.geo(topojson.mesh(global, global.objects.countries, (a, b) => a !== b), {stroke: "white"})
 ]
}))
  }</div>
</div>

```js
const nation_citations = FileAttachment("./data/nation_citations.csv").csv({typed: true});
```

```js
const valuemap_c = new Map(nation_citations.map(d => [d.Nation, d.Citations]));
```

```js
const nation_citations_new = FileAttachment("./data/nation_citations_new.csv").csv({typed: true});
```

```js
const valuemap_cnew = new Map(nation_citations_new.map(d => [d.Nation, d.Citations]));
```

<div class="grid grid-cols-2" style="grid-auto-rows: 400px;">
  <div class="card">${
    resize((width) => Plot.plot({
  projection: "equal-earth",
  width: 600,
  height: 600/2,
  color: {scheme: "YlGnBu", unknown: "#ccc", label: "Citations", legend: true},
  marks: [
    Plot.geo(topojson.feature(global, global.objects.countries), Plot.centroid({
      fill: d => valuemap_c.get(d.properties.name),
      title: d => `${d.properties.name}\n${valuemap_c.get(d.properties.name)}`,
      tip: true
    })),
    Plot.geo(topojson.mesh(global, global.objects.countries, (a, b) => a !== b), {stroke: "white"})
 ]
}))
  }</div>
  <div class="card">${
    resize((width) => Plot.plot({
  projection: "equal-earth",
  width: 600,
  height: 600/2,
  color: {scheme: "YlGnBu", unknown: "#ccc", label: "Citations", legend: true},
  marks: [
    Plot.geo(topojson.feature(global, global.objects.countries), Plot.centroid({
      fill: d => valuemap_cnew.get(d.properties.name),
      title: d => `${d.properties.name}\n${valuemap_cnew.get(d.properties.name)}`,
      tip: true
    })),
    Plot.geo(topojson.mesh(global, global.objects.countries, (a, b) => a !== b), {stroke: "white"})
 ]
}))
  }</div>
</div>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Embedding Observable Chart</title>
</head>
<body>
  <iframe width="80%" height="600" frameborder="0"
    src="https://observablehq.com/embed/845f5a168baec437?cells=chart"></iframe>
</body>
</html>



<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 4rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 1rem 0;
  padding: 1rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 80em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

.subtitle-container {
    margin-top: 3rem; 
  }

.subtitle {
    font-size: 36px; 
    font-weight: 600;
    color: var(--theme-foreground-muted); 
    text-align: left; 
    width: 100%; 
    margin-left: 2rem; 
    margin-bottom: 3rem;
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>
