"""SwanLab visualizations for the original LIBERO lifelong-learning trainer."""

import numpy as np
import swanlab
from swanlab import echarts


def log_result_summary(result_summary, *, step):
    metrics = {}
    for name, source in (
        ("success_confusion_matrix", "S_conf_mat"),
        ("loss_confusion_matrix", "L_conf_mat"),
    ):
        matrix = np.asarray(result_summary[source])
        labels = [str(i) for i in range(matrix.shape[1])]
        chart = (
            echarts.HeatMap()
            .add_xaxis(labels)
            .add_yaxis(
                name,
                [str(i) for i in range(matrix.shape[0])],
                [[j, i, float(matrix[i, j])] for i in range(matrix.shape[0]) for j in range(matrix.shape[1])],
            )
            .set_global_opts(
                visualmap_opts=echarts.options.VisualMapOpts(min_=float(matrix.min()), max_=float(matrix.max()))
            )
        )
        metrics[name] = chart
    for name, source in (("fwd_transfer_success", "S_fwd"), ("fwd_transfer_loss", "L_fwd")):
        values = np.asarray(result_summary[source]).tolist()
        metrics[name] = echarts.Line().add_xaxis([str(i) for i in range(len(values))]).add_yaxis(name, values)
    swanlab.log(metrics, step=step)
