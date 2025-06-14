export default {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './src/App.vue'
  ],
  theme: {
    extend: {
      fontFamily: {
        title: 'Raleway '
      },
      colors: {
        secondary: 'var(--p-primary-300)'
      },
      screens: {}
    }
  },
  plugins: [], 
  darkMode: 'class'
}
