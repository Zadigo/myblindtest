<template>
  <section class="my-5">
    <div class="row">
      <div class="col-sm-12 col-md-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <BarChart :chart-data="genreChartData" :options="genreChartOptions" height="300px" />
          </div>
        </div>
      </div>

      <div class="col-sm-12 col-md-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <TimelineChart :chart-data="timelineData" :options="timelineOptions" height="300px" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import type { ChartData, ChartOptions } from 'chart.js'
import { useHead } from 'unhead'
import { computed, ref } from 'vue'

useHead({
  title: 'Statistics',
  meta: [
    {
      name: 'description',
      content: 'Write a description here'
    }
  ]
})

// Sample data - replace with your actual data
const songs = ref([
  { genre: 'Rock', year: 2020 },
  { genre: 'Pop', year: 2021 },
  { genre: 'Jazz', year: 2019 },
  { genre: 'Rock', year: 2021 }
])

// Compute genre data
const genreChartData = computed<ChartData>(() => {
  const genres = [...new Set(songs.value.map(song => song.genre))]
  const counts = genres.map(genre =>
    songs.value.filter(song => song.genre === genre).length
  )

  return {
    labels: genres,
    datasets: [{
      label: 'Number of Songs',
      data: counts,
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
  }
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

const timelineData = computed<ChartData>(() => {
  return {
    labels: [1, 2, 3, 4, 5, 6, 7],
    datasets: [
      {
        label: 'Evolution',
        data: [100, 101, 102, 101, 100, 99, 98],
        borderWidth: 1
      }
    ]
  }
})

const timelineOptions = computed<ChartOptions>(() => ({
  plugins: {
    title: {
      display: true,
      text: 'Timeline evolution'
    }
  }
}))

// Compute year data
// const yearChartData = computed<ChartData>(() => {
//   const years = [...new Set(songs.value.map(song => song.year))].sort()
//   const counts = years.map(year =>
//     songs.value.filter(song => song.year === year).length
//   )

//   return {
//     labels: years,
//     datasets: [{
//       label: 'Songs Released',
//       data: counts,
//       backgroundColor: 'rgba(75, 192, 192, 0.5)',
//       borderColor: 'rgba(75, 192, 192, 1)',
//       borderWidth: 1
//     }]
//   }
// })

// const yearChartOptions = computed<ChartOptions>(() => ({
//   responsive: true,
//   plugins: {
//     legend: {
//       position: 'top'
//     },
//     title: {
//       display: true,
//       text: 'Songs by Release Year'
//     }
//   },
//   scales: {
//     y: {
//       beginAtZero: true,
//       ticks: {
//         stepSize: 1
//       }
//     }
//   }
// }))
</script>

<style scoped>
.charts-dashboard {
  padding: 1rem;
}
</style>
