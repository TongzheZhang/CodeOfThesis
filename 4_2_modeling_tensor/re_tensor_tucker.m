function [ B ] = re_tensor_tucker(A,dim1,dim2,dim3)
%利用高阶奇异值分解进行张量重构
%   输入为张量，dim1,dim2,dim3是保留的维度
%   输出为重构张量
%   去掉U中末尾几列
%% 按不同的模展开张量
A1 = tenmat(A,1);
A2 = tenmat(A,2);
A3 = tenmat(A,3);
%% 分解展开矩阵
[U1,S1,V1] = svd(A1.data);
[U2,S2,V2] = svd(A2.data);
[U3,S3,V3] = svd(A3.data);
%% 去除噪声
U1(:,dim1+1:end) = [];%5:6
U2(:,dim2+1:end) = [];%70:100
U3(:,dim3+1:end) = [];%3
%% 构建核心张量和重构
S = ttm(A,{U1',U2',U3'});
B = ttm(S,{U1,U2,U3}); %tucker的三方面矩阵就是U1，U2，U3
end

