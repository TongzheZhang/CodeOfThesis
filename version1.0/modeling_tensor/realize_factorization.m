%% 示例程序，初始赋值并初始化张量，实现论文上的数和程序
subs = [1 1 1;2 1 1;3 1 1;2 1 2;2 2 2;2 3 2;3 3 1;3 3 2;3 3 3;3 3 4;3 3 5];
my_sptensor = sptensor(subs,1);
my_tensor = tensor(my_sptensor);

re_my_tensor = re_tensor_tucker(my_tensor);