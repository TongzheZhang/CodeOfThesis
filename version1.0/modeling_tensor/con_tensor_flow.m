function [tensor_flow] = con_tensot_flow(  )
%构建张量流
load('firm_features.mat')
load('news_features.mat')
load('emo_features.mat')
tensor_flow = cell(1,size(emo_features,1));
re_tensor_flow = cell(1,size(emo_features,1));

for i = 1:221
    M = zeros(6,100,3);
    M(:,1,1) = firm_features(i,:);
    M(2,:,2) = news_features(i,:);
    M(3,3,:) = emo_features(i,:);
    T = tensor(M);
    tensor_flow{i} = T;
    re_tensor_flow{i} = re_tensor_tucker(T);
end

save tensor_flow tensor_flow re_tensor_flow
end