---
title: 将代码高亮插件codecolorer替换为highlight
permalink: codecolorer-adapted-to-highlight
layout: post
tags: 经验技巧 codecolorer highlight 代码高亮 wordpress plugin
categories: 经验技巧 我做站长 wordpress
published: false
---

最近在写一个wordpress小的客户端发布工具，就是直接写markdown，然后转为html发布到wordpress，为什么要写?

- 不太想换之前已有的blogs，试过相应的工具将已有的wordpress blog转为markdown，效果不是很好。//直接用github+jekyll之类的静态站点
- wordpress已有的支持markdown的插件貌似都不怎么理想，想兼容之前的比较麻烦，特别是用了代码高亮之类的插件//用wordpress已有的支持markdown的插件

所以就写了，目前的技术方案是：
```本地markdown+pandoc——>html——>wordpress-xmlrpc——>wordpress server```
这样的好处是：

- 仅仅要对已有的blog进行细小的改动即可，即改下那些po了代码的文章；
- 本地的markdown方便管理和备份，也方便生成其他如pdf等格式；
- win下之前还有wlw工具方便发布带有图片的blog，但在mac、linux下找不到相应方便的工具，现在用这个统一的client就比较方便传图片等资源。

本篇文章是讨论解决之前文章代码高亮的问题。一方面，现在的代码高亮是基于pandoc的，pandoc会把代码拆分添加各种tag，然后根据tag去css，且生成的html是与之前的codecolorer不兼容的，开启codecolorer插件后，现在的文章乱得一塌糊涂；另外一方面，关闭codecolorer后，由于现在的文章代码已经不是独立的代码，是带有各种html标签的文本，解决方案是将之前的所有post中含有的代码都用pandoc转换一下，这个成本太高；后来找到一个代码高亮的插件可以自定义代码区域的标签，且是通过前端实现的，不占用服务器资源，于是就采用了这款插件[hightlight](https://highlightjs.org/)。

codecolorer之前的代码区域基本上都是通过```[cc lang="java]java code[/cc]```实现的，hightlight可以自定义html标签，所以大致只需要将原来的文章中所有的``[cc]``` 替换成```<cc>```即可，不能用hightlight默认的```<pre><code></code><pre>```，这个又会跟pandoc的冲突。

在将代码高亮插件codecolorer替换为highlight过程中，遇到的主要问题是：

- codecolorer之前的代码区域仅用```[cc]```标签包围，highlight自定义标签时，换行符会出现问题。```hljs.configure({useBR: true});``` 不生效，参见[hightligth讨论](https://github.com/isagalaev/highlight.js/issues/860)，结果是要求code中需要包含```<br>```标签，这不扯么。。。解决方法是手动通过js添加```<br>```。
- 换行符问题解决了，代码缩进有出现问题了。囧。后来想想还是手动在```<cc>```周围添加```<pre>```吧。

代码如下:

```javascript
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.6/styles/default.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.6/highlight.min.js"></script>
<script src="http://code.jquery.com/jquery-2.1.4.min.js"></script>
<script>
   if(false)
       hljs.initHighlightingOnLoad(); //default tag<pre><code>
   else
   	$(document).ready(function() {
       //hljs.configure({useBR: true});//this does NOT work, the original code should contains <br>, see https://github.com/isagalaev/highlight.js/issues/860
       $('cc').each(function(){
           $(this).wrap("<pre></pre>");
           //var codestr = $(this).html();
           //$(this).html(codestr.replace(/\n/g, '<br>')); //manually substitute, add <pre>, no need
       });
       $('cc').each(function(i, block) {
           hljs.highlightBlock(block);
       });
   });
</script>
```

Demo如下： 
<iframe src='./codecolorer-adapted-to-highlight/highlighttest.html' width=100%>
</iframe>


然后就是使这些js代码应用到之前的所有文章中，直接添加到每篇含有代码的文章中的正文里容易被wordpress过滤转义掉，且加载的顺序不正确也会导致代码高亮出现问题，如果加在全站的header中有造成不必要的浪费，幸好wordpress提供了给每篇文章自定义的功能，wordpress后台发布文章时有个自定义栏目，可以给每篇文章加个标签，然后wp加载的时候根据这篇文章的标签采用不同的逻辑加载。方法可以参考[在 WordPress 指定页面加载指定 JavaScript 或 CSS 代码](http://loo2k.com/blog/wordpress-page-javascript-css-code/) 

最后就是修改那些含有代码的文章，修改```[cc]```标签，给文章添加自定义字段。sql语句如下：

```sql
update 
```

```php

```