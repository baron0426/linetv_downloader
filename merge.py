import os
import natsort

with open(os.path.join('merged.ts'), 'wb+') as handle:
    for file in natsort.natsorted(os.listdir('decrypted')):
        with open(os.path.join('decrypted', file), 'rb') as handle2:
            handle.write(handle2.read())
