%对价格相似度方法的主函数
clear;
tensor_flow = con_tensor_flow();
load('price_list.mat');
load('tensor_flow.mat');
% 训练得到V1,V2,V3
[V1,V2,V3] = re_co_tensor_tucker();
days = 221;
re_co_tensor_flow = cell(1,days);
for i = 1:days
    re_co_tensor_flow{i} = re_co_tensor_tucker_single(tensor_flow{i},V1,V2,V3);
end