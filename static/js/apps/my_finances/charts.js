$(document).ready(function () {
    $.get("/my_finances/current_finances/get_summary_tiles", function (data) {
        for (const [data_name, v] of Object.entries(data)) {
            if (data_name === 'error') {
                $('#summary_tiles').html(v)
            } else if (data_name === 'last_balance_date') {
                $(`#${data_name}`).html(v)
            } else {
                $(`#${data_name}`).html(
                    new Intl.NumberFormat('en-IE', {style: 'currency', currency: 'EUR'}).format(v)
                )
            }
        }
    });

    $.get("/my_finances/current_finances/get_year_chart", function (res) {
        let canvas = $('#year_chart_canvas')
        const config = {
            type: 'line',
            data: {
                labels: res.labels,
                datasets: [
                    {
                        type: 'scatter',
                        label: 'Balance Checks',
                        data: res.data_balance_check,
                        borderWidth: 2,
                        backgroundColor: 'rgba(28, 200, 138, 0.1)',
                        borderColor: 'rgba(28, 200, 138, 1)',
                    },
                    {
                        type: 'scatter',
                        label: 'Balance Today',
                        data: res.data_today,
                        borderWidth: 2,
                        backgroundColor: 'rgba(246, 194, 62, 0.1)',
                        borderColor: 'rgba(246, 194, 62, 1)',
                    },
                    {
                        label: 'Balance Estimated',
                        data: res.data_estimated,
                        fill: true,
                        borderWidth: 2,
                        backgroundColor: "rgba(78, 115, 223, 0.1)",
                        borderColor: "rgba(78, 115, 223, 1)",
                        cubicInterpolationMode: 'monotone',
                        tension: 0.4,
                        pointRadius: 0,
                    },
                ]
            },
            options: {
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 10,
                        top: 10,
                        bottom: 5
                    }
                },
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: false,
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        position: 'nearest'
                    }
                },
                elements: {
                    point: {
                        radius: 4,
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                            drawBorder: false
                        },
                        ticks: {
                            display: true,
                            autoSkip: true
                        }
                    },
                    y: {
                        ticks: {
                            maxTicksLimit: 5,
                            padding: 10,
                            // Include a dollar sign in the ticks
                            callback: function (value, index, values) {
                                return new Intl.NumberFormat('en-IE', {
                                    style: 'currency', currency: 'EUR',
                                    maximumSignificantDigits: 1
                                }).format(value);
                            }
                        },
                        gridLines: {
                            color: "rgb(234, 236, 244)",
                            zeroLineColor: "rgb(234, 236, 244)",
                            drawBorder: false,
                            borderDash: [2],
                            zeroLineBorderDash: [2]
                        }
                    },
                }
            }
        };
        new Chart(canvas, config);
    });

    $.get("/my_finances/current_finances/get_income_or_outcome_by_type?get_what=income", function (res) {
        let canvas = $('#income_by_type')
        const config = {
            type: 'doughnut',
            data: {
                labels: res.labels,
                datasets: [
                    {
                        label: 'Income',
                        data: res.data,
                        backgroundColor: [
                            'rgb(255, 99, 132)',
                            'rgb(75, 192, 192)',
                            'rgb(255, 205, 86)',
                            'rgb(54, 162, 235)'
                        ],
                        hoverOffset: 4,
                    }
                ]
            },
            options: {
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 5,
                        right: 5,
                        top: 5,
                        bottom: 5
                    }
                },
                responsive: true,
            }
        };
        new Chart(canvas, config);
    });

    $.get("/my_finances/current_finances/get_income_or_outcome_by_type?get_what=outcome", function (res) {
        let canvas = $('#outcome_by_type')
        const config = {
            type: 'doughnut',
            data: {
                labels: res.labels,
                datasets: [
                    {
                        label: 'Outcome',
                        data: res.data,
                        backgroundColor: [
                            'rgb(255, 99, 132)',
                            'rgb(255, 159, 64)',
                            'rgb(255, 205, 86)',
                            'rgb(75, 192, 192)',
                            'rgb(54, 162, 235)',
                            'rgb(153, 102, 255)',
                            'rgb(201, 203, 207)',
                            'rgb(255, 205, 86)',
                            'rgb(75, 192, 192)',
                        ],
                        hoverOffset: 4,
                    }
                ]
            },
            options: {
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 5,
                        right: 5,
                        top: 5,
                        bottom: 5
                    }
                },
                responsive: true,
            }
        };
        new Chart(canvas, config);
    });

})
