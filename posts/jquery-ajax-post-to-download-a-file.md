---
title: jQuery Ajax请求下载文件资源
permalink: jquery-ajax-post-to-download-a-file 
layout: post
tags: work scala jquery 前端 
categories: 敲敲代码 Scala 工作那些事儿
published: true 
---

最近遇到这样一个问题，后端用Scala结合Play框架，前端jQuery+Bootstrap, 
需求是这样的，其实跟[SO](http://stackoverflow.com/questions/3499597/javascript-jquery-to-download-file-via-post-with-json-data)上的这个问题一样，
根据Ajax的Post请求要求server端或者直接返回Json数据或者直接返回可以下载的file文件。搜索了下问题，貌似单独一次ajax请求搞不定。

解决方案大同小异，但都是通过发请求两次；

### server端逻辑不变

server端逻辑不变，client根据server的返回判断再次post可以download的file。server端直接返回的是file，ajax请求的返回的时候再通过一样的form隐藏表单请求一次；[Handle file download from ajax post](http://stackoverflow.com/questions/16086162/handle-file-download-from-ajax-post)
Server端：

```java
if request is json
	Ok(json)
else
	Ok.sendFile(File)
```
当是filedownload的请求时，response的header如下：

```python
Content-Disposition:attachment; filename="15_08_23-11_02_57_3227832721122260226064.csv"
Content-Length:4388
Content-Type:text/csv
```

client端：

```javascript
var url = "/tool/query";
$.ajax({
    url: url,
    type: "POST",
    data: params,
    success: function(response, status, request){
      var disp = request.getResponseHeader('Content-Disposition');
        if (disp && disp.search('attachment') != -1) {
        var form = $('<form method="POST" action="' + url + '">');
        $.each(params, function(k, v) {
            form.append($('<input type="hidden" name="' + k +
                '" value="' + v + '">'));
            });
        form.appendTo('body').submit().remove();
        return;
      }
      if(response.status == "ok"){
         showResult(response.data);
      }else{
         showError('Error: ', response.msg);
      }
    }
})
```
	
确实是请求了两次，返回了两次file的内容，增大了带宽等负担，实测chrome，第一次response返回了实际的数据，第二次请求不是ajax请求，浏览器弹框保存文件，juery有log信息```Resource interpreted as Document but transferred with MIME type text/csv:```；好处client的请求不变，仅仅将Ajax请求改为不通过的form请求，server端处理简单，不需要改变，只需要一个action即可。其实再加个标记可以防止server发回两次数据的。


### server端逻辑改变

server端在第一次请求的时候不直接返回file，而是返回一个url，该url可以获取文件，通过iframe的方式再请求一次，然后iframe的src指向最新的资源(可以是直接如上得file资源)；或者直接用一个get请求去下载文件。
同样是请求了两次，第一次仅仅返回一个url(不管这个url是直接返回的file content还是说get请求)，第二次才返回真正的file内容，带宽较少，但server端需要有两个action进行处理。


Reference:

- [File Download requests using jquery/POST request with psuedo ajax](https://gist.github.com/DavidMah/3533415) 
- [Handle file download from ajax post](http://stackoverflow.com/questions/16086162/handle-file-download-from-ajax-post) 
- [Javascript/jquery to download file via POST with JSON data](http://stackoverflow.com/questions/3499597/javascript-jquery-to-download-file-via-post-with-json-data)
