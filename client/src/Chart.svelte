<script>

    export let data;// = [['a',1],['b',3],['c',2]]

    //import * as echarts from 'echarts'
    import Chart from 'chart.js/auto';


    let container
    let chart
    $: (() => {
        if (!container) {return}
        while(container.children.length > 0) {container.removeChild(container.children[0])}
        let canvas = document.createElement('canvas')
        container.appendChild(canvas)
        chart = new Chart(canvas, {
            type:'bar',
            data:{
                labels:data.map(x=>x[0]),
                datasets: [{
                    label:'meters walked',
                    data:data.map(x=>x[1])
                }]
            },
            options:{}
        })
    })()

    /*
    let chart
    let dochart = false
    $:chartElem ? (()=>{chart = echarts.init(chartElem); dochart = true;console.log('chartElem', chartElem)})(): console.log('no chartElem')
    $:dochart ? (() => {
            chart.setOption({
                title:{
                    text:'Test'
                },
                tooltip:{},
                xAxis:{
                    data:data.map(x=>x[0])
                },
                yAxis:{},
                series:[
                    {
                        name:'meters',
                        type:'bar',
                        data:data.map(x=>x[1])
                    }
                ]
            });
            console.log('chart', chart)
        })()
        : console.log('no chart')
    
    */
</script>

<div bind:this={container} style="width: 600px;height:400px;">
</div>