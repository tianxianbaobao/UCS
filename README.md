
# UCS
UCAS course sync tool  
国科大课件资料同步工具

# Requirement

python 2.7+

# Quick Start

- download  
```shell
git clone https://github.com/tianxianbaobao/UCS.git
```
2. config  
在ucs.config文件中，依次填入用户名，密码，和课件同步位置,如:

		[USER]
		usrname=tianxianbaobao
		passwd=123abc
		savedir=Courses

- run  
```python
python login.py
```

# Issue
建议写成alias

网上资源存在多级目录情况的处理

受版权保护文件的下载

（Optional）更好的增量同步方法
