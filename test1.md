wordpress 绑定m.tanglei.name 访问此 都以wptouch主题访问。
 
最终解决方案： 手动设置UA，让wptouch后台添加设置的UA能够match后切换。相关联系太多，不能直接设置is_mobile_device为true或者直接```$this->is_supported_device()```返回true。
vim core/class-wptouch-pro.php 中的```is_supported_device()```方法中：

```php
$domain = $_SERVER['HTTP_HOST'];
if ($domain == 'm.tanglei.name')
     $_SERVER['HTTP_USER_AGENT']='tanglei’; //跟wptouch admin后台设置的一样即可
```

首页解决了～ 还得改首页上的链接～ 这些链接都是www打头的～ 

vim wp-config.php 添加如下设置，成功后 WP后台设置-常规中wordpress地址和站点地址不可编辑。

```php
//multiple domain set tanglei begin
$tangleihome = 'http://'.$_SERVER['HTTP_HOST'];
$tangleisiteurl = $tangleihome;
define('WP_HOME', $tangleihome);
define('WP_SITEURL', $tangleisiteurl);
//multiple domain set tanglei end
```

对SEO不太好～管他呢～