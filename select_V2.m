function [] = select_V2(folder, folder_v1, folder_v2, folder_dataset)

if exist(folder_v2)==0 
    mkdir(folder_v2);
end

files = dir([folder_v1,'/*_T.png']);
path = folder;
f = linspace(0.3e12, 0.8e12, 100);
Q_array = [];
FOM_array = [];

for i=1:length(files)

abc = split(files(i).name, '_');
name = abc{1};
load(append(path, 'results_', name,'.mat'));
y = squeeze(T)';

local_min = islocalmin(y);
local_max = islocalmax(y);

pmin_x = f(local_min==1);
pmin_y = y(local_min==1);
fr = pmin_x(1:end);
pmin_y(pmin_x>0.75e12) = [];
pmin_y(pmin_x<0.35e12) = [];
pmin_x(pmin_x>0.75e12) = [];
pmin_x(pmin_x<0.35e12) = [];

if length(pmin_x)>=1   
    
    p1_x = f(1); p1_y = y(1);
    p2_x = f(100); p2_y = y(100);
    pmax_x = f(local_max==1);
    pmax_y = y(local_max==1);
    points = [p1_x, pmin_x(1:end), pmax_x(1:end), p2_x; p1_y, pmin_y(1:end), pmax_y(1:end), p2_y];
    
    X = points(1,:); Y = points(2,:);
    [Xsorted,I] = sort(X);
    Ysorted = Y(I);
    
    Q = [];
    FoM = [];
    for kn=1:length(pmin_x)
        k = find(Xsorted==pmin_x(kn));
        p_min_X = Xsorted(k); p_min_Y = Ysorted(k);
        if Ysorted(k-1)<=Ysorted(k+1)
            p_max_X = Xsorted(k-1); p_max_Y = Ysorted(k-1);
        else
            p_max_X = Xsorted(k+1); p_max_Y = Ysorted(k+1);
        end
        
        hm = (p_min_Y+p_max_Y)/2.0;
        p1_X = interp1(y(1:find(y==p_min_Y)), f(1:find(f==p_min_X)), hm);
        p2_X = interp1(y(find(y==p_min_Y):end), f(find(f==p_min_X):end), hm);        
        Q = [Q, p_min_X/abs(p2_X-p1_X)];
        FoM = [FoM, p_min_X/abs(p2_X-p1_X)*abs(p_max_Y-p_min_Y)];    
    end

    if max(FoM)>=0.7
       save([folder_v2, name, '_points.mat'], "Xsorted","Ysorted", "fr");
       save([folder_v2, name, '_metrics.mat'], "Q", "FoM", "fr", "y");
       copyfile([folder_v1, name,'_T.png'], folder_v2);
       splitted_str = split(folder,"/");
       copyfile([path,'pred_', name,'.png' ], [folder_dataset,splitted_str{end-2},'_pred_',name,'.png']);
    end



end



end