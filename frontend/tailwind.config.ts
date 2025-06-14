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
      fontFamily: {},
      colors: {
        bg: {
          primary: 'var(--p-primary-color);'
        }
      },
      screens: {}
    }
  },
  plugins: [], 
  darkMode: 'class'
}
