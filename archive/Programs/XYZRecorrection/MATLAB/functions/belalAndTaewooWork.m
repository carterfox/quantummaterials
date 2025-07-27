
img = acquireImage();
imshow(img);
% Now let's convert into grayscale image
gray = rgb2gray(img);
imshow(gray);
%Get Fourier Transform of an image
F = fft2(gray_img);

%Get the centered spectrum
Fsh = fftshift(F);

%apply log transform
log_img = log(1+abs(Fsh));
    
sum = 0;
for i = 1:10
    for j = 1:10
        sum = sum + double(log_img(535 + i, 715 + j));
    end
end

avg = double(sum/100);

mappedVal = maptorange(avg, [0,20], [0,1000]);

