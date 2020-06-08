import  unittest
from main import app
#测试方法运行命令：
#python -m unittest discover#运行测试
#要查看测试代码的覆盖率
#coverage run -m unittest discover#首先需要运行该命令
#coverage report#然后运行该命令查看测试代码的覆盖率
class test_danyuan(unittest.TestCase):
    def setUp(self):#测试用例之前运行，
        print('up')
        #获取数据库连接
        self.app=app.test_client()
    def tearDown(self):#测试用例之后运行
        print('down')
        #释放数据库连接
    def test_login(self):#具体的测试用例
        print('测试中')
        rv=self.app.get('/')
        print(type(rv.data))
        print(rv.data.decode('utf-8'))
        assert '起飞的木木' in rv.data.decode('utf-8')
