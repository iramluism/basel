from enum import Enum


class ReportFormat(str, Enum):
    BASIC = "basic"
    HTML = "html"
    MEAN_I = "mean_i"
    MEAN_A = "mean_a"
    MEAN_E = "mean_e"
    MEAN = "mean"
