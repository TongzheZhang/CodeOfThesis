function [re_tensor_flow,tensor_flow] = con_tensor_flow(total_len,dim1,dim2,dim3,conmethod,whenormlize)
%构建两个张量流
%   之后要加入用什么方法构建的选项，外积法，还是三棍法
%   conmethod是构建方法，可以选择threestick，或者默认的外积构建法
%% 载入特征
load('E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\firm_features.mat');
load('E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\news_features_pca.mat');%注意对公司提取的特征是经过PCA降维之后的结果
load('E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\emo_features.mat');
%% 归一化,归一化好像对张量回归不好
if strcmp(whenormlize,'yes')
emo_features = normc(emo_features);
firm_features = normc(firm_features);
news_features = normc(news_features);
end
%构建原始的张量流
tensor_flow = cell(1,size(emo_features,1));
%构建tucker分解之后的重构后的张量流
re_tensor_flow = cell(1,size(emo_features,1));
%% 重构过程
for i = 1:total_len
    M = zeros(6,100,6);
    if strcmp(conmethod,'threestick')
        %disp('使用三个棍构建法');
        M(:,1,1) = firm_features(i,:);
        M(2,:,2) = news_features(i,:);
        M(3,3,:) = emo_features(i,:);
    else
        M = outproducts(firm_features(i,:),news_features(i,:),emo_features(i,:));
        %disp('使用外积构件法');
    end
    
    T = tensor(M);
    tensor_flow{i} = T;
    re_tensor_flow{i} = re_tensor_tucker(T,dim1,dim2,dim3);
end
%% 把重构前的流和重构后的流都保存下来，统称tensor_flow
save tensor_flow tensor_flow re_tensor_flow;
end