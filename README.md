# pokemon-crawler
该项目使用 python scrapy 爬取 [神奇宝贝百科](https://wiki.52poke.com/wiki/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89/%E7%AE%80%E5%8D%95%E7%89%88) 的所有神奇宝贝的各项数据，并将数据保存至 MongoDB 中

## 安装 packages
**scrapy**  
[scrapy](https://docs.scrapy.org/en/latest/intro/install.html) 是一个Python编写的开源网络爬虫框架，优势在于使用异步处理请求和通过 pipelines 将数据保存至数据库
```
$ conda install -c conda-forge scrapy
```

**pymongo**  
[pymongo](https://pypi.org/project/pymongo/) 是 MongoDB 的 python 实现
```
$ pip install pymongo
```

**BeautifulSoup**   
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 是一个可以从HTML或XML文件中提取数据的Python库
```
$ pip install beautifulsoup4
```

## 安装 MongoDB 
**MongoDB**  
[MongoDB](https://www.mongodb.com/) 是一个基于分布式文件存储的开源数据库系统  
在 MongoDB 网站上下载压缩文件 [mongodb community server](https://www.mongodb.com/download-center/community)
解压缩文件，并将文件复制到 /usr/local/mongodb 文件目录下   
```
$ sudo mv mongodb-osx-ssl-x86_64-4.0.8.tgz /usr/local/mongodb
```
进入 /usr/local/mongodb 目录   
```
$ cd /usr/local/mongdb
```
创建用于保存数据库的文件夹   
```
$ sudo mkdir -p /data/db
```
设置 /data/db 的读写权限   
```
$ sudo chown username /data/db
```
进入根目录
```
$ cd
```
打开 .bash_profile
```
$ open .bash_profile
```
将 export MONGO_PATH=/usr/local/mongodb 和 export PATH=$PATH:$MONGO_PATH/bin 粘贴至 .bash_profile 中保存

## 运行
在 /pokemon 目录下 运行 scrapy crawl pokemons 即可开始爬取 Pokemon 的各项数据  
并保存至 MongoDB
![pokemons-stats-mongodb-screenshot.png](https://github.com/ezra1218/pokemon-crawler/blob/master/pokemons-scrapy/IMG/pokemons-stats-mongodb-screenshot.png)
