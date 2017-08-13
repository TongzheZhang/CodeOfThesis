function [re_LPPandLDA_tensor_flow,T1new,T2new,T3new] = re_LPP_and_LDA_tensor_tucker(tensor_flow,y_incre,y_class,total_num,train_num,test_num,dim1,dim2,dim3,dim_t1,dim_t2,dim_t3,alpha,beta,num_class)
%re_LPP_and_LDA_tensor_tucker
%   读入价格和特征张量
%   输出X1,X2,X3和重构的训练张量
%   tensor_flow是输入的特征
%   y_incre是对应的y值
%   train_num：训练天数
%   dim1，dim2，dim3：U保留的维度
%   dim_v1,dim_v2,dim_v3：V保留的维度

%% 得到训练数据
train_tensor_flow = tensor_flow(1:train_num);
train_prices = y_incre(1:train_num);
train_y_class = y_class(1:train_num);
%% 创建一些容器
C_flow = cell(1,train_num);
U1_flow = cell(1,train_num);
U2_flow = cell(1,train_num);
U3_flow = cell(1,train_num);
U1_flow_new = cell(1,total_num);
U2_flow_new = cell(1,total_num);
U3_flow_new = cell(1,total_num);
re_LPPandLDA_tensor_flow = cell(1,total_num);
%% 构建价格相似矩阵W
W = zeros(train_num,train_num);
for i = 1:train_num
    for j = i:train_num
        if abs(train_prices(i)-train_prices(j))<0.01
            W(i,j) = 1;
        end
    end
end
D = sum(W,1);
D = D';
%% 得到张量流的核流，和不同模态面的模流
for i = 1:train_num
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
%% 得到Sb，Sw
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
    U1(:,dim1+1:end) = [];%
    U2(:,dim2+1:end) = [];%
    U3(:,dim3+1:end) = [];%
    S = ttm(tensor_flow{i},{U1',U2',U3'});
    C_flow{i} = S;
    U1_flow{i} = U1;
    U2_flow{i} = U2;
    U3_flow{i} = U3;
    
end
[X1,Sb1,Sw1] = LDA_2D(train_y_class, U1_flow(1:train_num), num_class, dim_t1);
[X2,Sb2,Sw2] = LDA_2D(train_y_class, U2_flow(1:train_num), num_class, dim_t2);
[X3,Sb3,Sw3] = LDA_2D(train_y_class, U3_flow(1:train_num), num_class, dim_t3);
%% 求得DU,WU，注意，这里的特征维度可能随着提取特征的不同，而改变
DU1 = zeros(6,6);
WU1 = zeros(6,6);
DU2 = zeros(100,100);
WU2 = zeros(100,100);
DU3 = zeros(6,6);
WU3 = zeros(6,6);
%% DU1，WU2
for i = 1:train_num
    DU1 = DU1 + D(i)*U1_flow{i}*U1_flow{i}';
    for j = i:train_num
        WU1 = WU1 + W(i,j)*U1_flow{i}*U1_flow{j}';
    end
end
%% DU2，WU2
for i = 1:train_num
    DU2 = DU2 + D(i)*U2_flow{i}*U2_flow{i}';
    for j = i:train_num
        WU2 = WU2 + W(i,j)*U2_flow{i}*U2_flow{j}';
    end
end
%%  DU3，WU3
for i = 1:train_num
    DU3 = DU3 + D(i)*U3_flow{i}*U3_flow{i}';
    for j = i:train_num
        WU3 = WU3 + W(i,j)*U3_flow{i}*U3_flow{j}';
    end
end

%% 求解T1
T1 = pinv(DU1) * (beta*(DU1 - alpha*WU1)+(1-beta)*(WU1-DU1));
[V1,eig1] = eig(T1);
[values1,posits1]=sort(diag(eig1),'descend');
T1new=T1(:,posits1(1:dim_t1));
%% 求解T2
T2 = pinv(DU2) * (beta*(DU2 - alpha*WU2)+(1-beta)*(WU2-DU2));
[V2,eig2] = eig(T2);
[values2,posits2]=sort(diag(eig2),'descend');
T2new=T2(:,posits2(1:dim_t2));
%% 求解T3
T3 = pinv(DU3) * (beta*(DU3 - alpha*WU3)+(1-beta)*(WU3-DU3));
[V3,eig3] = eig(T3);
[values3,posits3]=sort(diag(eig3),'descend');
T3new=T3(:,posits3(1:dim_t3));

%% 取实部
T1new = real(T1new);
T2new = real(T2new);
T3new = real(T3new);

%% 得到新的张量流
for i = 1:total_num
    U1_flow_new{i} = T1new'*U1_flow{i};
    U2_flow_new{i} = T2new'*U2_flow{i};
    U3_flow_new{i} = T3new'*U3_flow{i};
    re_LPPandLDA_tensor_flow{i} = ttm(C_flow{i},{ U1_flow_new{i}, U2_flow_new{i}, U3_flow_new{i}});
end
end

