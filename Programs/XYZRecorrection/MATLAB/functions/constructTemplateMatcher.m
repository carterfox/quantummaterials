function template = constructTemplateMatcher(sampleX, sampleY)

[grayImage, ~, ~, ~] = findAndCropLaserRegion();

templateLength = 70;
templateWidth = 70;
cropCoords = [(sampleX - templateLength/2) (sampleY - templateWidth/2) templateLength templateWidth];
template = imcrop(grayImage, cropCoords);
end

