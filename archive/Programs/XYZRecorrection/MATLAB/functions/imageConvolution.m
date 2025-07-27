function [convolvedImage] = imageConvolution(referenceImage)
%grab the current frame
actualImage = acquireImage();
%convert both to grayscale
actualImage = im2gray(actualImage);

referenceImage = im2gray(referenceImage);

%convolve the current frame with the reference frame
convolvedImage = conv2(actualImage, referenceImage)/(2^24-1);

