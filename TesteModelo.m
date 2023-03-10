clear
close all
clc
%%
L = .45;
D = .04;
rho = 998;
A = 100;
T = 2; w = 2*pi/T;
t = 0:.01:30; 		%construção de vetor x=primeiro:incremento:último
x(:,1) = A/1000*cos(w*t);	%x(:,1) 
xdot(:,1) = -A*w/1000*sin(w*t);
xddot(:,1) = -A*w^2/1000*cos(w*t); 
cm_comGJR = 1;
cd_comGJR = 2;

cm_semGJR = .6*cm_comGJR;
cd_semGJR = .2*cd_comGJR;

SNR = 2;

time_shift = .2;
%%
fig1 = figure('Position',[50 50 1280 720],'Name','fig_fit'); 
Hax = .27;
ax1 = axes(gcf,'Position',[.08 .12+2*Hax .83 Hax],'FontSize',20); ylabel(ax1,'x(mm)'); hold(ax1,'on'); box(ax1,'on'); grid(ax1,'on');
ax2 = axes(gcf,'Position',[.08 .12+Hax .83 Hax],'FontSize',20); ylabel(ax2,'F(N)'); hold(ax2,'on'); box(ax2,'on'); grid(ax2,'on'); 
ax3 = axes(gcf,'Position',[.08 .12 .83 Hax],'FontSize',20); ylabel(ax3,'F(N)'); xlabel(ax3,'t(s)'); hold(ax3,'on'); box(ax3,'on'); grid(ax3,'on'); 
ax1.XTickLabels = {}; 
ax2.XTickLabels = {}; ax2.YAxisLocation = 'right';
%%
F1(:,1) = -.5*rho*L*D.*xdot.*abs(xdot)*cd_comGJR-rho*pi*D^2/4*L*xddot*cm_comGJR;
F2(:,1) = -.5*rho*L*D.*xdot.*abs(xdot)*cm_semGJR-rho*pi*D^2/4*L*xddot*cd_semGJR;
F3(:,1) = F1-F2;
NOISE = std( F3 )/SNR;	%std tem o python
F = F1 + ( rand(size(x))-.5 ) * NOISE ;	%size=len e rand faz aleatórios de 0-1

[cf1,cf2] = butter( 4,5/(100/2),'low' );	%tem no scipy
F_filt(:,1) = filtfilt( cf1,cf2,F );	%tem filtfilt no scipy
%%
x_fit(:,1:2) = [xdot(t>5 & t<25),xddot(t>5 & t<25)];	%x_fit(:,1:2) = [xdot(t>5 & t<25),xddot(t>5 & t<25)]
%y_fit(:,1) = F_filt( round(t,2)>(5) & round(t,2)<(25) );	%round(t,2)
%y_fit_shift(:,1) = F_filt( round(t,2)>(5-time_shift) & round(t,2)<(25-time_shift) );
y_fit(:,1) = F_filt( t>(5) & t<25 );	%round(t,2) & tbm funciona no py
y_fit_shift(:,1) = F_filt( t>(5-time_shift) & t<(25-time_shift) );

eq = ['CD*',num2str(-.5*rho*L*D,'%10.3f'),'*v*abs(v) + CA*',num2str(-rho*pi*(D^2)/(4*L),'%10.3f'),'*a'];	%fazer a equação
ft = fittype( eq, 'independent', {'v','a'}, 'dependent', 'F' );	%fittype?
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );	%fitoptions?
opts.Display = 'Off';
opts.Lower = [0 -2];
opts.Upper = [5 5];
opts.StartPoint = [1 1];

[c11,gof11] = fit( x_fit,y_fit_shift, ft, opts);
cd_top_fit_shift = c11.CD;
cm_top_fit_shift = c11.CA;
r2_top_shift = gof11.rsquare;

[c22,gof22] = fit( x_fit,y_fit, ft, opts);
cd_top_fit = c22.CD;
cm_top_fit = c22.CA;
r2_top = gof22.rsquare;

F_fit(:,1) = -.5*rho*L*D.*x_fit(:,1).*abs(x_fit(:,1))*cd_top_fit - rho*pi*D^2/4*L*x_fit(:,2)*cm_top_fit;
F_fit_shift(:,1) = -.5*rho*L*D.*x_fit(:,1).*abs(x_fit(:,1))*cd_top_fit_shift - rho*pi*D^2/4*L*x_fit(:,2)*cm_top_fit_shift;
%%
plot(ax1,t,x,'k','LineWidth',2);
plot(ax2,t,F1,'LineWidth',2,'DisplayName','F_{GJR+STR}');
plot(ax2,t-time_shift,F2,'LineWidth',2,'DisplayName','F_{STR}');
plot(ax2,t,F3,'LineWidth',2,'DisplayName','F_{GJR}');
plot(ax2,t,F,'LineWidth',1,'DisplayName','F_{GJR}+SNR');
plot(ax3,t,F,'LineWidth',1,'DisplayName','F_{GJR}+SNR');
plot(ax3,t,F_filt,'LineWidth',2,'DisplayName','F_{GJR}+SNR - filt');
str = [ ['CD = ',num2str(cd_top_fit,'%10.3f'),' & CM = ',num2str(cm_top_fit,'%10.3f')] newline ['R^2 = ',num2str(r2_top,'%10.3f')] ];
plot(ax3,t(t>5 & t<25),F_fit,'LineWidth',2,'DisplayName',[ 'F_{GJR}+SNR - FIT' newline str ] );
str = [ ['CD = ',num2str(cd_top_fit_shift,'%10.3f'),' & CM = ',num2str(cm_top_fit_shift,'%10.3f')] newline ['R^2 = ',num2str(r2_top_shift,'%10.3f')] ];
plot(ax3,t(t>5 & t<25),F_fit_shift,'LineWidth',2,'DisplayName',[ 'F_{GJR}+SNR - FIT com shift' newline str ] );
legend('Location','SouthWest','FontSize',14)