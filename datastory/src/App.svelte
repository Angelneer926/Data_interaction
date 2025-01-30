<script>
  import * as d3 from 'd3';
  import { onMount } from 'svelte';
  import Scrolly from "./Scrolly.svelte";
   import ScatterPlotWithDensity from './ScatterPlotWithDensity.svelte';
    import AnimatedBarChart from './AnimatedBarChart.svelte';

  let value = undefined;
    let attentionElement; 
  let fontSize = '1.75em'; 

  let showComparison = false; // This will control the visibility of the comparison image

  const toggleComparison = () => {
    showComparison = !showComparison; // Toggle visibility
  };
  const steps = ["Implementation Barriers😣", "Data Processing📑", "Attention Mechanism🧠", "Prediction results🔮"];

  
  let containers = [];
  let stepElements = [];

  let triggerElement;
  let isVisible = false;

  const handleScroll = () => {
  if (attentionElement) {
    const rect = attentionElement.getBoundingClientRect();
    if (rect.top <= 1000) {
      fontSize = '2.5em';  
    } else {
      fontSize = '1.75em';  
    }
  }
};
  
  const updateActiveStep = () => {
    let newValue = undefined; 
    

    stepElements.forEach((el, i) => {
      const rect = el.getBoundingClientRect();
      
      if (rect.top >= 0 && rect.top <= 200) {
        newValue = i;  
      }
    });

    value = newValue;
  };

  onMount(() => {
    stepElements = containers;
    window.addEventListener('scroll', updateActiveStep);
    updateActiveStep();

    const onScroll = () => {
      const rect = triggerElement.getBoundingClientRect();
      isVisible = rect.top < window.innerHeight && rect.bottom >= 0;
    };

    window.addEventListener("scroll", onScroll);
    onScroll(); 

    return () => {
      window.removeEventListener('scroll', updateActiveStep);
      window.removeEventListener("scroll", onScroll);
    };
    const handleScroll = () => {
    const rect = triggerElement.getBoundingClientRect();
    isVisible = rect.top < window.innerHeight && rect.bottom >= 0;
  };

  window.addEventListener("scroll", handleScroll);
  
  handleScroll();

  return () => {
    window.removeEventListener('scroll', updateActiveStep);
    window.removeEventListener("scroll", handleScroll);
  };
  });

  import { onDestroy } from "svelte";
  onDestroy(() => {
    window.removeEventListener('scroll', updateActiveStep);
  });
  let currentSlide = 0;

  const slides = [
    { title: "Ovarian Cancer", content: "A highly lethal malignancy in the female reproductive system, with <strong>low early detection rates</strong> due to nonspecific symptoms. While less common than breast cancer, it has a much <strong>higher mortality rate</strong>. The limited number of cases has slowed research progress, leaving it behind breast cancer in terms of study advancements. However, its high fatality risk has recently rekindled research interest." },
    { title: "Ovarian Cancer Subtypes", content: "Include <strong>HGSC, CCOC, ENOC, LGSC, and MUC</strong>, with HGSC accounting for approximately 70% of cases. These subtypes differ in cell morphology, etiology, molecular and genetic characteristics, and clinical features. A shift towards <strong>subtype-based treatments</strong> has emerged, such as the use of PARP inhibitors for HGSC patients, highlighting the growing importance of accurate subtype diagnosis in clinical practice." },
    { title: "Histopathological Imaging", content: "Essential for diagnosing ovarian cancer, helping to determine tumor type, malignancy, severity, and spread. They also provide key information for prognosis and personalized treatment. However, current manual analysis by pathologists is limited by <strong>resource shortages and varying expertise</strong>, highlighting the need for automated image analysis. Recently, <strong>deep learning</strong> has been applied to histopathological classification." }
  ];

  const nextSlide = () => {
    currentSlide = (currentSlide + 1) % slides.length;
  };

  const prevSlide = () => {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
  };

  const scrollToStep = (index) => {
    const stepElement = containers[index];
    if (stepElement) {
      stepElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };
  let data = [];

  const loadData = async () => {
    data = await d3.csv('/train.csv');
    data.forEach(d => {
      d.image_width = +d.image_width;
      d.image_height = +d.image_height;
    });
  };

  loadData();
</script>

<div class="info">
  <h1>Ovarian cancer histopathological image <br>subtype classification</h1>
  <div class="content">
    <img src="image/overall.jpg" alt="Description of image" class="left-align" />
    <div class="text-box">
      <div class="slider">
        {#each slides as slide, i}
          <div class="slide {currentSlide === i ? 'active' : ''}">
            <h2>{slide.title}</h2>
            <!-- Use {@html} to render HTML content -->
            <p>{@html slide.content}</p>
          </div>
        {/each}
      </div>
      <div class="arrows">
        <button on:click={prevSlide}>❮</button>
        <button on:click={nextSlide}>❯</button>
      </div>
    </div>
  </div>
  <mark>Active: {value}</mark>
</div>


<section>

  <div class="spacer" />

  <nav class="tags-bar">
  {#each steps as step, i}
    <button class="tag" on:click={() => scrollToStep(i)}>
      {step}
    </button>
  {/each}
</nav>
  
  <div bind:this={containers[0]}>
    <div class="step" class:active={value === 0}>
      <p class="bold-text">{steps[0]}</p>
    </div>
  </div>

  <div class="custom-content">
  <p>The morphological characteristics of tumors vary across different subtypes, leading to distinct image sizes in terms of both width and height for each tissue slice.</p>
</div>

<ScatterPlotWithDensity {data} />

<div class="custom-content">
  <p>At the same time, histopathological slides possess high resolution, which necessitates segmentation for facilitating subsequent processes such as training. This also addresses the issue of varying sizes mentioned earlier. However, it is important to note that this may result in the fragmentation of the complete tissue structure, potentially affecting subsequent classification.</p>
</div>

  <div bind:this={containers[1]}>
    <div class="step" class:active={value === 1}>
      <p class="bold-text">{steps[1]}</p>
    </div>
  </div>

  <div class="custom-content">
  <h2>Image Segmentation</h2>
</div>

<img src="image/tiling.png" alt="Description of image" style="width: 50%;" />

<div class="custom-content">
  <p>✨ Reducing computational load and avoiding memory constraints</p>
  <p>✨ Meeting the image size requirements of image processing algorithms</p>
  <p>✨ Facilitating the use of pixel-level annotations and analysis</p>
</div>

<div class="custom-content">
  <h2>Tissue extraction</h2>
</div>

<img src="image/Extraction.png" alt="Description of image" style="width: 55%;" />

<div class="custom-content">
  <p>✨ Identifying patches of interest rather than background</p>
</div>

<div class="custom-content">
  <h2>Feature extraction</h2>
</div>


<img src="image/feature.png" alt="Description of image" style="width: 80%;" />

<div class="custom-content">
  <p>✨ Better represent the key information in the image</p>
</div>

  <div bind:this={containers[2]}>
    <div class="step" class:active={value === 2}>
      <p class="bold-text">{steps[2]}</p>
    </div>
  </div>

  <div class="custom-content">
  <p>Due to limited human resources, the segmented patches are often unlabeled. To address this challenge, attention mechanisms are among the commonly adopted solutions. By calculating attention matrices to weight the image patches, these mechanisms enable the model to focus on diagnostically significant regions while reducing noise, thereby enhancing classification accuracy.</p>
</div>

<div class="custom-content">
  <p class="attention-text" bind:this={attentionElement} style="--font-size: {fontSize}">
    So, what exactly does the attention mechanism do?
  </p>
</div>

<div class="custom-content">
  <p>The image is a histopathological slide of a tumor area annotated by human experts, with red, green, and blue used to denote the tumor, stroma (healthy tissue), and necrosis (dead or dying non-cancerous tissue), respectively. 
</p>
</div>

<img src="image/notation.png" alt="Description of image" style="width: 95%;" />

<div class="interactive-text-box">
  <button on:click={toggleComparison}>Comparison</button>
  {#if showComparison}
    <div class="comparison-image">
      <img src="image/comparison.png" alt="Comparison Image" style="width: 100%;" />
    </div>
    <div class="custom-content">
  <p>The image shows the highest-weighted patches from the attention mechanism of my model. It can be observed that the high-weighted areas largely correspond to the tumor regions in the annotated data, which is consistent with expectations. Generally, only the tumor regions can be used to determine the subtype of ovarian cancer.
</p>
</div>
  {/if}
</div>

  <div bind:this={containers[3]}>
    <div class="step" class:active={value === 3}>
      <p class="bold-text">{steps[3]}</p>
    </div>
  </div>

  <AnimatedBarChart />

<div class="custom-content">
  <p>✨ My model has incorporated certain measures to address data imbalance, which allows it to achieve satisfactory prediction results even for subtypes with very few samples.
</p>
</div>

<div class="custom-content">
  <p>✨ My model performs poorly on EC, which aligns with the real-world observations of pathologists. ENOC is difficult to identify and is easily confused with other types.
</p>
</div>

  <div class="spacer" />
</section>





<style>
  .info {
    margin-top: 2em;
    text-align: center;
  }

  h1 {
    text-align: center;
    position: relative;
    margin-bottom: 1em;
  }

  .content {
    display: flex;
    justify-content: center; 
    align-items: stretch; 
    gap: 20px;
    margin-top: 20px;
  }

  .left-align {
    width: 50%;
    border-radius: 5px;
    object-fit: cover; 
  }

  .text-box {
    background-color: #f0f0f0;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    flex: 1;
    display: flex;
    flex-direction: column; 
    justify-content: flex-start; 
    text-align: left; 
    font-size: 1.2em; 
  }

  h2 {
    font-size: 1.5em; 
    text-align: center; 
  }

  p {
    font-size: 1.2em; 
    text-align: left; 
  }

  p strong, p b {
    font-weight: bold; 
  }

  .slider {
    display: flex;
    flex-direction: column;
    justify-content: flex-start; 
    align-items: flex-start; 
    text-align: left; 
  }

  .slide {
    display: none;
  }

  .slide.active {
    display: block;
  }

  .arrows {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
  }

  button {
    background-color: #ddd;
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    cursor: pointer;
  }

  button:hover {
    background-color: #bbb;
  }

  mark {
    padding: 0.5em;
    position: fixed;
    top: 0;
    right: 0;
  }

  /* 标签栏部分 */
  .tags-bar {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 40px; 
    padding: 10px;
    background-color: #ffffff;
    border-radius: 5px;
  }

  .tag {
    padding: 10px 20px;
    cursor: pointer;
    background-color: #ddd;
    border: none;
    border-radius: 5px;
    font-size: 1.2em;
  }

  .tag:hover {
    background-color: #bbb;
  }

  .sections-container {
    margin-top: 20px;
    padding: 0;
  }

  .step {
    width: 100%;
    height: auto;
    background: #ddd;
    margin-top: 1em;
    text-align: center;
    transition: background 100ms;
  }

  .step p {
    font-size: 2.5em;
  }

  .step.active {
    background: #aaa;
  }


  .small-text {
    font-size: 1.75em !important;
    text-align: left;
    font-weight: normal; 
  }
  .bold-text {
  font-weight: bold;
}
.custom-content {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  margin-top: 20px;
  text-align: center;
}

.custom-content h2 {
  font-size: 1.8em;
  margin-bottom: 10px;
}

.custom-content p {
  font-size: 1.75em;
  color: #555;
}

.hidden {
  opacity: 0;
  transform: translateY(20px); 
  transition: opacity 0.5s ease, transform 0.5s ease;
}


.visible {
  opacity: 1;
  transform: translateY(0); 
}

#trigger {
  height: 1px; 
  background: transparent; 
  margin-top: 100vh; 
}

.attention-text {
    color: red ! important;
    text-align: center;
    font-size: var(--font-size, 1.75em) ! important; 
    transition: font-size 0.3s ease;
  }

  .interactive-text-box {
    text-align: center;
    margin-top: 20px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .interactive-text-box button {
    padding: 10px 20px;
    font-size: 1.2em;
    cursor: pointer;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    transition: background-color 0.3s;
  }

  .interactive-text-box button:hover {
    background-color: #45a049;
  }

  .comparison-image {
    margin-top: 20px;
    display: block;
  }

  .comparison-image img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
  }
</style>
