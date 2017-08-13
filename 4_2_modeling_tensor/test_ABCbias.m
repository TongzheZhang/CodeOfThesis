function [right_num] = test_ABCbias(A,B,C,bias,tensor_flow,y_incre,total_len,train_num,test_num)
%检验训练的成果
%   输入回归参数和张量流，还有y值
%   输出正确的个数
%% 读入数据
test_tensor_flow = tensor_flow(train_num+1:total_len);%可以更改为不同的重构方式
test_price = y_incre(train_num+1:total_len);%升降幅度提升，数值过小，所以乘以1000，选取前n天训练
pred_price = [];
%% 预测
for i = 1:test_num
    one_tensor = test_tensor_flow{i};
    tempPrice = ttm(one_tensor, {A,B,C}, [1 2 3]); %<-- same as above
    tempPrice = reshape(double(tempPrice),1,1);
    pred_price = [pred_price;tempPrice];
end
%% 得到最终的预测结果
pred_price = (pred_price - bias);
%% 得到测试集的正负向
test_di = [];
for tempprice = test_price
    if tempprice>=0
        test_di = [test_di;1];
    else
        test_di = [test_di;-1];
    end
end
%% 得到测试集预测结果的正负向
pred_di = [];
for tempprice = pred_price'
    
    if tempprice>=0       
        pred_di = [pred_di;1];
    else
        pred_di = [pred_di;-1];
    end
end
%% 计算有多少个预测正确
right_num = 0;
for i = 1:test_num
    if pred_di(i)==test_di(i)
        right_num = right_num+1;
    end
end
save pred_price pred_price
end