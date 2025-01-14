import celery


@celery.shared_task
def song_information_completion():
    import time
    print('Works')
    time.sleep(10)
    return True
