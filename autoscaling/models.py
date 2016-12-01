class ScalingRuleItem:
    def __init__(self, metric, upper_threshold, lower_threshold, node_up, node_down):
        self.id = metric
        self.metric = metric
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold
        self.node_up = node_up
        self.node_down = node_down