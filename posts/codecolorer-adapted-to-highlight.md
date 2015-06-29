---
title: 将代码高亮插件codecolorer替换为highlight
permalink: codecolorer-adapted-to-highlight
layout: post
tags: 经验技巧 codecolorer highlight 代码高亮 wordpress plugin
categories: 经验技巧 我做站长 wordpress
published: True
---

最近在写一个wordpress小的客户端发布工具，就是直接写markdown，然后转为html发布到wordpress，为什么要写?

- 不太想换之前已有的blogs，试过相应的工具将已有的wordpress blog转为markdown，效果不是很好。//直接用github+jekyll之类的静态站点
- wordpress已有的支持markdown的插件貌似都不怎么理想，想兼容之前的比较麻烦，特别是用了代码高亮之类的插件//用wordpress已有的支持markdown的插件

所以就写了，目前的技术方案是：
```本地markdown+pandoc——>html——>wordpress-xmlrpc——>wordpress server```
这样的好处是：不需要对已有的blog进行较大的改动，


将代码高亮插件codecolorer替换为highlight
