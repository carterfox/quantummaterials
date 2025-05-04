function microns = locateSample(template, magnification)
    [locatedX, locatedY] = actuallyWorkingTemplateMatching(template);

    if magnification == 50
        constant = 3.45/50;
    elseif magnification == 20
        constant = 3.45/22.2;
    end


    x = locatedX - 200;
    y = 200 - locatedY;
    phi = atan(y/x);
    if (x > 0 && y > 0) || (x < 0 && y < 0)
        phiR = pi/4;
    else
        phiR = -pi/4;
    end
    
    phiC = phiR - phi;
    coords = [x y];
    rot = [cos(phiC) -sin(phiC) ; sin(phiC) cos(phiC)];
    result = coords.*rot;
    res = sum(result, 2);
    xprime = res(1);
    yprime = res(2);
    
    xDiff = xprime - x;
    yDiff = yprime - y;
    
    negativePhiCorrectionPixels = sqrt(xDiff^2 + yDiff^2)*sign(xDiff);
    positivePhiCorrectionPixels = sqrt(xprime^2 + yprime^2)*sign(xDiff);
    %Phi = pi/4
    micronX = constant*(negativePhiCorrectionPixels); 
    micronY = constant*(positivePhiCorrectionPixels);

    microns(1) = micronX;
    microns(2) = micronY;
    