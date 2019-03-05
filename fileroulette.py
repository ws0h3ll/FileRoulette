#!/usr/bin/env python3

"""Generate random ufile.io links until a live link is found."""

import queue
import random
import requests
import threading
import webbrowser

# A list of user agents. We'll pick one at random every time.
agents = [
    'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931',
    'Chrome (AppleWebKit/537.1; Chrome50.0; Windows NT 6.3) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.9200',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
    'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
]

# Just to prevent some SSL errors.
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += \
    ':ECDHE-ECDSA-AES128-GCM-SHA256'

def create_session():
    """Create a new randomized session for a HTTP request."""
    session = requests.Session()
    session.headers.update({"User-Agent": random.choice(agents),})
    return session

def extract_filename(html):
    """Extract the filename from the provided HTML."""
    try:
        a, b = split_after(html, '<div class="details">')
        a, b = split_after(b, '<h3>')
        a, b = split_before(b, '</h3>')
        return a
    except Exception as e:
        raise

def generate_ufile_link():
    """Generate a random ufile.io link."""
    characters = "abcdefghijklmnopqrstuvwxyz0123456789"
    key = "".join([random.choice(characters) for x in range(5)])
    url = "https://uploadfiles.io/{}".format(key)
    return url

def get_head(url):
    """Request the headers for the specified URL."""
    reply = create_session().head(url)
    return reply

def get_url_status(url):
    """Get the status code of the provided URL."""
    head = get_head(url)
    if(head.is_redirect):
        head = get_head(head.headers['Location'])
    return head.status_code

def retrieve_filename(url):
    """Retrieve the filename associated with the URL.

    If the file has expired, return False. Otherwise, return the filename.
    """
    head = get_head(url)
    if(head.is_redirect):
        url = head.headers['Location']
    result = create_session().get(url).content.decode()
    if "Sorry it's gone..." in result or "Premium Access Only" in result:
        return False
    return extract_filename(result)

def split_after(source, target):
    """Split a string after the target string, returning both parts."""
    if target not in source:
        return False, False
    index = source.find(target) + len(target)
    a = source[:index]
    b = source[index:]
    return a, b

def split_before(source, target):
    """Split a string before the target string, returning both parts."""
    if target not in source:
        return False, False
    index = source.find(target)
    a = source[:index]
    b = source[index:]
    return a, b

def url_is_live(url):
    """Check whether the given URL is live."""
    if get_url_status(url) == 200:
        return True
    return False

class ScanThread(threading.Thread):
    """Spawn a thread to scan until a viable URL is found."""
    def __init__(self, work_queue):
        super(ScanThread, self).__init__()
        self.work_queue = work_queue
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            url = generate_ufile_link()
            if url_is_live(url):
                filename = retrieve_filename(url)
                if(filename):
                    # Found one!
                    self.work_queue.put((url, filename))
                    self.stop()
            print(".", end="", flush=True)


print("Scanning for a live URL", end="", flush=True)

work_queue = queue.Queue()
threads = list()
for x in range(20):
    # Start 20 threads.
    thread = ScanThread(work_queue)
    thread.start()
    threads.append(thread)

while work_queue.empty():
    # Wait for a file to be found.
    pass

(url, filename) = work_queue.get()

for thread in threads:
    thread.stop()
    thread.join()

print("\nFound one!")
print("Live URL: {}".format(url))
print("Filename: {}".format(filename))
webbrowser.open(url)
