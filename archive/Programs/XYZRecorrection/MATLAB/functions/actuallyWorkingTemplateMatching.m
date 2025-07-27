function [x, y] = actuallyWorkingTemplateMatching(template)

[~, croppedImage, ~, ~] = findAndCropLaserRegion();
[I_SSD,I_NCC] = template_matching(template,croppedImage);

[y,x] = find(I_NCC==max(I_NCC(:)));
end

