%主函数程序
%   假设我们知道特征的维度是多少
%   对价格相似度方法的主函数
%   使用LDA方法
clear;
load('E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\y_incre.mat');
total_len = length(y_incre);
train_num = ceil(total_len*0.8);
test_num = total_len - train_num;
y_class = zeros(1,total_len);
y_test_real = y_incre(train_num+1:total_len)';
for i = 1:total_len
    if y_incre(i)>=0.001
        y_class(i) = 1;
    elseif y_incre(i)<=-0.001
        y_class(i) = 2;
    else 
        y_class(i) = 3;
    end
end
%U保留的维度
dim1=5;
dim2=80;
dim3=2;
%X保留的主成分维度
dim_x1=4;
dim_x2=60;
dim_x3=1;
%% 构建张量流
[re_tensor_flow, tensor_flow] = con_tensor_flow(total_len,dim1,dim2,dim3,'outproduct','no');% 使用三个棍构建法或者默认的外积方法，是否归一化
%% 训练得到X1，X2，X3
num_class = 3;%分为几类
[re_LDA_tensor_flow,X1,X2,X3] = re_2D_LDA_tensor_tucker(tensor_flow,y_class,total_len,train_num,dim1,dim2,dim3,dim_x1,dim_x2,dim_x3,num_class);

%% 利用V1,V2,V3得到利用相关性重建的张量流
re_tensor_flow_mat = zeros(dim_x1,dim_x2,dim_x3,total_len);
for i = 1:total_len
    re_tensor_flow_mat(:,:,:,i) =  re_LDA_tensor_flow{i};
end
using_mat = re_tensor_flow_mat;%更改训练和测试的特征张量
%% general tensor ridge regression，设置参数
lambda = 0.000000001;%0.000000000001
R = 10;
MaxIter = 30;
Tol = 1e-6;
[U, d, err] = genTensorRegression(tensor(using_mat(:,:,:,1:train_num)),y_incre(1:train_num)', lambda, R, MaxIter, Tol);%genTensorRegression
model.U = U;
model.b = d;
model.train_err = err;
%% Optimal rank tensor regression 
% R = 5;
% MaxIter = 50;
% Tol = 1e-6;
% C = 0.005;
% MaxRank = 88;
% libsvm_options = sprintf('-s %d -t %d -c %f', 3, 2, C);%http://blog.csdn.net/changyuanchn/article/details/7540014 参数说明
% [U,d,Alpha,beta,train_err] = orTensorRegression(tensor(using_mat(:,:,:,1:train_num)),y_incre(1:train_num)', MaxRank, 'lsq', 'sbl', 1, libsvm_options);
% model.U = U;
% model.b = d;
% model.train_err = train_err;
%% 测试
ten_U = ktensor(U);
ten_U = tensor(ten_U);
pred_price = [];
pred_price_class = [];
for i = 1:test_num
    tempFeature = tensor(using_mat(:,:,:,train_num+i));
    tempPred = innerprod(tempFeature, ten_U)+d;
    pred_price = [pred_price;tempPred];
     if tempPred>=0.0000001
        pred_price_class(i) = 1;
    elseif tempPred<=-0.0000001
        pred_price_class(i) = 2;
    else 
        pred_price_class(i) = 3;
    end
end
right_num=0;
right_class_num=0;
%% 结果
 for i=1:test_num
     if pred_price(i)*y_incre(i+train_num)>0
         right_num=right_num+1;
     end 
     if pred_price_class(i) == y_class(i+train_num) 
         right_class_num = right_class_num+1;
     end
 end
%% Root Mean Squared Errors
RMSE = sqrt((sum((pred_price(1:test_num)-y_test_real(1:test_num)).^2))/test_num);
save pred_price pred_price
disp('RMSE'),disp(RMSE);
disp('预测对的天数'),disp(right_num),disp('预测升降的准确率'),disp(right_num/test_num);
%disp('预测类准确度'),disp(right_class_num),disp('准确率'),disp(right_class_num/test_num)