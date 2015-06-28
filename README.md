# markdown2wordpress

##Wordpress markdown 发布客户端

- 依赖于 [python-wordpress-xmlrpc](https://github.com/tl3shi/python-wordpress-xmlrpc)
- 依赖于 [pandoc](http://pandoc.org/)
- 支持 makdown, 代码高亮
- 图片以 github 外链形式

## Log

- 2015-06-25
图片链接等仅支持线上的，不支持本地上传。
本地上传会出现的问题有：
    - 上传路径接口不能指定，上传后返回的url可以获得;
    - 不能从上传文件的文件名来查询server端是否存在相应的文件，因此不方便更新;
    - 所以的post存在的图片等每次多重新上传这个可以做到，但如果是更新的话会存在很多冗余
- 2015-06-26 
图片使用github外链的形式, 需要配置github代码库

