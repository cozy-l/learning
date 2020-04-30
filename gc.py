class classA():

    def __init__(self):
        print('object born, id:%s' % str(hex(id(self))))

    def __del__(self):
        print('object del,id:%s' % str(hex(id(self))))

