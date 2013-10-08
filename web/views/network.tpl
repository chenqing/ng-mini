<!DOCTYPE html>
<html>
<head>
    <title>{{host}} 服务器流量图</title>
    <link rel="stylesheet" href="static_files/css/pure-min.css">
    <link rel="stylesheet" href="static_files/css/baby-blue.css">
<style type="text/css">body {
 text-shadow: 0px 0px 1px #909090 !important;
}</style>
</head>
<body>

    <div class="pure-g-r" id="layout">
        <a href="#menu" id="menuLink" class="pure-menu-link">
    <span></span>
</a>

<div class="pure-u" id="menu">
    <div class="pure-menu pure-menu-open">
        <a class="pure-menu-heading" href="/">ng-mini</a>

        <ul>

            <li class=" ">
                <a href="/mini">汇总图</a>
            </li>

            <li class=" ">
                <a href="/network">流量图</a>
            </li>

            <li class=" ">
                <a href="/other">其它</a>
            </li>
        </ul>
    </div>
</div>


<div class="pure-u-1" id="main">

<div class="header">
    <h2>{{host}} 流量 图</h2>
</div>


<div class="content">


    <div class="layout-item pure-g-r">
		<img src="./static_files/pic/rrd/ng-mini-network-day.png">
    </div>
    <div class="layout-item pure-g-r">
		<img src="./static_files/pic/rrd/ng-mini-network-week.png">
    </div>
    <div class="layout-item pure-g-r">
		<img src="./static_files/pic/rrd/ng-mini-network-month.png">
    </div>
    <div class="layout-item pure-g-r">
		<img src="./static_files/pic/rrd/ng-mini-network-year.png">
    </div>

</div>


<div class="legal pure-g-r">
    <div class="pure-u-2-5">
        <div class="l-box">
            <p class="legal-license">
                CPIS@CHINACACHE.COM
            </p>
        </div>
    </div>

</div>


</div>
</div>

</body>
</html>
