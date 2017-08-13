%主函数程序
%   假设我们知道特征的维度是多少
%% 读入y值，求取训练集和测试集的个数
clear;
load('E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\y_incre.mat');
total_num = length(y_incre);
train_num = ceil(total_num*0.8);
test_num = total_num - train_num;
y_test_real = y_incre(train_num+1:total_num)';
%% 设定U保留!的维度
dim1=4;
dim2=60;
dim3=4;

%% 构建张量流
[re_tensor_flow, tensor_flow] = con_tensor_flow(total_num,dim1,dim2,dim3,'threestick','yes');% 使用三个棍构建法或者默认的外积方法，是否归一化

%% 得到张量流的矩阵形式，这样可以使用之后的回归
%更改训练和测试的特征张量
tensor_flow_mat = zeros(6,100,6,total_num);
for i = 1:total_num
    %更改训练和测试的特征张量
    tensor_flow_mat(:,:,:,i) =  re_tensor_flow{i};
end
%% general tensor ridge regression，设置参数
using_mat = tensor_flow_mat;
lambda = 0.0000000001;%0.000000000001
R = 3;
MaxIter = 50;
Tol = 1e-6;
[U, d, err] = genTensorRegression(tensor(using_mat(:,:,:,1:train_num)),y_incre(1:train_num)', lambda, R, MaxIter, Tol);%genTensorRegression
model.U = U;
model.b = d;
model.train_err = err;

%% 预测
ten_U = ktensor(U);
ten_U = tensor(ten_U);
pred_price = [];
for i = 1:test_num
    tempFeature = tensor(using_mat(:,:,:,train_num+i));
    tempPred = innerprod(tempFeature, ten_U)+d;
    pred_price = [pred_price;tempPred];
end
%% 结果
right_num=0;
right_class_num = 0;
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


%% 之前李庆的回归方法实现
% [re_tensor_flow, tensor_flow] = con_tensor_flow(total_len);
% [A,B,C,bias] = tensor_reg(re_tensor_flow,y_incre,total_len,train_num,test_num,6,100,3,2000);
% right_num = test_ABCbias(A,B,C,bias,re_tensor_flow,y_incre,total_len,train_num,test_num);
