import time
import concurrent.futures
import datetime
import re
import subprocess
import os







class Dual_consol():

    def __init__(self, input_file, filename_output):
        self.input = input_file
        self.filename = filename_output
        self.main()

    def crawler_checkserver(self, line, nb_line):
        print("execute: " + str(nb_line))
        time.sleep(2)
        datenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return datenow, line, "serveur ok"

    def returncrawler(self, fd, lineexec):
        lists = ', '.join(lineexec.result())
        fd.write('{0}\n'.format(lists))
        fd.flush()


    def main(self):
        lines = [line.rstrip('\n') for line in open(self.input)]

        print("\nnous sommes le ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("PID : " + str(os.getpid()), "\n")

        print("il y à (", len(lines), ") éléments")
        os.environ['DISPLAY'] = ':0'
        # Open file for output
        fd = open(self.filename, "w")
        # Open xterm window with logs from that
        # file
        title = "Process PID : " + str(os.getpid())
        p = subprocess.Popen(["xterm",
                      "-xrm",
                      'XTerm.vt100.allowTitleOps: false',
                      "-T",
                      title,
                      "+sb",
                      "-geometry",
                      "70x15+300+100",
                      "-e",
                      "tail",
                      "-f",
                      self.filename], stdout=subprocess.PIPE, shell=False)

        #os.system("notify-send '" + title + "' 'Execution...'")
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            for i, line in enumerate(lines):
                # exec multi thread
                executor.submit(self.crawler_checkserver, line, i).add_done_callback(lambda x: self.returncrawler(fd, x))

        #os.system("notify-send '" + title + "' 'à terminer'")
        p.kill()


if __name__ == "__main__":
    consol = Dual_consol("server.txt", "output")
