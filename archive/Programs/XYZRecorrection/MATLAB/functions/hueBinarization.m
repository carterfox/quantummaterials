function [denoised] = hueBinarization(RGBImage)
%convert image to hsv
hsvImage = rgb2hsv(RGBImage);
%separate h s v channels and just grab the hue 
[h] = imsplit(hsvImage);

%binarize the hue to isolate the sample
binarizedHue = imbinarize(h);
denoised = bwareaopen(binarizedHue, 20);

end

