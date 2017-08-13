function [A,B,C,bias] = tensor_reg(re_co_tensor_flow)
%% 
% 训练张量回归参数，最终返回A,B,C,bias

days = 177;% 选取前n天训练
%% 读入数据
load('tensor_flow.mat');
load('price_list.mat');
using_tensor_flow = re_co_tensor_flow(1:221);%可以更改为不同的重构方式
price = price_list(1:days)*1000;%升降幅度提升，数值过小，所以乘以1000，选取前n天训练
%% 赋予初始值
A = ones(1,6);B = ones(1,100);C = ones(1,3);bias = 0;
lastA = ones(1,6);lastB = ones(1,100);lastC = ones(1,3);lastbias = 0;

%% 训练
num = 1;
while num < 2000 % 设置为2000
    
    % 根据m的不同，把张量转化为向量
    % m = 1
    featureslist = [];
    for i = 1:days
        one_tensor = using_tensor_flow{i};
        tempFeatures = ttm(one_tensor, {lastB,lastC}, [2 3]); %<-- same as above
        tempFeatures = reshape(double(tempFeatures),1,6);
        featureslist = [featureslist;tempFeatures];
    end
    
    tempmodel = train(price', sparse(featureslist), '-s 13');
    A = tempmodel.w;
    bias = tempmodel.bias;
    
    % m = 2
    featureslist = [];
    for i = 1:days
        one_tensor = using_tensor_flow{i};
        tempFeatures = ttm(one_tensor, {A,lastC}, [1 3]); %<-- same as above
        tempFeatures = reshape(double(tempFeatures),1,100);
        featureslist = [featureslist;tempFeatures];
    end
    
    tempmodel = train(price', sparse(featureslist), '-s 13');
    B = tempmodel.w;
    bias = tempmodel.bias;
    
    % m = 3
    featureslist = [];
    for i = 1:days
        one_tensor = using_tensor_flow{i};
        tempFeatures = ttm(one_tensor, {A,B}, [1 2]); %<-- same as above
        tempFeatures = reshape(double(tempFeatures),1,3);
        featureslist = [featureslist;tempFeatures];
    end
    
    tempmodel = train(price', sparse(featureslist), '-s 13');
    C = tempmodel.w;
    bias = tempmodel.bias;
    
    % 显示和上次训练结果的差值
    dispA = sum((A - lastA).^2);
    dispB = sum((B - lastB).^2);
    dispC = sum((C - lastC).^2);
    totaldisp = dispA + dispB + dispC;
    %disp(dispA);
    %disp(dispB);
    %disp(dispC);
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
