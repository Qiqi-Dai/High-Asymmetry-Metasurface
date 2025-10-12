function [] = import_generator(path, i)

sx = 201;
sy = 201;
a = imread([path, 'pred_',num2str(i),'.png']);
a(a<128) = 0;
a(a>=128) = 1;
a = imresize(a, [sx, sy], 'nearest');
% imagesc(a);
b = reshape(a, [sx*sy,1]);
c = [b; b];
info = [sx, 1, 101; sy, 1, 101; 2, 1, 2];
writematrix(info,['import_',num2str(i),'.txt'],'delimiter','\t');
fid = fopen(['import_',num2str(i),'.txt'],'a+');
        
fprintf(fid,'%d\r\n',c);
fclose(fid);

end