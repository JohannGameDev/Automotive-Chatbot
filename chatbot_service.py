from mal import MAL
import os
import time

if __name__ == '__main__':
    # logging.basicConfig()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    messenger = MAL()
    messenger.start_services()
    print('Listening ...')
    # Keep the program running.

    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        messenger.shutdown()
