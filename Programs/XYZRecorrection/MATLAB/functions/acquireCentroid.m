function [C, BB] = acquireCentroid(BWImage)
%ACQUIRECENTROID gets center of mass of sample given a binarized image and
%optionally bounding boxes
object = regionprops(BWImage, 'BoundingBox', 'Centroid');
C = object(1).Centroid;
BB = object(1).BoundingBox;
end

