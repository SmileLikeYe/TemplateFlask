updateEcharts = function(option,idName) {
    var myChart=echarts.init(document.getElementById(idName));
    myChart.setOption(option);
}

generateEchartsOption1 = function(chartsData) {
	return {
		    title: {
		        text: '漏斗图',
		        subtext: '纯属虚构'
		    },
		    tooltip: {
		        trigger: 'item',
		        formatter: "{a} <br/>{b} : {c}%"
		    },
		    toolbox: {
		        feature: {
		            dataView: {readOnly: false},
		            restore: {},
		            saveAsImage: {}
		        }
		    },
		    legend: {
		        data: ['展现','点击','访问','咨询','订单']
		    },
		    series: [
		        {
		            name: '预期',
		            type: 'funnel',
		            left: '10%',
		            width: '80%',
		            label: {
		                normal: {
		                    formatter: '{b}预期'
		                },
		                emphasis: {
		                    position:'inside',
		                    formatter: '{b}预期: {c}%'
		                }
		            },
		            labelLine: {
		                normal: {
		                    show: false
		                }
		            },
		            itemStyle: {
		                normal: {
		                    opacity: 0.7
		                }
		            },
		            data: [
		                {value: 60, name: '访问'},
		                {value: 40, name: '咨询'},
		                {value: 20, name: '订单'},
		                {value: 80, name: '点击'},
		                {value: 100, name: '展现'}
		            ]
		        },
		        {
		            name: '实际',
		            type: 'funnel',
		            left: '10%',
		            width: '80%',
		            maxSize: '80%',
		            label: {
		                normal: {
		                    position: 'inside',
		                    formatter: '{c}%',
		                    textStyle: {
		                        color: '#fff'
		                    }
		                },
		                emphasis: {
		                    position:'inside',
		                    formatter: '{b}实际: {c}%'
		                }
		            },
		            itemStyle: {
		                normal: {
		                    opacity: 0.5,
		                    borderColor: '#fff',
		                    borderWidth: 2
		                }
		            },
		            data: chartsData
		        }
		    ]
		};

}

$("#showChars").click(function(){
	
	$.ajax({
            url: "/backend/api/echartsdata",
            type: "POST",
            data: JSON.stringify({"peID": 1}),
            contentType: "application/json; charset=utf-8",
            success: function(response) {
                data = $.parseJSON(response);
                console.log(data);
                updateEcharts(generateEchartsOption1(data),"echarts1")
           	}
     });
})

