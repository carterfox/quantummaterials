function [grayImage, laserX, laserY] = locateLaserPoint()

grayImage = rgb2gray(acquireImage());

%Laser is the maximum pixel value
binarized = grayImage > 0.85;

%denoise in case of outlier pixels
binarized = bwareaopen(binarized, 60);

%get coordinates of laser
object = regionprops(binarized, 'Centroid');
centroids = object.Centroid;
laserX = centroids(1,1);
laserY = centroids(1,2);

end

