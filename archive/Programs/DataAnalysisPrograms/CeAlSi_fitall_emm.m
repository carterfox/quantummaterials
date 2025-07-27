close all
clear;

Wavelength=800;

s1=num2str(Wavelength);
s2=num2str(Wavelength/2);
strPP='CeAlSi-300.0K-SHG-PP-nm-nm-001.txt';
strPS='CeAlSi-300.0K-SHG-PS-nm-nm-001.txt';
strSS='CeAlSi-300.0K-SHG-PP-nm-nm-002.txt';
strSP='CeAlSi-300.0K-SHG-PS-nm-nm-002.txt';
 filename1 = insertAfter(strPP,'PP-',s1);
    filenamePP=insertBefore(filename1,'nm-001',s2);
    
    filename2 = insertAfter(strPS,'PS-',s1);
    filenamePS=insertBefore(filename2,'nm-001',s2);
    
     filename3 = insertAfter(strSS,'PP-',s1);
    filenameSS=insertBefore(filename3,'nm-002',s2);
    
    filename4 = insertAfter(strSP,'PS-',s1);
    filenameSP=insertBefore(filename4,'nm-002',s2);
    
PP = dlmread(filenamePP);
PS = dlmread(filenamePS);
SS = dlmread(filenameSS);
SP = dlmread(filenameSP);

%------------------------------------------------------------------------


%operations to prepare the data: turn all angles into radians for the xx(:,1) part of the data sets. Then, remove
%offsets from the xx(:,2) part of the data sets.
SS(:,1) = SS(:,1)*pi/180;
% offs = min(SS(:,2));
offs = min(PS(:,2));
SS(:,2) = SS(:,2) - min(SS(:,2));
SP(:,1) = SP(:,1)*pi/180;
% SP(:,2) = SP(:,2) - min(SP(:,2));
SP(:,2) = SP(:,2) - min(SP(:,2));
PS(:,1) = PS(:,1)*pi/180;
PS(:,2) = PS(:,2) - offs;
PP(:,1) = PP(:,1)*pi/180;
PP(:,2) = PP(:,2) - offs;

% PP(:,2) = PP(:,2)- min(PP(:,2));

%--------------------------------------------------------------------------



xd = cat(1,SS(:,1),SP(:,1),PS(:,1),PP(:,1));
yd = cat(1,SS(:,2),SP(:,2),PS(:,2),PP(:,2));
m=max(yd);
yd=yd/m;
 %m=1;

% A=readmatrix('confidence_interval_emm2.txt');

 
 %M = readmatrix('coefficients_emm2.txt');
% M = dlmread('coefficients.txt')
  l=[-1,-1,-1,-1,-5];
 u=[1,1,1,1,5];
 s=[ 0.8 0.8  0.8 0.8 0.8 ];
%   l=[-5,-5,-5];
%  u=[5,5,5];
%  s=[5 5  5   ];


%    u=[A(1,1)+1,1+A(1,2),1+A(1,3),1+A(1,4),1+A(1,5)];
%    l=[A(1,1)-1,A(1,2)-1,A(1,3)-1,A(1,4)-1,A(1,5)-1];
%    s=[M(1,1) M(1,2) M(1,3) M(1,4) M(1,5)];
  
% %--------------------------------------------------------------------------
%create the fitoptions. Fitting with nonlinear least squares, specifying
%lower and upper boundaries for fit parameters, specifying a starting
%point.
fo = fitoptions('Method','NonlinearLeastSquares',...
               'Lower',(l),...
               'Upper',(u),...
               'StartPoint',(s));
           

%      [d,th,xxz,xyz,xzy,zxx,zxy,zzz]

%create the fit type, calling the custom function ralsiff2 as the model to fit to using the options of fo           
 % ft = fittype('cealsiff2_emm(x,xxz,zxx,zzz,xyz,xzy,zxy,d)','options',fo);

 ft = fittype('cealsiff2_emm(x,xxz,zxx,zzz,xyz,xzy,zxy,d)','problem',{'xxz','d'},'options',fo);

% ft=fittype('ralsiff2(x,th,xxz,zxx,zzz,xyz,xzy,zxy,d)','coefficients',{'th','xxz','zxx','zzz','xyz','xzy','zxy','d'},'options',fo);
%perform the fit
 % [c,gof] = fit(xd,yd,ft)
[c,gof] = fit(xd,yd,ft,'problem',{0,0})
% plot(xd,yd);
% hold on
% plot(c)
% plot(xd,ralsiff2(xd,c.th,c.xxz,c.zxx,c.zzz,c.xyz,c.xzy,c.zxy,c.d),'r')
% figure
%--------------------------------------------------------------------------
ci=confint(c); % gives the confidence interval values
f1=fopen('confidence_interval_emm_p_0.txt','w');
writematrix(ci,'confidence_interval_emm_p_0.txt');
fclose(f1);

Coefficients= [c.xxz,c.xyz,c.xzy,c.zxx,c.zxy,c.zzz];
f2=fopen('coefficients_emm_p_0.txt','w');

 writematrix(Coefficients,'coefficients_emm_p_0.txt');
fclose(f2);


x=SS(:,1);

%pick a model of the simulation to plot the fitted parameters Currently
% response
%--------------------------------------------------------------------------
% SSsim = SSeee(x,c.xxz,c.zxx,c.zzz)+ SSemm(x,c.xyz,c.xzy,c.zxy,c.d);
SSsim = SSeee(x,c.xxz,c.zxx,c.zzz)+ SSeem(x,c.xyz,c.xzy,c.zxy);

