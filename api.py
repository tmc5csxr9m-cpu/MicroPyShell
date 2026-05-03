import _thread
import uos
class SystemAPI:
    def __init__(self):
        self.fs_lock = _thread.allocate_lock()
        self.print_lock = _thread.allocate_lock()
        self.loglock = _thread.allocate_lock()
        self.exit = False
        self.serstat = {}
        self.log = []
    def api_print(self, pstr,end = '\n'):
        self.print_lock.acquire()
        try:
            print(pstr,end = end)
        finally:
            self.print_lock.release()
    def write_sersta(self,stat):
        self.loglock.acquire()
        try:
            self.serstat = stat
        finally:
            self.loglock.release()
    def change_ser(self,key,val):
        self.loglock.acquire()
        try:
            self.serstat[key] = val
        finally:
            self.loglock.release()
    def read_sersta(self):
        self.loglock.acquire()
        try:
            return self.serstat
        finally:
            self.loglock.release()
    def write_log(self,data):
        self.loglock.acquire()
        try:
            if len(self.log) >= 10:
                del self.log[0]
            self.log.append(data)
        finally:
            self.loglock.release()
    def read_log(self):
        self.loglock.acquire()
        try:
            return self.log
        finally:
            self.loglock.release()
    def listdir(self, path="."):
        self.fs_lock.acquire()
        try:
            return uos.listdir(path)
        finally:
            self.fs_lock.release()

    def stat(self, path):
        self.fs_lock.acquire()
        try:
            return uos.stat(path)
        finally:
            self.fs_lock.release()

    def read_file(self, path,lines = 1):
        self.fs_lock.acquire()
        try:
            with open(path, "r") as f:
                i = 1
                while lines > i:
                    f.readline()
                    lines -= 1
                return f.readline()
        finally:
            self.fs_lock.release()
            
    def get_line(self,path):
        self.fs_lock.acquire()
        try:
            with open(path, "r") as f:
                return sum(1 for _ in f)
        finally:
            self.fs_lock.release()

    def write_file(self, path, data):
        self.fs_lock.acquire()
        try:
            with open(path, "w") as f:
                f.write(data)
        finally:
            self.fs_lock.release()

    def append_file(self, path, data):
        self.fs_lock.acquire()
        try:
            with open(path, "a") as f:
                f.write(data)
        finally:
            self.fs_lock.release()

    def remove_file(self, path):
        self.fs_lock.acquire()
        try:
            uos.remove(path)
        finally:
            self.fs_lock.release()

    def mkdir(self, path):
        self.fs_lock.acquire()
        try:
            uos.mkdir(path)
        finally:
            self.fs_lock.release()

    def rmdir(self, path):
        self.fs_lock.acquire()
        try:
            uos.rmdir(path)
        finally:
            self.fs_lock.release()
    def ok(self):
        self.api_print('[INFO]API object load successfully')
system = SystemAPI()
system.ok()