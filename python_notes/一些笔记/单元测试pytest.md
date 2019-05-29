在程序的目录中创建test文件夹。  
在设置中开启pytest 选项  
`"python.unitTest.pyTestEnabled": true,`  
复制到工作区设置  
vscode中安装pytest  pipenv install pytest

```
tests
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-36.pyc
│   ├── mydict_test.cpython-36-PYTEST.pyc
│   └── test1.cpython-36.pyc
├── mydict_test.py
└── test1.py
```
test1.py
```
class Dict(dict):
    def __init__(self, **kw):
        super().__init__(**kw)
    
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
    
    def __setattr__(self, key, value):
        self[key] = value
```
test_mydict.py
```
import pytest

from tests.test1 import Dict


def test_init():
    d = Dict(a=1, b=2)
    assert d.a == 1
    assert d.b == 2


def test_attrerror():
    with pytest.raises(AttributeError):
        d = Dict()
        value = d.empty


def test_key():
    d = Dict()
    d['key'] = 'value'
    assert d.key == 'value'


def test_keyerror():
    d = Dict()
    with pytest.raises(KeyError):
        value = d['key']



def test_attr():
    d = dict()
    d['key'] = 'value'
    assert 'key' in d
    assert d['key'] == 'value'
```

pytest logs
```
============================= test session starts ==============================
platform darwin -- Python 3.6.6, pytest-3.9.3, py-1.7.0, pluggy-0.8.0
rootdir: /Users/admin/Pycharmprojects/microblog, inifile:
collected 5 items

tests/test_mydict.py .....                                               [100%]

 generated xml file: /var/folders/d8/hpn8d9yj11vdnzc_z71jhryh0000gn/T/tmp-6158ak2oMzTkBTUC.xml 
=========================== 5 passed in 0.05 seconds ===========================
```


##  将一个函数作为参数传入另一个函数
```
@pytest.fixture(scope='function')
def some_resource(request):
    '重复利用的组件'
    stuff_i_setup = ["I setup"]

    def some_teardown():
        stuff_i_setup[0] += " ... but now I'm torn down..."
        print(stuff_i_setup[0])
    request.addfinalizer(some_teardown)

    return stuff_i_setup[0]


def test_1_that_needs_resource(some_resource):
    print(some_resource + "... and now I'm testing things...")
```

在进入执行 测试完成后再执行  
模块级别 `setup_module ` 
类级别   @classmethod def setup_class(cls):  
方法级别 setup_method  
函数级别 setup_function  

