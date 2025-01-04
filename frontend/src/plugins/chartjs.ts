import {
    Chart,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    LineController,
    BarElement,
    BarController,
    Title,
    Tooltip,
    Legend,
    type ChartOptions
} from 'chart.js'

Chart.register(
    CategoryScale,
    LinearScale,
    LineElement,
    LineController,
    BarElement,
    BarController,
    PointElement,
    Title,
    Tooltip,
    Legend
)

export const defaultOptions: ChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top' as const
        },
        title: {
            display: true,
            text: 'Chart.js Bar Chart'
        }
    }
}
