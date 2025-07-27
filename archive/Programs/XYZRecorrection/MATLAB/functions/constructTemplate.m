function [template] = constructTemplate(sampX, sampY)

[croppedImage, ~, ~] = findAndCropLaserRegion();


templateLength = 150;
templateWidth = 150;
cropCoords = [(sampX - templateLength/2) (sampY - templateWidth/2) templateLength templateWidth];
template = imcrop(croppedImage, cropCoords);

end

