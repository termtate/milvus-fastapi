# 架构说明
[milvus的一个collection不允许超过64个字段](https://milvus.io/docs/limitations.md#Number-of-resources-in-a-collection)，但是output.xlsx内有80个字段，所以需要分表处理，models中的patients, patient_2就是划分出的两个表。  
proxy.py内的`CollectionProxy`类是`Collection`类的代理类，承担了全部了增删改查时分表的工作，在调用时和正常`Collection`类没有区别。
