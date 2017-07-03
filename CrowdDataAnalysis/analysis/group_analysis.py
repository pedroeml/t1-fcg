from collections import deque
import json


class GroupAnalysis:
    def __init__(self, groups):
        self.min_num_groups = len(groups)
        self.avg_num_groups = 0
        self.max_num_groups = len(groups)
        self.min_group_elements = len(groups[0])
        self.avg_group_elements = 0
        self.max_group_elements = len(groups[0])
        self.fields = {
            'min_num_groups': deque(),
            'avg_num_groups': deque(),
            'max_num_groups': deque(),
            'min_group_elements': deque(),
            'avg_group_elements': deque(),
            'max_group_elements': deque()
        }
        self.frames_count = 0
        self.receive_groups(groups)
        self.exported = False

    def receive_groups(self, groups):
        self.update_num_groups(groups)
        self.update_group_elements(groups)

        self.fields['min_num_groups'].append(self.min_num_groups)
        self.fields['avg_num_groups'].append(self.avg_num_groups)
        self.fields['max_num_groups'].append(self.max_num_groups)
        self.fields['min_group_elements'].append(self.min_group_elements)
        self.fields['avg_group_elements'].append(self.avg_group_elements)
        self.fields['max_group_elements'].append(self.max_group_elements)

        self.frames_count += 1

    def update_num_groups(self, groups):
        if len(groups) < self.min_num_groups:
            self.min_num_groups = len(groups)
        elif len(groups) > self.max_num_groups:
            self.max_num_groups = len(groups)

        self.avg_num_groups = (self.avg_num_groups * self.frames_count + len(groups)) / (self.frames_count + 1)

    def update_group_elements(self, groups):
        sum_group_elements = 0
        for group in groups:
            if len(group) < self.min_group_elements:
                self.min_group_elements = len(group)
            elif len(group) > self.max_group_elements:
                self.max_group_elements = len(group)

            sum_group_elements += len(group)

        avg_group_elements = sum_group_elements / len(groups)
        self.avg_group_elements = (self.avg_group_elements * self.frames_count + avg_group_elements) / (self.frames_count + 1)

    def export_analysis(self, filepath=''):
        d = {}
        for k, v in self.fields.items():
            d[k] = list(v)

        if filepath:
            with open(filepath, 'w') as f:
                json.dump(d, f)

        self.exported = True
        return d
