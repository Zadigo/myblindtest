<template>
  <div class="chart-container">
    <canvas ref="chartRef" />
  </div>
</template>

<script lang="ts" setup>
import { defaultOptions } from '@/plugins/chartjs'
import { Chart, type ChartData, type ChartOptions } from 'chart.js'
import { onMounted, ref, watch, type PropType } from 'vue'

const props = defineProps({
  chartData: {
    type: Object as PropType<ChartData>,
    required: true
  },
  options: {
    type: Object as PropType<ChartOptions>,
    default: () => defaultOptions
  },
  height: {
    type: String,
    default: '400px'
  }
})

const chartRef = ref<HTMLCanvasElement | null>(null)
let chart: Chart | null = null

// Create chart instance
function createChart () {
  if (chartRef.value) {
    chart = new Chart(chartRef.value, {
      type: 'bar',
      data: props.chartData,
      options: props.options
    })
  }
}

function updateChart () {
  if (chart) {
    chart.data = props.chartData
    chart.update()
  }
}

// Lifecycle hooks
onMounted(() => {
  createChart()
})

// Watch for data changes
watch(() => props.chartData, () => {
  updateChart()
}, { deep: true })

// Clean up on unmount
defineExpose({
  destroyChart: () => {
    if (chart) {
      chart.destroy()
      chart = null
    }
  }
})
</script>

<style lang="scss" scoped>
.chart-container {
  position: relative;
  height: v-bind('height');
  width: 100%;
}
</style>
