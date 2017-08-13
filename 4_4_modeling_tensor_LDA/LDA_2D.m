function [ NewX,Sb,Sw ] = LDA_2D( y_class, mat_flow, num_class, dim_to_keep )
%LDA_2D 此处显示有关此函数的摘要
%   mat_flow是个cell
%%
% 得到类别和每类的个数
y_result = tabulate(y_class);
N = zeros(num_class,1);
T = zeros(num_class,1);
% 样本总个数
num_sample = size(y_class,2);
Sb = zeros(size(mat_flow{1},1));
Sw = zeros(size(mat_flow{1},1));
% 求得所有样本平均的At
At = zeros(size(mat_flow{1}));
for i = 1:num_sample
    At = At + mat_flow{i};
end
At = At/num_sample;

for i = 1:num_class
    T(i) = y_result(i,1);
    N(i) = y_result(i,2);
    % 作为临时矩阵，用于累加类间
    Atemp = zeros(size(mat_flow{1}));
    for j = 1:num_sample
        if y_class(j) == T(i)
            Atemp = Atemp + mat_flow{j};
        end
    end
    % 得到每类的平均值
    A{i} = Atemp/T(i);
    % 得到Sb
    Sb = Sb + N(i)* (A{i}-At)*(A{i}-At)';
   
    for j = 1:num_sample
        if y_class(j) == T(i)
            Sw = Sw + ((mat_flow{j}-A{i}) * (mat_flow{j}-A{i})');
        end
    end
end
T = pinv(Sw) * Sb;
[X,eigens] = eig(T);
[values,posits]=sort(diag(eigens),'descend');
NewX=X(:,posits(1:dim_to_keep));

end

