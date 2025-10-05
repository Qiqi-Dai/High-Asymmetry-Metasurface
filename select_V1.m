function [] = select_V1(folder,i)

if exist(folder)==0 
    mkdir(folder);
end

fre = linspace(0.3, 0.8, 100);

load(['results_',num2str(i),'.mat']);
A1 = real_n_eff(21:80); 
B1 = any(A1(:) > 0);
C1 = any(A1(:) < 0);    
    
A2 = real_mu_eff(21:80); 
% B2 = any(A2(:) > 0);
% C2 = any(A2(:) < 0);
    
if B1==1 && C1==1
    plot(fre, T, 'LineWidth', 2);
    grid on;
    ylim([0,1]);
    xlim([0.3, 0.8]);
    xlabel('Frequency/THz');
    ylabel('Transmission');
    saveas(gcf,[folder,num2str(i),'_T.png']);
end
