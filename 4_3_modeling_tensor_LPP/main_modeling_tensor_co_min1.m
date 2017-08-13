%主函数程序
%   假设我们知道特征的维度是多少
%   对价格相似度方法的主函数
clear;
load('E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\y_min1.mat');
total_len = length(y_min1);
train_num = ceil(total_len*0.8);
test_num = total_len - train_num;
y_class = zeros(1,total_len);
y_test_real = y_min1(train_num+1:total_len)';
for i = 1:total_len
    if y_min1(i)>=0.001
        y_class(i) = 1;
    elseif y_min1(i)<=-0.001
        y_class(i) = 2;
    else 
        y_class(i) = 3;
    end
end
%U保留的维度
dim1=5;
dim2=80;
dim3=2;
%V保留的主成分维度
dim_v1=4;
dim_v2=60;
dim_v3=1;
%% 构建张量流
[re_tensor_flow, tensor_flow] = con_tensor_flow_min1(total_len,dim1,dim2,dim3,'outproduct','no');% 使用三个棍构建法或者默认的外积方法，是否归一化

%% 训练得到V1,V2,V3
[V1,V2,V3] = re_co_tensor_tucker(tensor_flow,y_min1,train_num,dim1,dim2,dim3,dim_v1,dim_v2,dim_v3);

%% 利用V1,V2,V3得到利用相关性重建的张量流
re_tensor_flow_mat = zeros(6,100,6,total_len);

re_co_tensor_flow = cell(1,total_len);
re_co_tensor_flow_mat = zeros(dim_v1,dim_v2,dim_v3,total_len);
for i = 1:total_len
    [re_co_tensor_flow{i},re_co_tensor_flow_mat(:,:,:,i)] = re_co_tensor_tucker_single(tensor_flow{i},V1,V2,V3,dim1,dim2,dim3);
    re_tensor_flow_mat(:,:,:,i) =  re_tensor_flow{i};
end

%% general tensor ridge regression
using_mat = re_tensor_flow_mat;%更改训练和测试的特征张量
lambda = 0.00000000000001;
R = 10;
MaxIter = 30;
Tol = 1e-6;
[U, d, err] = genTensorRegression(tensor(using_mat(:,:,:,1:train_num)),y_min1(1:train_num)', lambda, R, MaxIter, Tol);%genTensorRegression
model.U = U;
model.b = d;
model.train_err = err;

%% 测试
ten_U = ktensor(U);
ten_U = tensor(ten_U);
pred_price = [];
for i = 1:test_num
    tempFeature = tensor(using_mat(:,:,:,train_num+i));
    tempPred = innerprod(tempFeature, ten_U)+d;
    pred_price = [pred_price;tempPred];
end
right_num=0;
%% 结果
 for i=1:test_num
     if pred_price(i)*y_min1(i+train_num)>0
         right_num=right_num+1;
     end
 end
disp(right_num);
accuracy = right_num/test_num;
disp(accuracy);
%% Root Mean Squared Errors
RMSE = sum((pred_price(1:test_num)-y_test_real(1:test_num)).^2);
disp('RMSE'),disp(RMSE);
save pred_price pred_price