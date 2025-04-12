import requests, hashlib, json, random, time #, locale
# locale.setlocale(locale.LC_ALL, 'Russian')
from data.configs_reader import DIR
from .cf_configs_reader import get_cf_configs, load_default_configs
from utils import logger, read, write


methods = ['contest.status', 'contest.standings']
formats = ['neoSaris', 'S4RIS']


class ContestInfo:
    def __init__(self, data):
        self.__is_private = data['IS_PRIVATE_GROUP'] == 'true'
        self.__group_code = data['GROUP_CODE']
        self.__contest_id = data['CONTEST_ID']
        self.__as_manager = data['AS_MANAGER']
        self.__api_key = data['CF_API_KEY']
        self.__api_secret = data['CF_API_SECRET']
        self.__frozen_time = data['FROZEN_TIME']
        self.__showUnofficial = data['SHOW_UNOFFICIAL']
        self.__reqs = dict() # TODO analyze efficiency


    def build_params(self, method):
        if not self.__is_private:
            params_req = f'contestId={self.__contest_id}'
            return params_req
        
        key = f'apiKey={self.__api_key}'
        mngr = f'&asManager={self.__as_manager}'
        ID = f'&contestId={self.__contest_id}'
        code = f'&groupCode={self.__group_code}'
        showUnofficial = ''
        if method == 'contest.standings':
            showUnofficial = f'&showUnofficial={self.__showUnofficial}'
        rand = str(random.randint(0, 999999) + 100000)
        current_time = f'&time={int(time.time())}'
        # participantTypes = '&participantTypes=VIRTUAL'
        str_params = f'{key}{mngr}{ID}{code}{showUnofficial}{current_time}'
        str_req  = f'{rand}/{method}?{str_params}#{self.__api_secret}'
        hash = hashlib.sha512(str_req.encode()).hexdigest()
        api_sig = rand + hash
        params_req = f'{str_params}&apiSig={api_sig}'
        return params_req


    def get_contest_data(self, method):
        status = 'OK'
        logs = f'Loading cashed data for {method}\n'
        contest_data = self.__reqs.get(method)
        if contest_data == None:
            logs = f'Sending request {method} to codeforces\n'
            logger.info(logs)
            url = 'https://codeforces.com/api/'
            params = self.build_params(method)
            req = f'{url}{method}?{params}'
            file_name = f'{DIR}/logs/{self.__contest_id}_{method}.json'
            N = 2
            for i in range(1,N):
                # if i > 1:
                #     logger.info('try #{i}\n')
                contest_data = requests.get(req).json()
                status = contest_data['status']
                if status == 'OK':
                    self.__reqs.update({method: contest_data})
                    break
                if i < 5:
                    time.sleep(5 * i)
            else:
                err_logs = f'{status}. Try again later.\n' # More at {file_name}\n'
                logger.error(err_logs)
                logs += err_logs
            write(contest_data, file_name)
        return status, logs, contest_data


    def format_submissions(self, duration, format_id=0):
        status, logs, contest_sub = self.get_contest_data('contest.status')
        list_contest_sub = contest_sub
        # sub_team_names = set()
        if status == 'OK':
            list_contest_sub = list()
            contest_sub = sorted(list(contest_sub['result']), key=lambda sub: sub['relativeTimeSeconds']) #not necessary
            for sub in contest_sub:
                time_sub = sub['relativeTimeSeconds'] // 60
                if (
                    (
                        sub['author']['participantType'] == 'CONTESTANT'
                        or self.__showUnofficial == 'true'
                    ) 
                    and not sub['author']['ghost'] 
                    and time_sub <= duration
                ):
                    sub['party'] = sub['author']
                    team_name = self.get_contestants_names(sub)
                    # sub_team_names.add(team_name)
                    template = [
                        {
                            'timeSubmitted': time_sub, 
                            'contestantName': team_name,
                            'problemIndex': sub['problem']['index'],
                            'verdict': sub['verdict']
                        },
                        {
                            'contestant': team_name,
                            'problemLetter': sub['problem']['index'],
                            'timeMinutesFromStart': time_sub,
                            'success': sub['verdict'] == 'OK'
                        }
                    ]
                    list_contest_sub.append(template[format_id])
        return status, logs, list_contest_sub #, sub_team_names
        

    def format_standings(self, format_id=0):
        status, logs, contest_data = self.get_contest_data('contest.standings')
        stands = contest_data
        if status == 'OK':
            duration = contest_data['result']['contest']['durationSeconds'] // 60
            if formats[format_id] == 'neoSaris':
                problem_func = lambda problem: {'index': problem['index'], 'name': problem['name']}
                contestants_func = lambda row: {'id': row[0], 'name': row[1]}
            else:
                if type(self.__frozen_time) == int:
                    self.__frozen_time = int(self.__frozen_time)
                else:
                    self.__frozen_time = 60
                self.__frozen_time = duration - self.__frozen_time
                problem_func = lambda problem: problem['index']
                contestants_func = lambda row: row[1]
            _, _, contestants_names = self.get_request_contestants()
            # contestants_names = sub_team_names.union(contestants_names)
            stands = {
                'contestData': {
                    'duration': duration,
                    'frozenTimeDuration': self.__frozen_time,
                    'name': contest_data['result']['contest']['name'],
                    'type': contest_data['result']['contest']['type']
                },
                'problems': list(map(problem_func, contest_data['result']['problems'])),
                'contestants': list(map(contestants_func, enumerate(contestants_names)))
            }
        return status, logs, stands


    def format_JSON(self, format_id=0):
        status, logs, contest_data = self.format_standings(format_id)
        result = contest_data
        if status == 'OK':
            duration = contest_data['contestData']['duration']
            status, sub_logs, submissions = self.format_submissions(duration, format_id)
            logs += sub_logs
            result = submissions
            if status == 'OK':
                if formats[format_id] == 'neoSaris':
                    contest_data['contestData']['type'] = 'ICPC'
                    neoSaris_JSONobject = {
                        'contestMetadata': contest_data['contestData'],
                        'problems': contest_data['problems'],
                        'contestants': contest_data['contestants'],
                        'verdicts': {
                            'accepted': ["OK", "PARTIAL"],
                            'wrongAnswerWithPenalty': [
                            "FAILED",
                            "RUNTIME_ERROR",
                            "WRONG_ANSWER",
                            "PRESENTATION_ERROR",
                            "TIME_LIMIT_EXCEEDED",
                            "MEMORY_LIMIT_EXCEEDED",
                            "IDLENESS_LIMIT_EXCEEDED",
                            "SECURITY_VIOLATED",
                            "CRASHED",
                            "INPUT_PREPARATION_CRASHED",
                            "CHALLENGED",
                            "REJECTED",
                            "SKIPPED",
                            ],
                            'wrongAnswerWithoutPenalty': ["COMPILATION_ERROR"],
                        },
                        'submissions': submissions
                    }
                    result = neoSaris_JSONobject
                else:
                    S4RIS_JSONobject = {
                        'contestName': contest_data['contestData']['name'],
                        'freezeTimeMinutesFromStart': contest_data['contestData']['frozenTimeDuration'],
                        'problemLetters': contest_data['problems'],
                        'contestants': contest_data['contestants'],
                        'runs': submissions
                    }
                    result = S4RIS_JSONobject
        return status, logs, result


    def clean_data(self, rawdata):
        return {s.replace('\x00', '') for s in rawdata if isinstance(s, str)} 


    def get_contestants_names(self, row):
        return (
            row['party']['members'][0].get('name') or 
            row['party']['members'][0].get('handle') or 
            row['party'].get('teamName') or
            f'NO_NAME_{row['party'].get('participantId')}'
        )


    def get_request_contestants(self):
        status, logs, contest_data = self.get_contest_data('contest.standings')
        contestants_names = None
        if status == 'OK':
            contestants_names = self.clean_data(set(map(self.get_contestants_names, contest_data['result']['rows'])))
        return status, logs, contestants_names


    def get_saved_contestants(self, chat_id):
        file_name = f'{DIR}/data/Names_{chat_id}_{self.__contest_id}.json'
        status, logs, contestants_names = read(file_name)
        if status == 'FAILED':
            status, req_logs, contestants_names = self.get_request_contestants()
            contestants_names = dict.fromkeys(contestants_names, None)
            logs += req_logs
            if status == 'OK':
                create_logs = f'Creating file\n' # {file_name}\n'
                logger.info(create_logs)
                logs += create_logs
                write(contestants_names, file_name, is_json=True)
        return status, logs, contestants_names


    def check_new_contestants(self, chat_id):
        status, logs, new_contestants_names = self.get_request_contestants()
        diff = None
        if status == 'OK':
            file_name = f'{DIR}/data/Names_{chat_id}_{self.__contest_id}.json'
            status, read_logs, contestants_names = read(file_name)
            if status == 'FAILED':
                status = 'OK'
                contestants_names = dict()
                create_logs = f'Creating file\n' # {file_name}\n'
                logger.info(create_logs)
                read_logs += create_logs
            logs += read_logs
            if len(contestants_names) < len(new_contestants_names):
                diff = dict.fromkeys(new_contestants_names - set(contestants_names.keys()), None)
                new_contestants_names = dict.fromkeys(new_contestants_names, None) | contestants_names
                write(new_contestants_names, file_name, is_json=True)
        return status, logs, diff


def get_unfreezed_standings(chat_id):
    status, logs, configs = get_cf_configs(chat_id)
    if status == 'FAILED':
        status, def_logs, configs = load_default_configs(chat_id)
        logs += def_logs
    docs = [(status, logs, None, None)]
    if status == 'OK':
        docs = list()
        new_contest_data = ContestInfo(configs)
        contest_id = configs['CONTEST_ID']
        for format_id, format in enumerate(formats):
            status, logs, json_obj = new_contest_data.format_JSON(format_id)
            file_name = f'{contest_id}_{format}_logs.json'
            docs.append((status, logs, json_obj, file_name))
            if status == 'FAILED':
                break
    return docs


def get_contestants(chat_id, key='all'):
    status, logs, configs = get_cf_configs(chat_id)
    if status == 'FAILED':
        status, def_logs, configs = load_default_configs(chat_id)
        logs += def_logs
    names = None
    if status == 'OK':
        new_contest_data = ContestInfo(configs)
        if key == 'all':
            status, logs, names = new_contest_data.get_saved_contestants(chat_id)
        elif key == 'new':
            status, logs, names = new_contest_data.check_new_contestants(chat_id)
    return status, logs, names