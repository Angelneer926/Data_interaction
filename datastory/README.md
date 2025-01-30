Website Link: https://fancy-gaufre-84610d.netlify.app/

This project aims to provide an accessible explanation of an ovarian cancer histopathological slide subtype classification model. The introduction starts with the basic background of the problem. To help people from different backgrounds understand the relevant concepts, the introduction is divided into three sections. This allows users to focus only on the content they are unfamiliar with, avoiding overly lengthy explanations that might cause disengagement.

Following the introduction, a navigation bar allows users to freely explore different sections by clicking on various tags. The first section, titled "Implementation Barriers," addresses two issues. The first is the inconsistency in the sizes of tumor slides across subtypes, which is demonstrated through a scatter plot. Users can click on different subtype combinations to compare them. The second issue is the high resolution of histopathological images. Together, these issues lead to the need for image segmentation and the application of a multi-instance approach in the model.

The second section, "Data Processing," showcases the basic flow of data handling in the model. 

The third section, which focuses on the core of the model—the attention mechanism—aims to show users what this abstract mechanism does by visualizing the weights of the small patches it outputs. A comparison button allows users to compare similarities between images from different sources.

The fourth section presents the model’s final results. Since the model addresses the issue of data imbalance, an animated bar chart will illustrate that the initial sample distribution across subtypes does not significantly impact the prediction results.

Additionally, when the mouse hovers over a subtitle about to leave the viewport, its background color will change, providing a dynamic visual cue.