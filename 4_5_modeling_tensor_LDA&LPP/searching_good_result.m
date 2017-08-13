%找到结果还不错的结果参数
%
good_result = [];
for i = 1:size(total_res,1)
    if total_res(i,2)<=0.0041 && total_res(i,1)>= 25
        good_result = [good_result;total_res(i,:)];
    end
end
disp('好结果的个数');
disp(size(good_result,1));
save good_result good_result
