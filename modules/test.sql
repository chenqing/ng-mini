create table `test` ( 
    `id` int(12) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY , 
    `hostname` varchar(100) NOT NULL,
    `load` float(4) NOT NULL , 
    `time` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )DEFAULT CHARSET='UTF8';
