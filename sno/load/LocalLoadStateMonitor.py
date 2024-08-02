class LocalLoadStateMonitor:
    def __init__(self):
        self.current_process_name = "Initializing"
        self.overall_progress = 0

    def set_current_process(self, name, overall_progress):
        self.current_process_name = name
        self.overall_progress = overall_progress

    def set_overall_progress(self, overall_progress):
        self.overall_progress = overall_progress

    def get_process_name(self):
        return self.current_process_name

    def get_overall_progress(self):
        return self.overall_progress
