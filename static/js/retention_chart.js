function initRetentionChart(data, colors) {
  const retentionOptions = {
    series: [{
      name: 'Retention Rate',
      type: 'area',
      data: data.retention
    }, {
      name: 'Graduation Ready %',
      type: 'line',
      data: data.graduationReady
    }],
    chart: {
      height: 300,
      type: 'line',
      fontFamily: 'inherit',
      foreColor: colors.textColor,
      stacked: false,
      toolbar: {
        show: false
      }
    },
    colors: [colors.success, colors.warning],
    stroke: {
      width: [2, 3],
      curve: 'smooth'
    },
    plotOptions: {
      bar: {
        columnWidth: '50%'
      }
    },
    fill: {
      type: ['gradient', 'solid'],
      gradient: {
        shade: 'light',
        type: "vertical",
        opacityFrom: 0.7,
        opacityTo: 0.2
      }
    },
    labels: [
      'Current',
      '-1 Month',
      '-2 Months',
      '-3 Months',
      '-4 Months',
      '-5 Months'
    ],
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Time Period',
        style: {
          color: colors.textColor
        }
      },
      labels: {
        style: {
          colors: colors.textColor
        }
      }
    },
    yaxis: [
      {
        title: {
          text: 'Retention %',
          style: {
            color: colors.textColor
          }
        },
        labels: {
          style: {
            colors: colors.textColor
          }
        },
        min: 0,
        max: 100
      },
      {
        opposite: true,
        title: {
          text: 'Graduation Ready %',
          style: {
            color: colors.textColor
          }
        },
        labels: {
          style: {
            colors: colors.textColor
          }
        }
      }
    ],
    tooltip: {
      theme: document.body.classList.contains('dark-theme') ? 'dark' : 'light',
      shared: true,
      intersect: false,
      y: {
        formatter: function(y) {
          if (typeof y !== "undefined") {
            return y.toFixed(1) + "%";
          }
          return y;
        }
      }
    },
    legend: {
      labels: {
        colors: [colors.textColor]
      }
    }
  };

  const retentionChart = new ApexCharts(document.querySelector("#retentionChart"), retentionOptions);
  retentionChart.render();
} 