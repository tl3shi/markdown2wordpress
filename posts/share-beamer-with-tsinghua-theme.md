---
title: 分享一个清华主题的beamer模版
permalink: share-beamer-with-tsinghua-theme
layout: post
tags: latex beamer tsinghua 学位论文答辩 ppt 模版
categories: MyLife 清华大学 
published: true
---

在这里分享一个清华主题的latex beamer模版，我硕士学位论文答辩就是用的这个，我从[这里](http://far.tooold.cn/post/latex/beamertsinghua)改编的，感谢原作者。这还有[另外一个中文beamer模版](https://github.com/forhappy/aliyun-pk-report-2012)供参考。

我在原文“一个清华的beamer主题[^1]”的基础上添加了中文支持，修改了封面，下图封面的是效果图。完整的效果可以看[这里](https://github.com/tl3shi/THUBeamer/blob/master/tanglei_thesis_report.pdf)。

<center>
![Tisnghua-beamer学位论文答辩PPT封面](./share-beamer-with-tsinghua-theme/tanglei_thesis_report-0.png)
</center>

此外，我修改后的这个latex beamer模版还集成了一些常用的功能，跟原文相比增加了比如：(1) 页码显示，这是答辩过程中常用的；(2) 参考文献的引用方式引用页脚注和尾页集中同步展示；(3) 示例中还包括也些算法的引用等。CS等相关专业可以直接copy改改就用，省得自己再去查。

<center>
![](./share-beamer-with-tsinghua-theme/tanglei_thesis_report-1.png)
![](./share-beamer-with-tsinghua-theme/tanglei_thesis_report-2.png)
</center>

感兴趣的同学可以从 [这里fork或者下载：THUBeamer](https://github.com/tl3shi/THUBeamer)，其中 [tanglei_thesis_report.tex](https://github.com/tl3shi/THUBeamer/blob/master/tanglei_thesis_report.tex) 为我自己学位论文答辩用到的PPT的精简版，[tsinghua_test.tex](https://github.com/tl3shi/THUBeamer/blob/master/tsinghua_test.tex)为原来版本的简单修改，你可以根据兴趣选择参考的模版。

这里也分享下我在写这个ppt时遇到的一些关于latex、beamer等问题。

- 改变footnote大小 ```\setbeamerfont{footnote}{size=\tiny}```
- 改变caption大小 ```\setbeamerfont{caption}{size=\scriptsize}```
- 设置caption自动标号 ```\setbeamertemplate{caption}[numbered]```
- 设置subfig的label大小 ```\usepackage[caption=false,font=scriptsize]{subfig}```
- 目录文字大小 ```\setbeamerfont{subsection in toc}{size=\footnotesize}```
- 目录章节控制  ```\tableofcontents[sections={<1-5>}]```
- 是否显示note \setbeameroption{show notes} %un-comment to see the notes 
- 公式中的粗体斜体问题 ```\usepackage[BoldFont,SlantFont]{xeCJK}```
- 参考文献的图标改成文字[^3] ```\setbeamertemplate{bibliography item}[text]``` [ref](http://tex.stackexchange.com/questions/68080/beamer-bibliography-icon) 
- 参考文献字体大小 ```\renewcommand*{\bibfont}{\footnotesize}```
- 参考文献格式 ```\usepackage[backend=bibtex,sorting=none]{biblatex}```
- beamer单页上要引用多次reference：
     - 避免重复的的footnote[^4][ref](http://tex.stackexchange.com/questions/35043/reference-different-places-to-the-same-footnote)
     - autocite的方式 
- xelatex 编译提示 ```** WARNING ** Version of PDF file (1.5) is newer than version limit specification ```，需要编译时加参数选项 ```xelatex -output-driver="xdvipdfmx -V 5"  source.tex ```, 具体根据 version版本改相应参数；
- xelatex mac下中文乱码，
两种方法： 
	- 编译不过， 提示*SIMKAI.TTF*找不到, 可以按照[此文](http://albertcn.blog.163.com/blog/static/2094201452013521105128316/)[^5]修改```/usr/local/texlive/2014/texmf-dist/tex/latex/ctex/fontset/ctex-xecjk-winfonts.def ``` 文件即可;
	- 不修改全局的上面那个文件，当前文件使用nofonts选项，如 	```\documentclass[a4paper,nofonts]{article}```， 然后自定义类型如```\setCJKmainfont[BoldFont={Adobe Heiti Std},ItalicFont={Adobe Kaiti Std}]{SimSun}``` 再编译即可，或者```\setCJKmainfont[BoldFont={SimHei},ItalicFont={KaiTi_GB2312}]{SimSun} ``` 改成本机有的;
	- 若编译过了，还是乱码，记得看你tex源文件的编码，是不是UTF-8。```set fileencoding=utf-8```
- PPT章节切换时添加目录 

	```
	\AtBeginSubsection[] {
	  \frame<handout:0> {
	  \frametitle{目录}
	  %  \begin{multicols}{2}
	  \tableofcontents[current,currentsubsection,sections={<1-5>}]
	  %\end{multicols}
	    }
	    \addtocounter{framenumber}{-1}  %目录页不计算页码
	  }
	```

答辩时用beamer有不好的方式就是:

- beamer 动画不好做，我答辩时准备嵌入动画，复杂也不太容易，另一个可选的方案是简单的动画做成gif动图，外部浏览器打开等；所以如果你希望自己的PPT足够绚丽多姿，那还是用MS的Office更好;
- beamer 排练计时不太方便，演讲时看备注也不那么方便，这里有一个用```\note```做双屏注释的教程，还不是那么容易;[^2]
- beamer 制作过程中也没PPT那么简单，不满足*WYSIWYG*, 时不时还报错什么的难得debug; 

总之在选latex做PPT时还是要好好考虑一下，当然写论文排版什么的力推latex。就酱。

参考文献：

[^1]: [一个清华的beamer主题](http://far.tooold.cn/post/latex/beamertsinghua) 
[^2]: [beamer+xelatex使用\note做双屏注释](http://bbs.ctex.org/forum.php?mod=viewthread&tid=71817)
[^3]: [Beamer Bibliography Icon](http://tex.stackexchange.com/questions/68080/beamer-bibliography-icon)
[^4]: [Reference different places to the same footnote](http://tex.stackexchange.com/questions/35043/reference-different-places-to-the-same-footnote)
[^5]: [texlive的中文问题](http://albertcn.blog.163.com/blog/static/2094201452013521105128316/)
