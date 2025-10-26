<template>
  <volt-card class="border-none">
    <template #content>
      <bar-chart :chart-data="genreChartData" :options="genreChartOptions" height="300px" />
    </template>
  </volt-card>
</template>

<script lang="ts" setup>
import type { ChartData, ChartOptions } from 'chart.js'
import type { StatisticsData } from '@/types';

const props = defineProps<{ chartData: StatisticsData | undefined }>()

const labels = computed(() => props.chartData?.labels || [])
const data = computed(() => props.chartData?.data || [])

const genreChartData: ChartData = ref({
  labels: labels.value,
  datasets: [{
    label: 'Number of Songs',
    data: data.value,
    backgroundColor: [
      'rgba(255, 99, 132, 0.5)',
      'rgba(54, 162, 235, 0.5)',
      'rgba(255, 206, 86, 0.5)',
      'rgba(75, 192, 192, 0.5)'
    ],
    borderColor: [
      'rgba(255, 99, 132, 1)',
      'rgba(54, 162, 235, 1)',
      'rgba(255, 206, 86, 1)',
      'rgba(75, 192, 192, 1)'
    ],
    borderWidth: 1
  }]
})

const genreChartOptions = computed<ChartOptions>(() => ({
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    },
    title: {
      display: true,
      text: 'Distribution of Songs by Genre'
    }
  }
}))
</script>
