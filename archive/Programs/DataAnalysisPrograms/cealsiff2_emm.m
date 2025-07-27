function out=cealsiff2_emm(x,xxz,zxx,zzz,xyz,xzy,zxy,d)
%when MATLAB fits using a custom function, it passes garbage values into
%the function just to test if the function works as expected. The next four
%lines are to deal with the garbage values and produce an output so that
%MATLAB does not consider the function unusable for fitting. If you comment
%out these four lines, you will see why they are needed: MATLAB will not be
%able to fit the data.
if length(x)<=2
    out = ones(size(x))+xxz+zxx+zzz+d;
    return
end

%split it up into SS, SP, PP, PS in that order by assuming that each
%response is given the same size of the xd and yd vectors.

l1 =length(x)/4+1; 
l2 =length(x)/2+1; 
l3 =3*length(x)/4+1; 
% l1 =length(x)/2+1; 

%%Now define all the responses. Some involve the parameter th, which is a
%%parameter to rotate the whole data set if the crystal was slightly off
%%orientation in the setup.

%eee responses

    function med = SSeee(x,xxz,zxx,zzz,d)
         med = (1/32).*cos(x).^2.*(6.*xxz+3.*zxx+zzz+((-2).*xxz+(-1).*zxx+zzz).*cos(2.*x)).^2;

    end
    function med = SPeee(x,xxz,zxx,zzz,d)
         med = (1/8).*sin(x).^2.*(((-2).*xxz+zxx+zzz).*cos(x).^2+2.*zxx.*sin(x).^2).^2;
    end
    function med = PPeee(x,xxz,zxx,zzz,d)
         med = (1/8).*((2.*xxz+zxx+zzz).*cos(x).^2+2.*zxx.*sin(x).^2).^2;


    end
    function med = PSeee(x,xxz,zxx,zzz,d)
         med = 2.*xxz.^2.*cos(x).^2.*sin(x).^2;

    end

%eem responses

    function med = SSeem(x,xyz,xzy,zxy,d)
        med = (1/4).*(xzy+zxy).^2.*cos(x).^2;
    end
    function med = SPeem(x,xyz,xzy,zxy,d)
        med = (1/4).*(xyz+(-1).*zxy).^2.*sin(x).^2;
    end
    function med = PPeem(x,xyz,xzy,zxy,d)
       med=(1/16).*((-1).*xyz+xzy+2.*zxy+(xyz+xzy).*cos(2.*x)).^2;
    end
    function med = PSeem(x,xyz,xzy,zxy,d)
        med = (1/16).*(xyz+xzy).^2.*sin(2.*x).^2;
    end

%emm responses


    function med = SSemm(x,xyz,xzy,zxy,d)
        med = (1/8).*cos(x).^2.*(2.*xzy.*cos(x).^2+((-2).*xyz+xzy+zxy).*sin(x).^2).^2;
    end
    function med = SPemm(x,xyz,xzy,zxy,d)
        med = (1/32).*(6.*xyz+3.*xzy+zxy+(2.*xyz+xzy+(-1).*zxy).*cos(2.*x)).^2.*sin(x).^2;
    end
    function med = PPemm(x,xyz,xzy,zxy,d)
        med = (1/8).*(2.*xzy.*cos(x).^2+(2.*xyz+xzy+zxy).*sin(x).^2).^2;
    end
    function med = PSemm(x,xyz,zxx,zzz,d)
        med = 2.*xyz.^2.*cos(x).^2.*sin(x).^2;
    end

%mee responses

    function med = SSmee(x,xyz,xzy,zxy)
        med = xyz.^2.*cos(x).^2;
    end
    function med = SPmee(x,xyz,xzy,zxy)
        med = 0;
    end
    function med = PPmee(x,xyz,xzy,zxy)
        med = xyz.^2.*cos(x).^4;
    end
    function med = PSmee(x,xyz,zxx,zzz)
        med = xyz.^2.*cos(x).^2.*sin(x).^2;
    end
% 
% %mem responses
% 
    function med = SSmem(x,xyz,xzy,zxy,d)
        med = (1/32).*cos(x).^2.*(xyz+(-3).*d+xzy+(-1).*zxy+(-1).*(xyz+d+xzy+(-1).*zxy).*cos(2.*x)).^2;
    end
    function med = SPmem(x,xyz,xzy,zxy,d)
        med = (1/32).*((-3).*xyz+d+xzy+(-1).*zxy+(xyz+d+xzy+(-1).*zxy).*cos(2.*x)).^2.*sin(x).^2;
    end
    function med = PPmem(x,xyz,xzy,zxy,d)
        med = (1/2).*(d.*cos(x).^2+(-1).*xyz.*sin(x).^2).^2;
    end
    function med = PSmem(x,xyz,xzy,zxy,d)
        med = (1/32).*(xyz+d+(-1).*xzy+zxy).^2.*sin(2.*x).^2;
    end
% 
% %mmm responses
% 
    function med = SSmmm(x,xyz,xzy,zxy)
        med = 0;
    end
    function med = SPmmm(x,xyz,xzy,zxy)
        med = xyz.^2.*sin(x).^2;
    end
    function med = PPmmm(x,xyz,xzy,zxy)
        med = xyz.^2.*sin(x).^4;
    end
    function med = PSmmm(x,xyz,zxx,zzz)
        med = xyz.^2.*cos(x).^2.*sin(x).^2;
    end


out = zeros(size(x));


for i=1:length(x)
    %the first 1/4 of the data will be fit as SSeee
    if i>0 && i<l1
        out(i) = SSeee(x(i),xxz,zxx,zzz,d)+ SSeem(x(i),xyz,xzy,zxy,d);
    %the second 1/4 of the data will be fit as SPeee
    elseif i>=l1 && i<l2
        out(i) = SPeee(x(i),xxz,zxx,zzz,d)+ SPeem(x(i),xyz,xzy,zxy,d);
    %the third 1/4 of the data will be fit as PSeee
    elseif i>=l2 && i<l3
        out(i) = PSeee(x(i),xxz,zxx,zzz,d)+ PSeem(x(i),xyz,xzy,zxy,d);
    %the fourth 1/4 of the data will be fit as PPeee
    else 
        out(i) = PPeee(x(i),xxz,zxx,zzz,d) + PPeem(x(i),xyz,xzy,zxy,d);
    end
end

end