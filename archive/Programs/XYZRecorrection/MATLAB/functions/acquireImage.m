function [img] = acquireImage()

[img, maxPixelValue] = SC135SoftwareTrigger();
%normalize the image
img = img/maxPixelValue;
