
# UCS
UCAS course sync tool  
国科大课件资料同步工具

![](http://i13.tietuku.com/20fe5caf84f47af0.png)

# Requirement

python 2.7+

# Quick Start (for Linux/OS X)

- download  
```shell
git clone https://github.com/tianxianbaobao/UCS.git
```

- config  
在config.ini文件中，依次填入SEP系统的用户名，密码，和课件同步位置,如:

		[USER]
		usrname=tianxianbaobao
		passwd=123abc
		savedir=MyCourses

- run  
```python
python syncc.py
```

# Quick Start (for Windows)

- 下载 [python2.7](https://www.python.org/ftp/python/2.7.10/python-2.7.10.amd64.msi)
- 下载 [ucs](https://github.com/tianxianbaobao/UCS/archive/master.zip)
- 按上一节中的方法修改config.ini文件
- 双击`synnc.py`运行同步程序


# Bug Report

[Septicmk \<mengke@ncic.ac.cn\>](mengke@ncic.ac.cn)

[Freeman \<zhangzhengyu@ncic.ac.cn\>](zhangzhengyu@ncic.ac.cn)
