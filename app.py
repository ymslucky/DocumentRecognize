import waitress

from system.configuration import SystemConfiguration

if __name__ == '__main__':
    SystemConfiguration.initialize()
    waitress.serve(SystemConfiguration.APP, host='0.0.0.0', port=5000)
