<script lang="ts">
	import Chart from './Chart.svelte'
	import { onMount } from 'svelte';

	let rn =0
	let devices = []

	const periods = ['d', 'w', 'm']
	let period = 'd'
	let offset = 0
	let now = new Date()

	function addDays(date, days) {
		var result = new Date(date);
		result.setDate(result.getDate() + days);
		return result;
	}
	function addMonths(date, months) {
		var result = new Date(date);
		result.setMonth(result.getMonth() + months);
		return result;
	}	$:refdate = period == 'd' ? addDays(now, offset) : (period == 'w' ? addDays(now, 7*offset) : addMonths(now, offset))

	let selected_uuid

	let show_dev = false
	let data 

	let show_chart = false

	function toISO(date){
		var isoDateTime = new Date(date.getTime() - (date.getTimezoneOffset() * 60000)).toISOString().replace('T', ' ').substring(0,19);
		return isoDateTime
	}

	function complete_data(d, period){
		let cpldata = []
		if (d.length > 0){
			let refdate = new Date(Date.parse(d[0][0].replace(' ', 'T')))
			let didx = 0
			if (period == 'd'){
				for(var h of [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]){
					let hour = new Date(refdate.setHours(h, 0, 0))
					hour = toISO(hour)
					if (hour == d[didx][0]){
						cpldata.push([h, d[didx][1]])
					}else{
						cpldata.push([h, 0])
					}
				}
			}else if(period == 'w'){
				refdate = addDays(refdate, -refdate.getDay()+1)
				const daydic = {0:'Mo', 1:'Tu', 2:'We', 3:'Th', 4:'Fr', 5:'Sa', 6:'Su'}
				for(var day_offset of [0,1,2,3,4,5,6]){		
					
					let hour = toISO(addDays(refdate, day_offset))
					if (hour == d[didx][0]){
						cpldata.push([daydic[day_offset], d[didx][1]])
					}else{
						cpldata.push([daydic[day_offset], 0])
					}
				}				
			}else if(period == 'm'){
				refdate = addDays(refdate, -refdate.getDate()+1)
				for(var day_offset of [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]){					

					let hour = addDays(refdate, day_offset)
					if (hour.getMonth() != refdate.getMonth()){
						break;
					}
					hour = toISO(hour)
					if (hour == d[didx][0]){
						cpldata.push([day_offset+1, d[didx][1]])
					}else{
						cpldata.push([day_offset+1, 0])
					}
				}				
			}
		}
		return cpldata
	}

	$:if (show_dev){
		let endpoint = {'d':'/hoursInDay', 'w':'/daysInWeek', 'm':'/daysInMonth'}[period]		
		fetch(`${endpoint}?device=${selected_uuid}&day=${refdate.toISOString()}`)
			.then((r)=>r.json())
			.then((d) => {
				show_chart = false
				data = complete_data(d, period)
				show_chart = true
			})
	}

	function getDevices(){
		fetch(`/devices`)
			.then((r) => r.json())
			.then((data) => {
				devices = data.map(x => {return {'uuid':x[0], 'name':x[1], 'created_at':x[2]}})
			})
	}

	function showDevice(uuid){
		show_dev = true
		selected_uuid = uuid
	}

	onMount(() => {
		getDevices()
	})
	
	
	
</script>

<main>
	<div>
		{#each devices as {uuid, name}, i}
			<button on:click={showDevice(uuid)}>{name}</button>
		{/each}
	</div>
	{#if show_dev}
		<div>
			<span>{toISO(refdate).split(' ')[0]}</span>
			<button 
				class:active="{period === 'd'}"
				on:click="{() => {period = 'd'; offset=0}}"
			>day</button>
			<button
				class:active="{period === 'w'}"
				on:click="{() => {period = 'w'; offset=0}}"
			>week</button>
			<button
				class:active="{period === 'm'}"
				on:click="{() => {period = 'm'; offset=0}}"
			>month</button>	
		</div>
		{#if show_chart}
			<div class="chartwrap">
				<div class="chartwrap-left"><button class="vertical-center" on:click="{() => offset -= 1}">&lt;</button></div>
				<div class="chartwrap-center"><Chart data={data} /></div>
				<div class="chartwrap-right"><button class="vertical-center" on:click="{() => offset += 1}">&gt;</button></div>
			</div>
		{/if}
	{/if}


</main>

<style>
	main {
		margin: 0 auto;
	}

	.active {
		background-color: #ff3e00;
		color: white;
	}

	.chartwrap {
		display:grid;
		grid-template-columns: 10% 50% 40%;
	}
	.chartwrap-left {
		grid-column:1;
		overflow: hidden;
		text-align:right;
		padding-right:100px;
		height:400px;
		position:relative;
	}
	.chartwrap-center {
		grid-column:2;
  		overflow: hidden;	
	}
	.chartwrap-right {
		grid-column:3;
  		overflow: hidden;	
		text-align:left;
		height:400px;
		position:relative;
	}
	.vertical-center {
		margin: 0;
		
		position: absolute;
		height:200px;
		top:50px;
	}
	
</style>