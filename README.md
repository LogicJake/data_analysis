# 数据融合和智能分析实验
## 网易云音乐歌曲评论情感倾向分析
### 问题描述
该问题为二分类问题，通过朴素贝叶斯算法将评论分为积极和消极两种。
### 问题解决
#### 数据准备
自己在之前暑假的时候，曾经爬取过周杰伦歌曲《等你下课》下面的评论，总计1w条。首先对评论进行标注，人工完成标注是不现实的，所以采用百度的情感倾向分析api完成标注，api地址：  
  
https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify  
  
百度api的情感分析会将评论分为三类，积极，消极和中立，在这里只研究积极和消极部分，其中积极取值为1，消极取值为0。整理后得到4378条积极评论，2604条消极评论。其中70%作为训练集，30%作为测试集。
#### 情感倾向分析
首先生成词汇表，通过jieba分词将评论分词，并利用停用词文件去除停用词，减少词汇量，这样就生成了不重复的词汇表。    
  
训练测试数据，将待训练的评论转成词袋，即该评论分出来的词语，在词汇表中出现的次数，生成了一个一维向量。特征即为词汇表中的单词在该评论中出现的次数。将测试集处理完毕后得到两个数组，特征数组和特征对应的标注数组，利用朴素贝叶斯对其进行训练。训练完成后即可利用模型对测试数据进行测试。
### 实验结果
错误率为0.385    

本实验中模型分类的对错是以百度api的标注结果为准，而百度api给出的标注结果也不一定完全准确，当然这也是在数据量比较大之下的无奈之举，也是本实验的瑕疵。另外由于评论数较多，生成的词汇表过大，从而导致特征量过多，引入了干扰，这也是本实验的不足。
## 基于颜色信息的图像分割
### 问题描述
利用KMeans对图像颜色聚类。
### 问题解决
遍历图片得到每个像素点的RGB值，以RGB三色值进行KMeans聚类，根据聚类结果将相同类的像素点涂上相同的颜色。
### 实验结果
| 原图 | K=2 | K=3 | K=5 |
|:-:|:-:|:-:|:-:|
|![raw](https://github.com/LogicJake/data_analysis/blob/master/cluster/pic.jpg?raw=true)|![2](https://github.com/LogicJake/data_analysis/blob/master/cluster/pic/cluster_2.jpg?raw=true)|![3](https://github.com/LogicJake/data_analysis/blob/master/cluster/pic/cluster_3.jpg?raw=true)|![5](https://github.com/LogicJake/data_analysis/blob/master/cluster/pic/cluster_5.jpg?raw=true)|
## 可视化遗传算法
### 问题描述
在一张地图上只有一块地方可以被阳光照射到，其余地方为阳光照射不到的黑色区域。现在全图存在一种绿色植物，他需要阳光生存，根据大自然的选择，生长在黑暗区域的植物会被淘汰，从而导致植物向阳光照射区域生长。下图为初始地图，其中绿色为初始的植物生长点，要让其集中生长于中间白色区域。
  
![raw](https://github.com/LogicJake/data_analysis/blob/master/optimization/pic.jpg?raw=true)
### 问题解决
植物的属性为其在图片上的坐标，并将坐标值转成二进制串，从而变成他的一对基因，x基因和y基因，代表坐标x，y值。每个植物所在位置的图片颜色值RGB转成灰度值，范围从0到255，白色为255，灰度值越大越靠近白色。所以灰度值为适应度值。
  
生成第一代植物，种群数量为图片像素总个数的1/3。利用随机数将其随机分布在全图。  

适者生存，计算每个植物的适应度值，从而计算出选择概论和积累概率，根据赌轮选择法选出能够交互基因的那部分植物。根据交叉率决定需要交叉多少对植物，随机选择一段基因完成互换，从而得到新的基因，注意交叉完毕后要检查基因代表的坐标是否处理图片范围内，否则重新交换。
  
根据变异率决定变异多少位的基因，从交叉后的种群中随机选择一个植物，再随机选择某位基因进行变异，变异操作为0变1，1变0。
### 实验结果
| 初始分布 | 第一代 | 第二代 | 第三代 | 第四代 |
|:-:|:-:|:-:|:-:|:-:|
|![raw](https://github.com/LogicJake/data_analysis/blob/master/optimization/pic/0.jpg?raw=true)|![2](https://github.com/LogicJake/data_analysis/blob/master/optimization/pic/1.jpg?raw=true)|![3](https://github.com/LogicJake/data_analysis/blob/master/optimization/pic/2.jpg?raw=true)|![5](https://github.com/LogicJake/data_analysis/blob/master/optimization/pic/3.jpg?raw=true)|![5](https://github.com/LogicJake/data_analysis/blob/master/optimization/pic/4.jpg?raw=true)|
| 第五代 | 第六代 | 第七代 | 第八代 | 第九代 |
|![raw](https://github.com/LogicJake/data_analysis/blob/master/optimization/pic/5.jpg?raw=true)|![2](https://github.com/LogicJake/data_analysis/blob/master/optimization/pic/6.jpg?raw=true)|![3](https://github.com/LogicJake/data_analysis/blob/master/optimization/pic/7.jpg?raw=true)|![5](https://github.com/LogicJake/data_analysis/blob/master/optimization/pic/8.jpg?raw=true)|![5](https://github.com/LogicJake/data_analysis/blob/master/optimization/pic/9.jpg?raw=true)|
