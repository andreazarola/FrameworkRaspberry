from threading import Thread


class HiveThreadingRequest(Thread):

    def __init__(self, hive_request):
        self.hive_request = hive_request
        super(HiveThreadingRequest, self).__init__()

    def run(self):
        try:
            self.hive_request.execute()
            self.hive_request.close_connection()
        except Exception as e:
            print(str(e))