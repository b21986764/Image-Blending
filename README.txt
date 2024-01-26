Image Blending Project

Link to drive that include images: https://drive.google.com/drive/folders/1MBiyqjETRNbQDl_ZIkNc9mCEwh3CdAoC?usp=sharing

Overview
This project demonstrates a basic image blending technique using Python and OpenCV. It involves downsampling and upsampling images to create Gaussian and Laplacian pyramids, which are then used to blend two images together.

Requirements
- Python
- OpenCV library

Files
- Pyramids.py: Main script for image blending.

How to Run
1. Place two images you want to blend in the project directory.
2. Run the Pyramids.py script.
3. Select the Region of Interest (ROI) from the second image.
4. The script will blend the images and display the result.

Process Overview
1. Load Images: Two images are loaded and resized to the same dimensions.
2. ROI Selection: A Region of Interest is selected on the second image.
3. Pyramid Construction: Gaussian and Laplacian pyramids are constructed for both images.
4. Mask Creation: A mask is created for blending based on the selected ROI.
5. Blending: The pyramids are blended according to the mask.
6. Result: The final blended image is displayed and saved.

Output
- The script outputs a blended image based on the ROI selected.

