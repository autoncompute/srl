import srl
from datetime import datetime

ServiceName = 'PyEventDetector'

class TaskProgressMessageFactory:
    @staticmethod
    def generate( original_message, progress, status_message, task_id = None ):
        if task_id == None: task_id = original_message['task-id']
        return srl.ProgressMessageFactory.generate(
                original_message, task_id, progress, status_message)

    @staticmethod
    def generate_progress_request( task_id ):
        return srl.ProgressMessageFactory.generate_progress_request(
                ServiceName, 'Progress', task_id)

class CheapEventReportRequestFactory:
    @staticmethod
    def generate( target_location, keylist, analysis_start_date, analysis_end_date ):
        if not isinstance(target_location, str):
            raise Exception('target_location should be a string!')
        if not isinstance(keylist, (list, tuple)):
            keylist = [keylist]
        if not isinstance(analysis_start_date, str):
            raise Exception('analysis_start_date should be a string!')
        if not isinstance(analysis_end_date, str):
            raise Exception('analysis_end_date should be a string!')

        message = srl.InterfaceMessage(ServiceName, 'CheapEventReport')
        message['target-location']      = target_location
        message['keylist']              = keylist
        message['analysis-start-date']  = analysis_start_date
        message['analysis-end-date']    = analysis_end_date
        return message.encode()

    @staticmethod
    def parse( message ):
        if not isinstance(message, srl.InterfaceMessage):
            raise Exception('message should be an InterfaceMessage!')

        request = \
        {
            'target-location'       : message['target-location'],
            'keylist'               : message['keylist'],
            'analysis-start-date'   : datetime.strptime(message['analysis-start-date']  , '%b/%d/%Y').date(),
            'analysis-end-date'     : datetime.strptime(message['analysis-end-date']    , '%b/%d/%Y').date()
        }
        return request

class CheapEventReportResponseFactory:
    @staticmethod
    def generate( original_message, results ):
        if not isinstance(original_message, srl.InterfaceMessage):
            raise Exception('original_message should be an InterfaceMessage!')

        message = srl.InterfaceMessage(
                original_message.get_module(),
                original_message.get_service(),
                original_message.get_client_id())
        message['results'] = results
        for i in xrange(len(message['results'])):
            if not isinstance(message['results'][i][0], str):
                message['results'][i][0] = message['results'][i][0].strftime('%m/%d/%Y')
        return message.encode()