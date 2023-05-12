# Principal Component Analysis explained visually

Created: Jul 13, 2020 9:22 AM
URL: https://setosa.io/ev/principal-component-analysis/

![fb-thumb.png](Principal%20Component%20Analysis%20explained%20visually%2032535dac32b24b3e96532845813e6275/fb-thumb.png)

### Explained Visually

with text by [Lewis Lehe](http://twitter.com/lewislehe)

Principal component analysis (PCA) is a technique used to emphasize variation and bring out strong patterns in a dataset. It's often used to make data easy to explore and visualize.

First, consider a dataset in only two dimensions, like (height, weight). This dataset can be plotted as points in a plane. But if we want to tease out variation, PCA finds a new coordinate system in which every point has a new (x,y) value. The axes don't actually mean anything physical; they're combinations of height and weight called "principal components" that are chosen to give one axes lots of variation.

Drag the points around in the following visualization to see PC coordinate system adjusts.