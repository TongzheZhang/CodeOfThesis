function [A,B,C,bias] = tensor_reg(tensor_flow,y_incre,total_len,train_num,test_num,num_train,dim_v1,dim_v2,dim_v3)
%训练张量回归参数，最终返回A,B,C,bias
%   输入一个张量流，和一个缺省值days
%   输出回归所需要的参数
days = train_num;% 选取前n天训练

%% 读入数据
using_tensor_flow = tensor_flow(1:total_len);%可以更改为不同的重构方式  re_co_tensor_flow(1:221)
price = y_incre(1:days);%*1000;%升降幅度提升，数值过小，所以乘以1000，选取前n天训练
%% 赋予初始值
A = ones(1,dim_v1);B = ones(1,dim_v2);C = ones(1,dim_v3);bias = 0;
lastA = ones(1,dim_v1);lastB = ones(1,dim_v2);lastC = ones(1,dim_v3);lastbias = 0;

%% 训练
num = 1;
while num < num_train % 设置为2000
    
    % 根据m的不同，把张量转化为向量
    % m = 1
    featureslist = [];
    for i = 1:days
        one_tensor = using_tensor_flow{i};
        tempFeatures = ttm(one_tensor, {lastB,lastC}, [2 3]); %<-- same as above
        tempFeatures = reshape(double(tempFeatures),1,dim_v1);
        featureslist = [featureslist;tempFeatures];
    end
    
    tempmodel = svmtrain(price', sparse(featureslist),  '-c 0.1 -s 4 -t 0');
    A = tempmodel.w;
    bias = tempmodel.bias;
    
    % m = 2
    tempmodel=[];
    featureslist = [];
    for i = 1:days
        one_tensor = using_tensor_flow{i};
        tempFeatures = ttm(one_tensor, {A,lastC}, [1 3]); %<-- same as above
        tempFeatures = reshape(double(tempFeatures),1,dim_v2);
        featureslist = [featureslist;tempFeatures];
    end
    
    tempmodel = svmtrain(price', sparse(featureslist), '-c 0.1 -s 4 -t 0');
    B = tempmodel.w;
    bias = tempmodel.bias;
    
    % m = 3
    tempmodel=[];
    featureslist = [];
    for i = 1:days
        one_tensor = using_tensor_flow{i};
        tempFeatures = ttm(one_tensor, {A,B}, [1 2]); %<-- same as above
        tempFeatures = reshape(double(tempFeatures),1,dim_v3);
        featureslist = [featureslist;tempFeatures];
    end
    
    tempmodel = svmtrain(price', sparse(featureslist),  '-c 0.1 -s 4 -t 0');
    C = tempmodel.w;
    bias = tempmodel.bias;
    
    % 显示和上次训练结果的差值
    dispA = sum((A - lastA).^2);
    dispB = sum((B - lastB).^2);
    dispC = sum((C - lastC).^2);
    totaldisp = dispA + dispB + dispC;
    disp(num);
    num = num + 1;
    disp(totaldisp);
    disp(bias - lastbias);
    lastA = A;
    lastB = B;
    lastC = C;
    lastbias = bias;
    
end

end
