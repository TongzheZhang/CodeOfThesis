function [V1new,V2new,V3new] = re_co_tensor_tucker(tensor_flow,y_incre,train_num,dim1,dim2,dim3,dim_v1,dim_v2,dim_v3)
%re_co_tensor_tucker 此处显示有关此函数的摘要
%   读入价格和特征张量
%   输出V1，V2，V3和重构的训练张量
%   tensor_flow是输入的特征
%   y_incre是对应的y值
%   train_num：训练天数
%   dim1，dim2，dim3：U保留的维度
%   dim_v1,dim_v2,dim_v3：V保留的维度

%% 读入数据
days = train_num;%177; %设置训练的天数
train_tensor_flow = tensor_flow(1:days);
train_prices = y_incre(1:days);
%% 构建价格相似矩阵W
W = zeros(days,days);
for i = 1:days
    for j = i:days
        if abs(train_prices(i)-train_prices(j))<0.01
            W(i,j) = 1;
        end
    end
end
D = sum(W,1);
D = D';
C_flow = cell(1,days);
U1_flow = cell(1,days);
U2_flow = cell(1,days);
U3_flow = cell(1,days);
%% 得到张量流的核流，和不同模态的模流
for i = 1:days
    % 按不同的模展开张量
    A1 = tenmat(train_tensor_flow{i},1);
    A2 = tenmat(train_tensor_flow{i},2);
    A3 = tenmat(train_tensor_flow{i},3);
    % 分解展开矩阵
    [U1,S1,V1] = svd(A1.data);
    [U2,S2,V2] = svd(A2.data);
    [U3,S3,V3] = svd(A3.data);
    % 去噪
    U1(:,dim1+1:end) = [];%5:6
    U2(:,dim2+1:end) = [];%71:100
    U3(:,dim3+1:end) = [];%3
    % 构建核心张量和重构
    S = ttm(train_tensor_flow{i},{U1',U2',U3'});    
    C_flow{i} = S;
    U1_flow{i} = U1;
    U2_flow{i} = U2;
    U3_flow{i} = U3;
end
%% 求得V1，V2，V3
DU1 = zeros(6,6);
WU1 = zeros(6,6);
DU2 = zeros(100,100);
WU2 = zeros(100,100);
DU3 = zeros(6,6);
WU3 = zeros(6,6);
%% V1
for i = 1:days
    DU1 = DU1 + D(i)*U1_flow{i}*U1_flow{i}';
    for j = i:days
        WU1 = WU1 + W(i,j)*U1_flow{i}*U1_flow{j}';
    end
end
T1 = pinv(DU1) * (DU1 - WU1);
[V1,eig1] = eig(T1);
[values1,posits1]=sort(diag(eig1),'ascend');
V1new=V1(:,posits1(1:dim_v1));
%% V2
for i = 1:days
    DU2 = DU2 + D(i)*U2_flow{i}*U2_flow{i}';
    for j = i:days
        WU2 = WU2 + W(i,j)*U2_flow{i}*U2_flow{j}';
    end
end
T2 = pinv(DU2) * (DU2 - WU2);
[V2,eig2] = eig(T2);
[values2,posits2]=sort(diag(eig2),'ascend');
V2new=V2(:,posits2(1:dim_v2));
%% V3
for i = 1:days
    DU3 = DU3 + D(i)*U3_flow{i}*U3_flow{i}';
    for j = i:days
        WU3 = WU3 + W(i,j)*U3_flow{i}*U3_flow{j}';
    end
end
T3 = pinv(DU3) * (DU3 - WU3);
[V3,eig3] = eig(T3);
[values3,posits3]=sort(diag(eig3),'ascend');
V3new=V3(:,posits3(1:dim_v3));
%% 取实部
V1new = real(V1new);
V2new = real(V2new);
V3new = real(V3new);
end