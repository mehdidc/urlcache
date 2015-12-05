import os
import wget

folder = os.path.join(os.getenv("HOME"), ".urlcache")


def download(url, out=None):

    url_hash = url_hash_(url)

    if not os.path.exists(folder):
        os.mkdir(folder)

    url_hash_filename = os.path.join(folder, url_hash)

    if os.path.exists(url_hash_filename):
        with open(url_hash_filename) as fd:
            filename = fd.read()
    else:
        filename = wget.download(url, out=folder)
        with open(url_hash_filename, "w") as fd:
            fd.write(filename)
    if out is None:
        out = "."

    if os.path.isdir(out):
        out = out + os.path.basename(filename)
    try:
        os.symlink(filename, out)
    except OSError:
        print("{} exists - cant override".format(out))


def url_hash_(url):
    import md5
    m = md5.new()
    m.update(url)
    return m.hexdigest()


def file_hash_(filename):
    import hashlib
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(filename, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()
