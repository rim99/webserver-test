import datetime
import urllib.request
import concurrent.futures
import argparse

SUCCESS = []
FAILURE = []
START_TIME = datetime.datetime.now()

def try_url(url, timeout):
    start = datetime.datetime.now()
    try:
        urllib.request.urlopen(url, timeout=timeout)
        end = datetime.datetime.now()
        SUCCESS.append((end - start).total_seconds())
    except Exception as msg:
        # print('Other error: ', msg)
        end = datetime.datetime.now()
        FAILURE.append((end - start).total_seconds())

def analysis_data():
    END_TIME = datetime.datetime.now()
    success = len(SUCCESS)
    failure = len(FAILURE)
    total_requests = success + failure
    success_ratio = round(success/total_requests, 2)*100
    total_time = (END_TIME-START_TIME).total_seconds()
    average_requests = round(total_requests/total_time, 2)
    print('Total requests: %d\nTotal time: %f\
          \nSuccess ratio: %f\nAverage requests per second: %f'\
          % (total_requests, total_time, success_ratio, average_requests))
    max = 0; min = 99999; total = 0
    for i in SUCCESS:
        if i > max:
            max = i
        if i < min:
            min = i
        total += i
    average = total/success
    print("Max request lapse: %f \
          \nMin request lapse: %f \
          \nAvg request lapse: %f"\
          % (max, min, average))

def main(max_jobs, thread_num, url, timeout):
    print('Running')
    count = 0
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread_num) as pool:
            while count != max_jobs:
                thread_r = pool.submit(try_url, url, timeout)
                count += 1
    except Exception as msg:
        print(msg)
    finally:
        analysis_data()

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Argument parser')
    parse.add_argument('-n', '--thread_num', help='The max number of workers in threads pool',
                       type=int, default=200)
    parse.add_argument('-u', '--url', help='The url of target for testing',
                       type=str)
    parse.add_argument('-t', '--timeout', help='The timeout-request will be treated as a failure',
                       type=int, default=999)
    parse.add_argument('-m', '--max_jobs', help="The maximum of request jobs",
                       type=int, default=1000)
    args = parse.parse_args()
    main(args.max_jobs, args.thread_num, args.url, args.timeout)



