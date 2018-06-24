let playApp = new Vue({
    el: '#play_app'
    , data: {
        inputString: `No sentence can be effective if it contains facts alone.
        It must also contain emotion, image, logic, and promise.`
    }
    , methods: {
        play(){
            var data = new FormData();
            data.append('text', this.inputString)
            this.$http.post('/convert/', data).then(this.playCallback)
        }

        , playCallback(d){
            console.log(d)
            let player = this.$refs.audio
            player.src = `${d.data.covert_output_dir}/${d.data.created_file}`
            this.$http.get('/static/output/ss.js').then(this.ssCallback)
        }

        , ssCallback(data) {

            eval(data.body)
            let [d, ud] = createChartData(wordString)
            chart.series[0].destroy()
            chart.yAxis[0].setExtremes(ud[0], ud[1])
            chart.addSeries({ data: d})
            let player = this.$refs.audio
            player.play()
        }
    }
})
