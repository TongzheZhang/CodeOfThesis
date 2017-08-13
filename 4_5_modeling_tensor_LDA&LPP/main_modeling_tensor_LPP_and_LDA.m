%主函数程序
%   假设我们知道特征的维度是多少
%   对价格相似度方法的主函数
%   使用LDA和LPP的方法
clear;
load('E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\y_incre.mat');
total_num = length(y_incre);
train_num = ceil(total_num*0.8);
test_num = total_num - train_num;
y_class = zeros(1,total_num);
y_test_real = y_incre(train_num+1:total_num)';
for i = 1:total_num
    if y_incre(i)>=0.01
        y_class(i) = 1;
    elseif y_incre(i)<=-0.01
        y_class(i) = 2;
    else
        y_class(i) = 3;
    end
end
%U保留的维度
dim1=5;
dim2=60;
dim3=5;
%X保留的主成分维度
dim_t1=4;
dim_t2=40;
dim_t3=4;
%% 构建张量流
[re_tensor_flow, tensor_flow] = con_tensor_flow(total_num,dim1,dim2,dim3,'outproduct','no');% 使用三个棍构建法或者默认的外积方法，是否归一化
%% 训练得到X1，X2，X3
num_class = 3;%分为几类
alpha = 1;
beta = 0.2;% 0<beta<1
[re_LPPandLDA_tensor_flow,T1new,T2new,T3new] = re_LPP_and_LDA_tensor_tucker(tensor_flow,y_incre,y_class,total_num,train_num,test_num,dim1,dim2,dim3,dim_t1,dim_t2,dim_t3,alpha,beta,num_class);

%% 得到张量流的矩阵形式，这样可以使用之后的回归
re_tensor_flow_mat = zeros(dim_t1,dim_t2,dim_t3,total_num);
for i = 1:total_num
    re_tensor_flow_mat(:,:,:,i) =  re_LPPandLDA_tensor_flow{i};
end
%% general tensor ridge regression，设置参数
using_mat = re_tensor_flow_mat;%更改训练和测试的特征张量
lambda = 0.0000000001;%0.000000000001
R = 3;
MaxIter = 50;
Tol = 1e-6;
[U, d, err] = genTensorRegression(tensor(using_mat(:,:,:,1:train_num)),y_incre(1:train_num)', lambda, R, MaxIter, Tol);%genTensorRegression
model.U = U;
model.b = d;
model.train_err = err;

%% 测试
ten_U = ktensor(U);
ten_U = tensor(ten_U);
pred_price = [];
pred_price_class = [];
for i = 1:test_num
    tempFeature = tensor(using_mat(:,:,:,train_num+i));
    tempPred = innerprod(tempFeature, ten_U)+d;
    pred_price = [pred_price;tempPred];
    if tempPred>=0.001
        pred_price_class(i) = 1;
    elseif tempPred<=-0.001
        pred_price_class(i) = 2;
    else
        pred_price_class(i) = 3;
    end
end
right_num=0;
right_class_num = 0;
%% 结果
for i=1:test_num
    if pred_price(i) >= 0
        if y_incre(i+train_num) >= 0
            right_num=right_num+1;
        end
    end
    if pred_price(i) < 0
        if y_incre(i+train_num) < 0
            right_num=right_num+1;
        end
    end 
end
%% 输出结果，Root Mean Squared Errors
RMSE = sum((pred_price(1:test_num)-y_test_real(1:test_num)).^2);
save pred_price pred_price
disp('RMSE'),disp(RMSE);
disp('预测对的天数'),disp(right_num),disp('预测升降的准确率'),disp(right_num/test_num);