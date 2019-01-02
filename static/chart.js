
// Notice that the dataset has missing data

var createChartData = function(wordString){

  let d = []
  let c = 0;
  let ud = [0, 0]
  for (var i = 0; i < wordString.length; i++) {
      let [a, b] = [parseInt(wordString[i]) || 0, parseInt(wordString[i+1]) || 0]

      ud[0] = Math.min(ud[0], a, b)
      ud[1] = Math.max(ud[1], a, b)

      d.push([c++, a, b])
  }

  return [d, ud];

}

let [d, ud] = createChartData(wordString)

console.log('limits', ud)

var chart = Highcharts.stockChart('container', {
    chart: {
      type: 'areasplinerange'
      , zoomType: 'x'
    },

    rangeSelector: {
        enabled: false
    }
    , navigator: {
        enabled: false
    }

    , yAxis: {
        min: ud[0]
        , max: ud[1]
    }

    , title: {
      text: 'Spoken'
    }

    , series: [{
      name: 'Waveform'
      , data: d
      , lineWidth: 0
      , color: '#219dac'
    }]

    , credits: {
        enabled: false
    }

  });
