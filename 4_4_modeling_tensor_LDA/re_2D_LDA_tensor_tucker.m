function [re_LDA_tensor_flow,X1,X2,X3] = re_2D_LDA_tensor_tucker( tensor_flow, y_class, total_num, train_num,dim1,dim2,dim3,dim_x1,dim_x2,dim_x3,num_class)
%re_2D_LDA_tensor_tucker 输入张量流，输出变换矩阵X1，X2，X3
%   输入张量流，利用tucker分解
%   y_class是y对应的类别
%   train_num是训练的天数
%   dim是U保留的维度
%   dim_x是X选取最大特征值时剩下的维度
train_y_class = y_class(1:train_num);%177; %设置训练的天数
%% 得到张量流的核流，和不同模态的模流
C_flow = cell(1,total_num);
U1_flow = cell(1,total_num);
U2_flow = cell(1,total_num);
U3_flow = cell(1,total_num);
U1_flow_new = cell(1,total_num);
U2_flow_new = cell(1,total_num);
U3_flow_new = cell(1,total_num);
re_LDA_tensor_flow = cell(1,total_num);
for i = 1:total_num
    % 按不同的模展开张量
    A1 = tenmat(tensor_flow{i},1);
    A2 = tenmat(tensor_flow{i},2);
    A3 = tenmat(tensor_flow{i},3);
    % 分解展开矩阵
    [U1,S1,V1] = svd(A1.data);
    [U2,S2,V2] = svd(A2.data);
    [U3,S3,V3] = svd(A3.data);
    %% 去除噪声
    U1(:,dim1+1:end) = [];%5:6
    U2(:,dim2+1:end) = [];%70:100
    U3(:,dim3+1:end) = [];%3
    S = ttm(tensor_flow{i},{U1',U2',U3'});
    C_flow{i} = S;
    U1_flow{i} = U1;
    U2_flow{i} = U2;
    U3_flow{i} = U3;
    
end
[X1,Sb1,Sw1] = LDA_2D(train_y_class, U1_flow(1:train_num), num_class, dim_x1);
[X2,Sb2,Sw2] = LDA_2D(train_y_class, U2_flow(1:train_num), num_class, dim_x2);
[X3,Sb3,Sw3] = LDA_2D(train_y_class, U3_flow(1:train_num), num_class, dim_x3);
for i = 1:total_num
    U1_flow_new{i} = X1'*U1_flow{i};
    U2_flow_new{i} = X2'*U2_flow{i};
    U3_flow_new{i} = X3'*U3_flow{i};
    re_LDA_tensor_flow{i} = ttm(C_flow{i},{ U1_flow_new{i}, U2_flow_new{i}, U3_flow_new{i}});
end
end

