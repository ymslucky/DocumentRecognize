"""
单元测试包
"""
import unittest

if __name__ == '__main__':
    from system.utils import get_project_path

    file_path = get_project_path() + 'TestResult.txt'
    file = open(file_path, 'w', encoding='utf8')

    # discover()方法加载所有测试用例进行测试
    discover = unittest.TestLoader().discover(start_dir='./', pattern='*_test.py', top_level_dir=None)
    # 实例化测试执行器
    # runner = unittest.TextTestRunner(stream=file, verbosity=2)
    runner = unittest.TextTestRunner(verbosity=2)
    # 运行测试用例
    runner.run(discover)

    print(f'测试结束，测试结果存放在 {file_path} 文件')
