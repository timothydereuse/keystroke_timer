from pynput.keyboard import Key, Listener
import time
import csv


def cur_time():
    return int(round(time.time() * 1e3))


def log_to_csv(log, fname, include_releases=True):
    with open(fname, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in log:
            if not include_releases and log[2] == 0:
                continue
            writer.writerow([
                row[0],
                row[1].name if hasattr(row[1], 'name') else row[1],
                row[2]
            ])

class keystrokeListener(object):

    def __init__(self):
        self.log = []
        self.start_time = -1
        pass

    def on_press(self, key):
        if key == Key.esc:
            self.log.append((cur_time() - self.start_time, key, 1))
            return False
        if self.start_time == -1 and key == Key.space:
            print('beginning log...')
            self.start_time = cur_time()
            self.log.append((0, key, 1))
            return
        elif self.start_time == -1:
            return
        self.log.append((cur_time() - self.start_time, key, 1))
        print(f'{key} press')

    def on_release(self, key):
        if self.start_time == -1:
            return
        else:
            self.log.append((cur_time() - self.start_time, key, 0))
            print(f'{key} release')
            return

    def record_log(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        return self.log


if __name__ == "__main__":
    fname = 'testcsv.csv'
    kl = keystrokeListener()
    log = kl.record_log()
    log_to_csv(log, fname)