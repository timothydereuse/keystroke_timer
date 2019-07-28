from pynput.keyboard import Key, Listener
import time
import csv
from argparse import ArgumentParser


def cur_time():
    return int(round(time.time() * 1e3))


def log_to_csv(log, fname, include_releases):
    with open(fname, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in log:
            if not include_releases and row[2] == 0:
                continue
            writer.writerow([
                row[0],
                row[1].name if hasattr(row[1], 'name') else row[1],
                row[2]
            ])


class keystrokeListener(object):

    def __init__(self, verbose):
        self.log = []
        self.start_time = -1
        self.verbose = verbose
        pass

    def on_press(self, key):
        if key == Key.esc:
            self.log.append((cur_time() - self.start_time, key, 1))
            return False
        if self.start_time == -1 and key == Key.space:
            print('Beginning log - hit esc to finish')
            self.start_time = cur_time()
            self.log.append((0, key, 1))
            return
        elif self.start_time == -1:
            return
        self.log.append((cur_time() - self.start_time, key, 1))
        if self.verbose:
            print(f'Press: {key}')

    def on_release(self, key):
        if self.start_time == -1:
            return
        self.log.append((cur_time() - self.start_time, key, 0))
        if self.verbose:
            print(f'Release: {key}')
        return

    def record_log(self):
        if self.verbose:
            print("Press spacebar to begin logging.")

        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        return self.log


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="write csv of keystrokes to this file", metavar="FILE")
    parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose", default=False,
                        help="don't print keypress messages to stdout")
    parser.add_argument("-r", "--releases",
                        action="store_true", dest="releases", default=False,
                        help="log key releases as well as keypresses")

    args = parser.parse_args()

    fname = f'{args.filename}.csv'
    kl = keystrokeListener(args.verbose)
    log = kl.record_log()
    log_to_csv(log, fname, include_releases=args.releases)