final_corpus.txt 是我们通过get_feature得到的自己的财经新闻语料库，是复制到这的。
test_news.txt和test_price.csv是我们爬下来的关于某一只股票的新闻列表和价格列表

cal_increment.py 是计算股价各种值的示例程序，如增量。
make_news.py 示例程序,倒序读入新闻，和股价对应,得到date_list

build_data.py 是造出数据集，把同一天的新闻链接在一起。得到data.txt