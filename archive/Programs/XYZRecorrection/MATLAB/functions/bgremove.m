% Load the image
img = acquireImage();

% Convert the image to grayscale
gray_img = rgb2gray(img);

% Use global thresholding to convert the image to binary
threshold = graythresh(gray_img);
binary_img = im2bw(gray_img, threshold);

% Invert the binary image
binary_img = ~binary_img;

% Multiply the binary image with the original image to remove the background
img(repmat(~binary_img,[1 1 3])) = 0;

% Display the image
imshow(img);