polarplot(SS(:,1),SS(:,2)/m,x,SSsim ,'LineWidth',2);
str_title=strcat('CeAlSi-SHG-',s1,'-PP-Rotating Analyser data fit with EMM');
title(str_title, 'fontsize',13);

str = {strcat('Adjusted R-square =', num2str(gof.adjrsquare),'\newline \bf(Fitted Data)', '\newline d= ',num2str(c.d), '\newline xxz= ',num2str(c.xxz),'\newline xyz = ' , num2str(c.xyz)...
    ,'\newline xzy= ',num2str(c.xzy),'\newline zxx = ' , num2str(c.zxx) ,'\newline zxy= ',num2str(c.zxy),'\newline zzz= ',num2str(c.zzz))};
legend('Data',str{:});

set(gcf, 'Position',  [200, 200, 770, 400])

%-----------------------------------------------------------------------------
figure;

% SPsim = SPeee(x,c.xxz,c.zxx,c.zzz)+ SPemm(x,c.xyz,c.xzy,c.zxy,c.d);
SPsim = SPeee(x,c.xxz,c.zxx,c.zzz)+ SPeem(x,c.xyz,c.xzy,c.zxy);
polarplot(SP(:,1),SP(:,2)/m,x,SPsim,'LineWidth',2);

str_title=strcat('CeAlSi-SHG-',s1,'-PS-Rotating Analyser data fit with EMM');
title(str_title, 'fontsize',13);
%--------------------------------------------------------------------------
figure;
% PSsim = PSeee(x,c.xxz,c.zxx,c.zzz)+ PSemm(x,c.xyz,c.xzy,c.zxy,c.d);
PSsim = PSeee(x,c.xxz,c.zxx,c.zzz)+ PSeem(x,c.xyz,c.xzy,c.zxy);
 polarplot(PS(:,1),PS(:,2)/m,x,PSsim,'LineWidth',2);
 str_title=strcat('CeAlSi-SHG-',s1,'-PS-Static Analyser data fit with EMM');
title(str_title, 'fontsize',13);
 %-------------------------------------------------------------------------
 figure;
% PPsim = PPeee(x,c.xxz,c.zxx,c.zzz)+ PPemm(x,c.xyz,c.xzy,c.zxy,c.d);
PPsim = PPeee(x,c.xxz,c.zxx,c.zzz)+ PPeem(x,c.xyz,c.xzy,c.zxy);
polarplot(PP(:,1),PP(:,2)/m,x,PPsim,'LineWidth',2);
str_title=strcat('CeAlSi-SHG-',s1,'-PP-Static Analyser data fit with EMM');
title(str_title, 'fontsize',13);

%--------------------------------------------------------------------------



str2='coefficients with wavelength_emm2_p0= nm.txt';
filename = insertAfter(str2,'wavelength_emm2_p0=',s1);
fileID = fopen(filename,'w');
fprintf(fileID,' %11s %8s %9s %8s %7s %7s \n','xxz','xyz','xzy','zxx','zxy','zzz' );
fprintf(fileID,' %6.6f %6.6f %6.6f %8.6f % 6.6f',c.xxz,c.xyz,c.xzy,c.zxx,c.zxy,c.zzz);
fclose(fileID);

%eee responses

    function med = SSeee(x,xxz,zxx,zzz)
        med = (1/32).*cos(x).^2.*(6.*xxz+3.*zxx+zzz+((-2).*xxz+(-1).*zxx+zzz).*cos(2.*x)).^2;
    end
    function med = SPeee(x,xxz,zxx,zzz)
        med = (1/8).*sin(x).^2.*(((-2).*xxz+zxx+zzz).*cos(x).^2+2.*zxx.*sin(x).^2).^2;
    end
    function med = PPeee(x,xxz,zxx,zzz)
        med = (1/8).*((2.*xxz+zxx+zzz).*cos(x).^2+2.*zxx.*sin(x).^2).^2;
    end
    function med = PSeee(x,xxz,zxx,~)
        med = 2.*xxz.^2.*cos(x).^2.*sin(x).^2;
    end

% eem responses

    function med = SSeem(x,xyz,xzy,zxy)
        med = (1/4).*(xzy+zxy).^2.*cos(x).^2;
    end
    function med = SPeem(x,xyz,xzy,zxy)
        med = (1/4).*(xyz+(-1).*zxy).^2.*sin(x).^2;
    end
    function med = PPeem(x,xyz,xzy,zxy)
       med=(1/16).*((-1).*xyz+xzy+2.*zxy+(xyz+xzy).*cos(2.*x)).^2;
    end
    function med = PSeem(x,xyz,xzy,zxy)
        med = (1/16).*(xyz+xzy).^2.*sin(2.*x).^2;
    end

% %emm responses
% 
% 
    function med = SSemm(x,xyz,xzy,zxy)
        med = (1/8).*cos(x).^2.*(2.*xzy.*cos(x).^2+((-2).*xyz+xzy+zxy).*sin(x).^2).^2;
    end
    function med = SPemm(x,xyz,xzy,zxy)
        med = (1/32).*(6.*xyz+3.*xzy+zxy+(2.*xyz+xzy+(-1).*zxy).*cos(2.*x)).^2.*sin(x).^2;
    end
    function med = PPemm(x,xyz,xzy,zxy)
        med = (1/8).*(2.*xzy.*cos(x).^2+(2.*xyz+xzy+zxy).*sin(x).^2).^2;
    end
    function med = PSemm(x,xyz,zxx,zzz)
        med = 2.*xyz.^2.*cos(x).^2.*sin(x).^2;
    end

% %mee responses
% 
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
%mem responses

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

% 
