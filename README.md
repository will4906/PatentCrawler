# PatentCrawler

专利爬虫
使用说明见[WIKI](https://github.com/will4906/PatentCrawler/wiki)

### Environment

* pip install -r requirements.txt
* 另外再安装tesseract-ocr

### ReleaseNote

* V3.0
    * 解决了由于网站升级需要注册登录账号才能查询的问题。
    * 实现了自动验证码识别
* V2.0
    * 使用scrapy框架爬取
    * 大幅度缩减代码
    * 加快了爬取速度
    * FixBug: 解决了首次爬取总是失败的问题
    * 详细原理：[http://blog.csdn.net/will4906/article/details/72625164](http://blog.csdn.net/will4906/article/details/72625164)
* V1.0
    * 使用selenium模拟爬取
    * javascript解析
    * 简单介绍：csdn博客：[http://blog.csdn.net/will4906/article/details/68955619](http://blog.csdn.net/will4906/article/details/68955619)

### TODO

* 继续完善表达式生成
* 随着软件的日益复杂，准备升级成web形式供大家使用，敬请期待。

### License

PatentCrawler is released under the Apache 2.0 license.
```
Copyright 2017 willshuhua.me.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
### 感谢支持

<table width="100%">
<tr><td align="center" colspan="2">赞赏</td></tr>
    <tr>
        <td align="center">
        <img src="http://img.blog.csdn.net/20170521121423299?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvd2lsbDQ5MDY=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" width="200px" alt="微信支付">
        </td>
        <td align="center">
        <img src="http://img.blog.csdn.net/20170521131930503?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvd2lsbDQ5MDY=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" width="200px" alt="支付宝">
        </td>
    </tr>
    <tr>
    <td align="center">微信</td>
    <td align="center">支付宝</td>
    </tr>
</table>