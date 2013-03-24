import subprocess


class Code(str):
    cc = 'cc'

    def compile(self):
        subprocess.call(['cc', '-x', 'c', '-'], self)
